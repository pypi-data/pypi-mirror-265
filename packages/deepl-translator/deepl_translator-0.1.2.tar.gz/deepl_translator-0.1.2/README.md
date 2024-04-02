# deepl_translator

`deepl_translator` is a simple command-line tool that uses the DeepL API (free version) to translate text between English and Japanese. This tool takes text from standard input and outputs the translation to standard output.

## Features

- Supports translation from English to Japanese and vice versa
- Easy to use from the command line
- Simple API key configuration through a `.env` file

## Prerequisites

- Python 3.x
- pip (Python's package manager)

## Installation

Use the following command to install `deepl_translator`:

```bash
pip install git+https://yourrepository.com/deepl_translator.git
```

> Note: Replace the above URL with the URL of the Git repository hosting this package.

## API Key Configuration

Before using `deepl_translator`, you need to obtain a free API key from DeepL API and configure it in a `.env` file as follows:

1. Create a free account on DeepL API and obtain an API key [here](https://www.deepl.com/pro#developer).
2. Create a `.env` file in the root directory of the project.
3. Add the following content to the `.env` file, replacing `YOUR_API_KEY` with your actual API key:

```makefile
DEEPL_API_KEY=YOUR_API_KEY
```

## Usage

Use `deepl_translator` from the command line to translate a text file:

```bash
cat input.txt | deepl -t [target_language] > output.txt
```

Here, `[target_language]` specifies the target language for translation. The options are as follows:

- `j` or `japanese`: Translate to Japanese
- `e` or `english`: Translate to English

For example, to translate an English text file to Japanese:

```bash
cat input.txt | deepl -t j > output.txt
```

## License

This project is published under the MIT License.

## Contributions

If you would like to contribute, please send a pull request or report an issue. We appreciate all contributions!
