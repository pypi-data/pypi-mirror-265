# The process of operation of this library.

1. "List files": This step lists all files in the directory, excluding the `.venv` folder.
2. "Extract imports": This step extracts import statements from Python files (`.py` and `.ipynb`) in the current directory.
3. "Get installed packages": This step retrieves a dictionary of installed packages and their versions.
4. "Get matched packages": This step retrieves a dictionary of matched packages and their versions from imported modules in Python files in the current directory.
5. "Write requirements txt": This step writes the matched packages and their versions to the `requirements.txt` file.



