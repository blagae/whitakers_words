# Whitaker's Words

## Project history

`whitakers_words` is a port of William Whitaker's original Ada code to Python for future maintenance and improvement.
You can find the current state of development that started with the original Whitaker's Words, written in Ada, on
[Martin Keegan's Github repository](https://github.com/mk270/whitakers-words).
More information about William Whitaker and the Words program is available there.  

## Changes since fork

This specific project is a repurposed fork of the initial effort by [Luke Hollis](https://github.com/ArchimedesDigital/open_words).
While the project looks very different on the surface, it still uses many parts of the original algorithm.
A number of (proposed) functions have been deleted:

* the promise of english-to-latin lookups has been abandoned
* multi-word lookups are no longer possible

Other changes include:

* `format_data` has been renamed to `generator`. It is now a data feeding program which reads Whitaker's file lists into Python dictionaries and lists
* `generator` logic is called upon installation of the project as a dependency (`python setup.py install`)
* inefficient dictionary loops (`O(n)`) have been replaced by lookups (`O(log n)`)
* tests were added

## Project status

This project is far from production-ready. Known issues are:

* `prefixes.py` and `suffixes.py` are not being used in program logic right now
* there is no longer a response builder which outputs JSON
* `INFLECTS.LAT` has two sets of two numbers to indicate declination etc; the only one I use right now is the first one.
* there is as of yet no way to filter for e.g. pre-classical inflections
* pronoun analysis provides terribly incorrect results

There are certainly many more major problems to be found. Feel free to create Github issues for any error you encounter.

## License

This project is under the MIT license. The license was taken over from the
[Luke Hollis project](https://github.com/ArchimedesDigital/open_words).

# Usage

To use the standard dictionary lookup, use the `Parser` class as follows:

```
from whitakers_words.parser import Parser
parser = Parser()
result = parser.parse("regemque")
```

The resulting value is a `WhitakerWord` object, structured as followed:
```
WhitakerWord:
  - forms:
    enclitic: que
    - analyses:
      lexeme: (rex, regis)
      inflections:
        - em (Accusative Singular Common)
      enclitic: que
```

## Install instructions

If you have cloned the repository, you can just use

    $ python setup.py install

Otherwise, you will need to install from the Github repo, because there is no PyPi package for this project.

    $ pip install git+https://github.com/blagae/whitakers_words.git#egg=whitakers_words

If you have a requirements file, then this is a valid format for the dependency:

    git+git://github.com/blagae/whitakers_words.git#egg=whitakers_words

# Development

## virtualenv

You are advised to use `virtualenv` or `venv` when modifying any code. The project currently runs on Python 3.9,
using some improvements of the type hinting system, but it could probably run on older versions as well.

## Test instructions

The tests use the `pytest` framework. All tests are in the `tests` module (which is not included in the dist).
You should be able to run them from the command line, without any further config, by just calling:

    $ pytest tests

## Using tox

If you want to run the full QA check of this project, just run tox on the command line while `venv` is active

    $ tox

This commands runs the tests, checks for PEP8 compliance with `flake8`, and for type hinting consistency with `mypy`.

## Project metadata

* The program logic is detailed [here](./project_structure.md). Since the project is in flux, this may be somewhat out of date.
* There are a number of TODO items throughout the code base, but I'll also try and keep the [TODO](./TODO.md) file up to date.

## Roadmap

* Improve current state of project
* Leverage all information in the `DICTLINE.GEN` file
* Compare results to output of the original Whitaker's Words program
* Output to JSON again
* ...
