# Clypher

Clypher is a simple command-line interface application for encrypting and decrypting files.

## Features

- Encrypt and Decrypt files using the command line.
- Batch encryption and decryption.
- Easily extendable with new encryption algorithms.

## Installation

You can install Clypher via `pip`.

```bash

pip install clypher

```

## Usage

Encrypt a file:

```bash

clypher enc <file_path>

```

Decrypt a file:

```bash

clypher dec <file_path>

```

You can also encrypt and decrypt multiple files at the same time:

```bash

clypher enc <file_path1> <file_path2> <file_path3>

clypher dec <file_path1> <file_path2> <file_path3>

```

You can even encrypt the contents of a directory:

```bash

clypher enc ./foo/

```

Or, encrypt everything in said directory recursively:


```bash

clypher enc ./foo/ --recursive

```


To display the list of available commands:

```bash

clypher --help

```

To display more information about a command:

```bash

clypher <command> --help

```

## Documentation

For more information about how Clypher works, check the [documentation](https://maxacan.github.io/clypher).

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
