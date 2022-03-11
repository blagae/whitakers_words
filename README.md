# Whitaker's Words

## Introduction

`whitakers_words` is a Latin word analysis tool written in Python 3.
Its core is a software library: it takes a single Latin word as input, and it outputs the word's stem, inflection, and meaning.
The output may also contain basic information about the word's syntactic use and/or some other metadata about frequency, semantic field, age, etc.

There is also a command line tool called `whitaker` that can be used on any terminal.

## Project history

`whitakers_words` is a reimplementation of William Whitaker's original project in Python 3.9 for future maintenance and improvement.
You can find the current state of development of the Ada code that started with the original Whitaker's Words,
on [Martin Keegan's Github repository](https://github.com/mk270/whitakers-words).
More information about William Whitaker and the Words program is available there.  

## Changes since fork

This specific project is a repurposed fork of the initial effort by [Luke Hollis](https://github.com/ArchimedesDigital/open_words).
While the project looks very different on the surface, it still uses many parts of the original algorithm.
A number of (proposed) functions have been deleted:

* the promise of english-to-latin lookups has been abandoned
* multi-word lookups are no longer possible

It has also seen significant improvement in usability and performance:

* `format_data` has been renamed to `datagenerator`. It is now a data feeding program which reads Whitaker's file lists into Python dictionaries and lists
* `datagenerator` logic is called upon installation of the project, through `setup.py` or `pip install`
* inefficient dictionary loops (`O(n)`) have been replaced by lookups (`O(log n)`)
* the default output is no longer a JSON dictionary, but rather a hierarchy of Python objects. It can thus be used as a library by a client application.
* tests were added
* a command line tool was added to simulate replicate the original Whitakers Words

## Project status

This project is far from production-ready. Known issues are:

* `prefixes.py` and `suffixes.py` are not being used in program logic right now
* the API does not yet support filtering fully e.g. pre-classical inflections are unsupported
* interrogative pronouns are analyzed terribly wrong

There are certainly many more major problems to be found. Feel free to create Github issues for any error you encounter.

## License

This project is under the MIT license. The license was taken over from the
[Luke Hollis project](https://github.com/ArchimedesDigital/open_words).
The original Whitaker's Words project in Ada had a very 'liberal' license that was ostensibly written by William Whitaker himself;
the canonical MIT license seems to be quite close to the intent Mr. Whitaker had.

# Usage

## Install instructions

The prerequisites are simple: have python 3.9 installed with pip.

If you have cloned the repository, you can just use either one of these options:

    $ python setup.py install

    $ pip install -e .

Otherwise, you will need to install from the Github repo, because there is no PyPi package for this project.

    $ pip install git+https://github.com/blagae/whitakers_words.git#egg=whitakers_words

If you want to use whitakers_words as a dependency, then this is a valid format for adding the project to `requirements.txt`:

    git+git://github.com/blagae/whitakers_words.git#egg=whitakers_words

## Usage as a library in Python code

To use the standard dictionary lookup, use the `Parser` class as follows:

```
from whitakers_words.parser import Parser
parser = Parser()
result = parser.parse("regemque")
```

The resulting value is a `Word` object, structured as follows:

```
Word:
  text: regemque
  forms:
    - enclitic: que
      analyses:
        - lexeme: (rex, regis)
          inflections:
            - root: reg
              affix: em (Accusative Singular Masculine)
          enclitic: que
```

## Command line tool

Since version 0.5, a command line tool called `whitaker` is available when you install the project.
It can be called as follows:

    $ whitaker parse regemque --formatter=yaml

Some caveats when using this tool, as of version 0.6:

* the tool is very basic and does not support a lot of options yet.
* it is not guaranteed that the subcommands will remain the same.

It also supports the original `words` format. Note that as of 0.6, some word types are not fully equivalent to the original WORDS program.

    $ whitaker words regemque
    que                  TACKON
    -que = and (enclitic, translated before attached word); completes plerus/uter;
    reg.em               N      3 1 ACC S M
    rex, regis  N (3rd) M   [XLXAX]
    king


# Development

## virtual environment

You are advised to use `virtualenv` or `venv` when modifying any code. The project currently runs on Python 3.9,
using some improvements of the type hinting system, but it could probably run on older versions as well with minimal modifications.

The folder `venv/` is ignored by the git config, so this name is the suggested name for your virtual environment:

    $ python -m venv venv/

## Test instructions

The tests use the `pytest` framework. All tests are in the `tests` module (which is not included in the distributed library code).
You should be able to run the tests from the command line, from the root folder of the project and without any further config, by just calling:

    $ pytest tests

If that doesn't work, you may need to manually install the project dependencies before:

    $ pip install -r requirements.txt

## Using tox

If you want to run the full QA check of this project, just run tox on the command line while `venv` is active:

    $ tox

This commands runs the tests with `pytest`, checks for PEP8 compliance with `flake8`, and for type hinting consistency with `mypy`.
If everything goes well, the last lines of the output of `tox` will look like this:

> py39: commands succeeded
> flake8: commands succeeded
> mypy: commands succeeded
> congratulations :)

If your tests are failing because the test runner can't find the package `whitakers_words.generated`,
then install the current project as a code dependency (not a package) by using the `-e` option, before retrying:

    $ pip install -e .

## Project metadata

* The program logic is detailed [here](./project_structure.md). Since the project is in flux, some details may be out of date at any given time.
* There are a number of TODO items throughout the code base, but I'll also try and keep the [TODO](./TODO.md) file up to date with more high-level items.

## Roadmap

* Improve current state of project
* Leverage all information in the `DICTLINE.GEN` file
* Compare results to output of the original Whitaker's Words program
* Output to different formats: JSON, YAML, Whitaker's original syntax, ...
* ...
