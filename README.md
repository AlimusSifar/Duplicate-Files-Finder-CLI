# Duplicate Files Finder via CLI

This CLI application is a tool for finding any type of duplicate files in one or more directories. It allows the user to specify the directories to search and whether to search recursively in subdirectories. It then generates a list of all the files in the specified directories and their subdirectories, and groups the files by their hash to identify duplicates. The app then outputs a list of the duplicate files, along with the number of duplicates found and the total size of the duplicates. This can be useful for finding and removing unnecessary copies of files to free up disk space.

## Usage

### Requirements

```toml
colorama = "^0.4.6"  # for colored outputs in the terminal
```

> Either execute `pip install -r requirements.txt` or execute `poetry install` in the repository directory.

### Replit.com

> Fork the [Repl](https://replit.com/@AlimusSifar/Duplicate-Files-Finder-CLI) and open the replit `shell`. Then execute the CLI commands. By default the help command will be displayed if you run directly using the `Run` button in replit.

```md
main.py [-h] [-i] [-r] [-v] directories [directories ...]

positional arguments:
  directories           one or more directories to search for duplicate files

optional arguments:
  -h, --help            show this help message and exit
  -i, --include-hidden  include hidden files and directories
  -r, --recursive       search subdirectories recursively
  -v, --verbose         increase output verbosity
```

## Example

A sample directory structure using `tree /F` in windows `cmd`; Argument `/F` includes all files:

```txt
E:\\tutorials
│   New Text Document.txt
│
└───ML-basic
    │   New Rich Text Document.rtf
    │   New Text Document.txt
    │
    └───Machine-Learning-From-Scratch
        ├───01-KNN
        │       KNN.py
        │       train.py
        │
        └───02-Linear-Regression
                LinearRegression.py
                train.py
```

> Executing the command `python main.py -r E:\tutorials` from the repository directory.

### Output

```terminal
Search subdirectories recursively:..............True

Include hidden files and directories:..........False

Verbosity:.........................................0

Selected directories to search for duplicate files:
  E:\tutorials

Total number of files:.............................7

Number of unique files:............................6

Number of duplicate files:.........................1

Duplicate files by hash:
{
  "d41d8cd98f00b204e9800998ecf8427e": [
    "E:\\tutorials\\ML-basic\\New Text Document.txt",
    "E:\\tutorials\\New Text Document.txt"
  ]
}

*For more details, run the code with `-v` or `-vv` etc.
```
