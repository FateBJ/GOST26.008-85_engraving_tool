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
