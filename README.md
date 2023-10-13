# Past Paper Question Extraction 

## Installation

### Mac

Install Poppler:

```$ brew install Poppler```

Install requirements:

```$ pip install -r requirements.txt```

### Linux

Install Poppler:

```$ sudo apt-get install python-poppler```

Install requirements:

```$ pip install -r requirements.txt```

### Windows

*Poppler is not supported on Windows natively, so you will need to use [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)*

Install Poppler on WSL (Ubuntu):

```$ sudo apt-get install python-poppler```


Install requirements:

```pip install -r requirements.txt```


## Usage

- Place Past Papers in `./past-papers`
  - If Past Papers do not have Question numbers at the same distance from the left edge of the page, as they do in CIE 9618, you will need to adjust `col_range = (125, 155)` in `script.py`
  - This also requires the column on the pages only contains question numbers, nothing else (at least no other numbers 1 - 9)
- Run the script e.g. `python3 script.py`

## Notes

- Its not perfect, because all the PDF pages are converted to PNG images, OCR that is applied does not pick up every question 100% of the time
  - Maybe I'll figure something out, but its by an estimate about 90% accurate, only now and then does a question get missed
  - Questions that are 'missed' are still within the quesiton PNGs, just below the quesiton beforehand.   

