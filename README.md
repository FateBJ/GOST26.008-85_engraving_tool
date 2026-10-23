# GOST 26.008-85 engraving tool

The tool that allows you to make G-Code files for a Mach-3 engraving machine or a
drawing machine that makes your life easier when you want to engrave some text,
using the GOST 26.008-85 font.

## Requirements

* Python 3.9+
* PyQt5 — `pip install -r requirements.txt`

`pyperclip` is optional: the command-line mode copies the result to the
clipboard when it is installed.

## Graphical interface

```
python app.py
```

Fill in the text, adjust the parameters and press **Generate G-code**
(Ctrl+Enter works too). The program is shown in the preview and copied to the
clipboard. If an output file is given, it is written on generation; otherwise
use **Save to…** to pick a file.

The form is defined in `main.ui`, so it can be opened and edited in Qt Designer.
`app.py` only contains the signal handling and the call into the generator.

## Command line

```
python main.py
```

The prompts ask for the same parameters in the terminal.

## Character set

The 33 capital letters are drawn by the hand-tuned routines in `main.py`.
Everything else comes from `font_data.py`, which holds the centre lines
extracted from the DXF drawings in `font/`, expressed in font units
(1 unit = height/16 mm, so the glyphs scale with the font height):

* lower-case Cyrillic а–я (й included, ё is not in the drawings)
* digits 0–9

Unsupported characters are skipped and listed in the status bar; they take no
space in the layout. The remaining DXF sheets are not one-glyph-per-cell fonts:
`signs_*` are specimen charts of punctuation and mathematical symbols (mixed
sizes, overlapping rows) and `digits_roman` shows numeral *examples* built from
I/V/X rather than separate characters. The Latin and Greek sheets contain only
the letters whose shapes differ from Cyrillic, so they need a fallback table
before they can be used as full alphabets.

`font_data.py` is generated; do not edit it by hand.

