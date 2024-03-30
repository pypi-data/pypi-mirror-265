![CI/CD](https://github.com/software-students-spring2024/3-python-package-exercise-snailman/actions/workflows/build.yml/badge.svg)

## Description

[wordutilities](https://test.pypi.org/project/wordutilities/): A Python package that provides some functions related to English-language words.

## Install package:

1. Use the following command to install the package: `pip install -i https://test.pypi.org/simple/ wordutilities`.
2. Create a Python program file that imports the package and uses it, e.g. `from wordutilities import wordutilities`.
3. Here are some examples as to how to call each function in the package:
    - `is_anagram("abc","cba")`
    - `scramble("abc")`
    - `anagrams("abc")`
    - `is_blank("abc")`
    - `permutations("hello")`
    - `select_random_sentence()`
    - `select_random_most_common_word()`
    - `fill_blanks()`
5. Run the python program.

### Function documentation:

#### [Usage examples](sample.py)

#### `is_anagram(word1, word2)`
Parameters: `word1` and `word2` are strings

Return value: a boolean

`is_anagram` takes as input two strings of characters and determines if they are anagrams of each other; that is, whether you can rearrange the characters in one to get the other.

#### `scramble(word)`
Parameters: `word` is a string

Return value: a string

`scramble` takes as input a string of characters and permutes these characters into a random order, before returning this new scrambled string

#### `anagrams(word)`
Parameters: `word` is a string (should only contain English letters)

Return value: a sorted list of strings

`anagrams` takes as input a string of letters and returns all English words which anagram to those letters

#### `anagrams_blank(word)`
Parameters: `word` is a string (should only contain English letters)

Return value: a sorted list of strings

`anagrams_blank` takes as input a string of letters and returns all English words which anagram to those letters plus one wild letter (akin to a scrabble blank).  For example, `anagrams_blank('hell')` would return a list containing the words 'hello', 'hells', and 'shell'.

#### `permutations(word)`
Parameters: `word` is a string

Return value: an unsorted list of strings

`permutations` takes as input a string of characters and returns a list of all possible permutations of those characters.   This list does not contain repeated permutations.  Users should note permutations grow according to the factorial function which will make this function slow for large strings.

### `select_random_sentence()`
Parameters: None

Return value: a string

Generates and returns a random sentence from a list of predefined sentences

### `select_random_most_common_word()`
Parameters: None

Return value: a string

Generates and returns a random word from a predefined list of the 20 most common words

### `fill_blanks()`
Paramenters: None

Return value: None

Selects a random sentence and replaces a word with a blank. User must guess out of three options the correct answer to fill in the blank. They will be prompted to try again until they either get the correct answer or quit.

## Contributing

### Set up virtual environment:

1. Install [pipenv](https://github.com/nyu-software-engineering/python-package-example?tab=readme-ov-file) if not already installed.
2. Clone the repository.
3. Run `pipenv shell` in your cloned repository.


### Install dependencies:

Run `pipenv install` in your virtual environment.

### Build package:

1. Run `python -m build` in the directory where `pyproject.toml` is located.
2. Verify that the built .tar archive has the correct contents using `tar --list -f dist/wordutilities-[version number].tar.gz`


### Test package:

1. Install pytest
2. Run `python3 -m pytest` in the project directory.

## Teammates

* [Corina Luca](https://github.com/CorinaLucaFocsan)
* [Jakob Hablitz](https://github.com/jsh9965)
* [Josckar Palomeque-Elias](https://github.com/josckar)
* [Stella Zhang](https://github.com/qq3173732005)
