import argparse
from head_require.core import head_require

def main():
    parser = argparse.ArgumentParser(description='Generate requirements.txt based on imported packages in Python files.')
    parser.add_argument('--directory_env', '-de', type=str, default='.venv/', help='Path to the directory environment containing the "Lib/" directory. Default is .venv/')
    parser.add_argument('--directory_project', '-dp', type=str, default='.', help='Path to the directory of your project or the root path of the project. Default is current directory.')
    args = parser.parse_args()

    directory = args.directory_env
    directory_project = args.directory_project

    pkg_manager = head_require(directory, directory_project)
    pkg_manager.head_require_function()

if __name__ == "__main__":
    main()
