[![Python Tests](https://github.com/MohamedElashri/ndpath/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/MohamedElashri/ndpath/actions/workflows/tests.yml)

# ndpath

ndpath is a command-line tool for managing and editing the PATH environment variables. It provides an interactive interface to view, add, remove, and reorder directories in your PATH.

## Introduction

ndpath is a Python port of the [pathos](https://github.com/chip/pathos) tool, which is written in Go. As the maintainer of ndpath, my motivation for creating this port is that I don't have sufficient knowledge of Go to contribute to the upstream development of pathos. Therefore, ndpath is intended to be a hard fork rather than a soft fork, allowing for independent development and maintenance.

## Installation

To install ndpath, you need to have Python installed on your system. You can install ndpath using pip:

```bash
pip install ndpath
```

## Usage

To use ndpath, simply run the following command in your terminal:


```
ndpath
```

This will launch the interactive interface of ndpath that will allow you to view, add, remove, and reorder paths in your PATH. You should also source the `.pathos.env` file in your shell configuration file (e.g., `.bashrc`, `.zshrc`, etc.) to load the modified PATH into your shell environment.

```bash
source ~/.pathos.env
```

## Features

ndpath provides the following features:

- View the current list of directories in your `PATH`
- Add new directories to your `PATH`
- Remove directories from your PATH
- Reorder directories in your PATH
- Save changes to your PATH permanently

## Keyboard Shortcuts

ndpath supports the following keyboard shortcuts:

- `q` - Quit the program (you will be prompted to save changes)
- `k` or `↑` - Move the selection cursor up
- `j` or `↓` - Move the selection cursor down
- `o` - Insert a new directory below the selected directory
- `O` - Insert a new directory above the selected directory
- `x` - Delete the selected directory
- `X` - Delete all non-existent directories from your PATH
- `D` - Deduplicate the list of directories in your PATH
- `S` - Manually save changes to your PATH

## Configuration

ndpath stores the modified PATH in a file named `.ndpath.env` in your home directory.
 This file is loaded by ndpath on startup and is updated whenever you save changes to your PATH.

## Contributing

Contributions to ndpath are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

ndpath is released under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgements

ndpath is inspired by and based on the [pathos](https://github.com/chip/pathos) tool. Special thanks to the creators and contributors of pathos for their work.
