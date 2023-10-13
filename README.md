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
  - If Past Papers do not have Question numbers at the same distance from the left edge of the page, as they do in CIE 9816, you will need to adjust `col_range = (125, 155)` in `script.py`
  - This also requires the column on the pages only contains question numbers, nothing else (at least no other numbers 1 - 9)
- Run the script e.g. `python3 script.py` 

