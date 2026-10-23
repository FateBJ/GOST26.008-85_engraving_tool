"""Qt front-end for the GOST 26.008-85 G-code generator.

Run with:  python app.py

The form itself lives in main.ui (editable in Qt Designer); all signal
handling and the call into the generator are in this module.
"""

import os
import sys
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets, uic

import main as engine

UI_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.ui")

#: Anchor points, in the same order as the items of originCombo in main.ui.
ORIGINS = [
    "Bottom center",
    "Bottom left",
    "Bottom right",
    "Center",
    "Middle left",
    "Middle right",
    "Top center",
    "Top left",
    "Top right",
]

FILE_FILTER = "G-code (*.nc *.tap *.gcode *.ngc *.txt);;All files (*)"

#: Wayland cannot activate a window on request, so Qt prints this warning every
#: time a dialog asks for focus.  It is harmless and there is nothing to fix.
WAYLAND_ACTIVATION_WARNING = "Wayland does not support QWindow::requestActivate()"


def qt_message_handler(mode, context, message):
    """Forward Qt messages to stderr, dropping only the Wayland focus warning."""
    if WAYLAND_ACTIVATION_WARNING in message:
        return
    if context.category and context.category != "default":
        sys.stderr.write("%s: %s\n" % (context.category, message))
    else:
        sys.stderr.write("%s\n" % message)



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui_file=UI_FILE):
        super().__init__()
        uic.loadUi(ui_file, self)

        if self.originCombo.count() != len(ORIGINS):
            raise RuntimeError(
                "main.ui: originCombo must contain exactly %d items" % len(ORIGINS)
            )

        self._code = ""
        self._last_dir = os.path.expanduser("~")

        self.generateButton.clicked.connect(self.generate)
        self.browseButton.clicked.connect(self.browse)
        self.copyButton.clicked.connect(self.copy_to_clipboard)
        self.modeCombo.currentIndexChanged.connect(self._sync_mode)
        self.textEdit.textChanged.connect(self._on_text_changed)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Return"), self)
        shortcut.activated.connect(self.generate)

        self._sync_mode(self.modeCombo.currentIndex())
        self.set_status("Enter the text and press Generate G-code (Ctrl+Enter).")

    # ------------------------------------------------------------------ UI --
    def _sync_mode(self, index):
        """Spindle speed only makes sense when engraving."""
        engraving = index == 0
        self.spindleSpin.setEnabled(engraving)
        self.spindleLabel.setEnabled(engraving)

    def _on_text_changed(self):
        # A stale preview next to edited text is misleading.
        if self._code:
            self._code = ""
            self.previewEdit.clear()
            self.set_status("Text changed - press Generate G-code to refresh.")

    def set_status(self, message):
        self.statusBar().showMessage(message)

    def warn(self, title, message, details=None):
        box = QtWidgets.QMessageBox(self)
        box.setIcon(QtWidgets.QMessageBox.Warning)
        box.setWindowTitle(title)
        box.setText(message)
        if details:
            box.setDetailedText(details)
        box.exec_()

    # ------------------------------------------------------------ actions --
    def read_params(self):
        """Collect the form into keyword arguments for engine.generate()."""
        return dict(
            font_height=self.heightSpin.value(),
            mode_=self.modeCombo.currentIndex(),
            origin_=self.originCombo.currentIndex(),
            align_=self.alignCombo.currentIndex(),
            z_depth=self.depthSpin.value(),
            safe_height=self.safeSpin.value(),
            cut_speed=self.cutSpeedSpin.value(),
            free_speed=self.freeSpeedSpin.value(),
            spindle_speed=self.spindleSpin.value(),
        )

    def generate(self):
        text = self.textEdit.toPlainText().rstrip("\n")
        if not text.strip():
            self.warn("Nothing to engrave", "Enter the text you want to engrave.")
            return

        try:
            code = engine.generate(text, **self.read_params())
        except Exception:  # keep the form usable on unexpected geometry errors
            details = traceback.format_exc()
            traceback.print_exc()
            self.warn(
                "G-code generation failed",
                "The generator raised an error. The details below may help.",
                details,
            )
            self.set_status("Generation failed.")
            return

        self._code = code
        self.previewEdit.setPlainText(code)
        QtWidgets.QApplication.clipboard().setText(code)

        skipped = self.unsupported_characters(text)
        status = "%d lines of G-code generated and copied to the clipboard." % len(
            code.splitlines()
        )
        if skipped:
            status += " Skipped unsupported characters: %s" % " ".join(skipped)

        path = self.outputEdit.text().strip()
        if path:
            try:
                self.write_file(path, code)
                status += " Saved to %s" % path
            except OSError as exc:
                self.warn("Could not save the file", str(exc))
                status += " Could not save to %s." % path

        self.set_status(status)

    def copy_to_clipboard(self):
        if not self._code:
            self.warn("No G-code yet", "Press Generate G-code first.")
            return
        QtWidgets.QApplication.clipboard().setText(self._code)
        self.set_status("G-code copied to the clipboard.")

    def browse(self):
        start = self.outputEdit.text().strip() or os.path.join(self._last_dir, "part.nc")
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save G-code", start, FILE_FILTER
        )
        if not path:
            return
        self.outputEdit.setText(path)
        self._last_dir = os.path.dirname(path) or self._last_dir
        if self._code:
            try:
                self.write_file(path, self._code)
                self.set_status("Saved to %s" % path)
            except OSError as exc:
                self.warn("Could not save the file", str(exc))
        else:
            self.set_status("The program will be saved to this file when generated.")

    # ------------------------------------------------------------ helpers --
    @staticmethod
    def unsupported_characters(text):
        """Characters the GOST font has no glyph for (lower case, Latin, ...)."""
        missing = {
            char
            for char in text
            if char not in engine.WIDTHS and char not in "\r\n\t"
        }
        return sorted(missing)

    @staticmethod
    def write_file(path, code):
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(code)


def run():
    # Must be in place before QApplication, which may already emit messages.
    QtCore.qInstallMessageHandler(qt_message_handler)

    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("GOST 26.008-85 Engraver")
    app.setApplicationDisplayName("GOST 26.008-85 Engraver")
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(run())
