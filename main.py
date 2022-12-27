import argparse
import hashlib
import json
import os
from typing import Iterator

from colorama import init, Fore

init(autoreset=True)


def group_files_by_hash(files: Iterator[tuple[str, str]]):
    """
    Group files by hash

    Parameters
    ----------
    files : `list[tuple[str, str]]`
        A list of tuples containing the file hash and file path

    Returns
    -------
    `dict[str, list[str]]`
        A dictionary containing the file hash as the key and a list of file paths as the value
    """
    files_by_hash: dict[str, list[str]] = {}

    # Iterate over the list of tuples
    for file_hash, file_path in files:

        # If the hash is not in the dictionary, add it and create a new list for the file paths
        if file_hash not in files_by_hash:
            files_by_hash[file_hash] = [file_path]
        # Otherwise, append the file path to the existing list
        else:
            files_by_hash[file_hash].append(file_path)

    return files_by_hash


def get_file_hash(file_path: str, chunk_size=10240):
    """
    Get the md5 hash of a file

    Parameters
    ----------
    file_path : `str`
        The path to the file
    chunk_size : `int`
        The size of the chunks to read the file in. Default is 10240 bytes

    Returns
    -------
    `str`
        The md5 hash of the file
    """

    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        # Create an md5 hash object
        hash_obj = hashlib.md5()

        # Read the file in chunks of 10240 bytes

        chunk = f.read(chunk_size)
        while chunk:
            # Update the hash with the chunk of data
            hash_obj.update(chunk)
            chunk = f.read(chunk_size)

        # Get the hexadecimal representation of the hash
        file_hash = hash_obj.hexdigest()

    return file_hash


def get_subdirs_files(recursive: bool,  includeHidden: bool, directories: Iterator[str]):
    """
    Get subdirectories and file paths

    Parameters
    ----------
    recursive : `bool`
        Search subdirectories recursively
    includeHidden : `bool`
        Include hidden files and directories
    directories : `Iterator[str]`
        Directories to search for files

    Returns
    -------
    `tuple`
        A tuple of subdirectories and file paths
    """
    # tuple of directories to ignore
    IGNORE_LIST = (
        'node_modules',
        'venv',
        '__pycache__',
    )

    subdirectories: set[str] = set()
    file_paths: set[str] = set()

    for directory in directories:
        for root, dirs, files in os.walk(directory):

            # all subdirectories
            # for subdir in dirs:
            #     # if recursive is False, stop searching subdirectories
            #     if not recursive and directory != root:
            #         break

            #     # ignore hidden directories
            #     if not includeHidden and subdir.startswith('.'):
            #         continue

            #     # ignore directories from ignore list
            #     if subdir in IGNORE_LIST:
            #         continue

            #     # Add the subdirectory to the list
            #     subdirectories.add(os.path.join(root, subdir))

            # all files
            for file in files:
                # if recursive is False, stop searching subdirectories
                if not recursive and directory != root:
                    break

                # ignore hidden files
                if not includeHidden and file.startswith('.'):
                    continue

                # ignore paths from ignore list
                if any(ignore_value in root for ignore_value in IGNORE_LIST):
                    continue

                # Add the file to the list
                file_paths.add(os.path.join(root, file))

    return iter(subdirectories), iter(file_paths)


def parse_cli_args():
    """
    Parse the command line arguments

    Returns
    -------
    `tuple`
        A tuple of the parsed arguments
    """

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add optional arguments
    parser.add_argument('-i', '--include-hidden', action='store_true', help='include hidden files and directories')
    parser.add_argument('-r', '--recursive', action='store_true', help='search subdirectories recursively')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase output verbosity')

    # Add positional arguments
    parser.add_argument('directories', nargs='+', help='one or more directories to search for duplicate files')

    # Parse the arguments
    args = parser.parse_args()

    # Get the arguments
    recursive: bool = args.recursive
    include_hidden: bool = args.include_hidden
    verbose: int = args.verbose
    directories: Iterator[str] = iter(args.directories)

    # Print the arguments if verbose is greater than 0
    # if verbose > 0:
    print(f'{Fore.YELLOW}Search subdirectories recursively:{args.recursive.__str__():.>20}', end='\n\n')
    print(f'{Fore.YELLOW}Include hidden files and directories:{args.include_hidden.__str__():.>17}', end='\n\n')
    print(f'{Fore.YELLOW}Verbosity:{args.verbose.__str__():.>44}', end='\n\n')
    print(f'{Fore.YELLOW}Selected directories to search for duplicate files:\n  ' +
          '\n  '.join(args.directories).__str__(), end='\n\n')

    return recursive, include_hidden, verbose, directories


def main():
    """
    Main function
    """

    # Parse the command line arguments
    recursive, include_hidden, verbose, directories = parse_cli_args()

    # Get the subdirectories
    subdirectories, file_paths = get_subdirs_files(recursive, include_hidden, directories)
    subdirectories, file_paths = sorted(list(subdirectories)), sorted(list(file_paths))

    # Print the subdirectories and file paths if verbose is greater than 1
    if verbose > 1:
        # print(Fore.YELLOW + 'Subdirectories:\n  ' + '\n  '.join(subdirectories), end='\n\n')
        print(Fore.YELLOW + 'File paths:\n  ' + '\n  '.join(file_paths), end='\n\n')

    # Print the number of subdirectories and file paths
    # print(Fore.YELLOW + 'Total number of subdirectories: ' + len(subdirectories).__str__(), end='\n\n')
    print(Fore.GREEN + f'Total number of files:{len(file_paths).__str__():.>32}', end='\n\n')

    # Get the hash of each file in a list
    file_hashes_with_paths = ((get_file_hash(file_path), file_path) for file_path in file_paths)

    # Group the file paths by hash
    files_by_hash = group_files_by_hash(file_hashes_with_paths)

    # Print the files by hash with json if verbose is greater than 1
    if verbose > 1:
        print(Fore.YELLOW + 'Files by hash:\n' + json.dumps(files_by_hash, indent=2), end='\n\n')

    # Get the number of unique and duplicate files
    unique_len = len(files_by_hash)
    duplicate_len = len(file_paths) - unique_len

    # Print the number of unique and duplicate files
    print(Fore.GREEN + f'Number of unique files:{unique_len.__str__():.>31}', end='\n\n')
    print(Fore.GREEN + f'Number of duplicate files:{duplicate_len.__str__():.>28}', end='\n\n')

    # ignore the files with only one path
    files_by_hash = {hash: paths for hash, paths in files_by_hash.items() if len(paths) > 1}

    # Print the files by hash with json
    print(Fore.GREEN + 'Duplicate files by hash:\n' + json.dumps(files_by_hash, indent=2), end='\n\n')

    # Exit the program
    print(f"{Fore.YELLOW}*For more details, run the code with `-v` or `--verbose` with a value greater than 0")
    print('Exiting program...')


if __name__ == "__main__":
    main()
