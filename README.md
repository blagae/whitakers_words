# Whitaker's Words

## Project history

`whitakers_words` is a port of William Whitaker's original Ada code to Python for future maintenance and improvement.
You can find the current state of development that started with the original Whitaker's Words, written in Ada, on
[Martin Keegan's Github repository](https://github.com/mk270/whitakers-words).
More information about William Whitaker and the Words program is available there.  

## Changes since fork

This specific project is a repurposed fork of the initial effort by [Luke Hollis](https://github.com/ArchimedesDigital/open_words).
A few functions have been deleted:

* the promise of english-to-latin lookups has been abandoned
* multi-word lookups are no longer possible

Other changes include:

* inefficient dictionary loops (`O(n)`) have been replaced by lookups (`O(log n)`)
* `Parse` has been renamed to `Parser`
* the response formatting logic has moved to its own module, named `formatter`
* tests were added
* `format_data` has been renamed to `generator`. It is now a data feeding program which reads Whitaker's file lists into Python dictionaries and lists
* `generator` logic is called upon installation of the egg (`python setup.py install`)

## Project status

This project is far from production-ready. Known issues are:

* `prefixes.py` and `suffixes.py` are not being used in program logic
* adverbial forms of comparatives and superlatives are analyzed completely wrong
* `INCLECTS.LAT` has two sets of two numbers to indicate declination etc; the only one I use right now is the first one.

There are certainly more problem to be found. Feel free to create Github issues for any error you encounter.

## License

This project is under the MIT license. The license was taken over from the
[Luke Hollis project](https://github.com/ArchimedesDigital/open_words).

# Usage

To use the standard dictionary lookup, use the `Parser` class as follows:

```
from whitakers_words.parse import Parser
parser = Parser()
parser.parse("regis")
```

The return value is a Python dictionary, easily wrapped to JSON, structured as followed:
```
{
  "word": "regis",
  "defs": [
    { "orth": [ "rex", "reg" ],
      "senses": [ "king" ],
      "infls": [
        { "stem": "reg",  "ending": "is", "pos": "noun", "decl": 3,
          "form": { "declension": "accusative", "number": "plural", "gender": "masculine" }
        }]
    },
    { "orth": [ "rego", "regere", "rexi", "rectus" ],
      "senses": [ "rule, guide", "manage, direct" ],
      "infls": [
        { "stem": "reg", "ending": "is", "pos": "verb", "decl": 3,
          "form": { "tense": "present", "voice": "active", "mood": "indicative", "person": 2, "number": "singular" }
        }]
    }
  ]
}
```

## Install instructions

If you have cloned the repository, you can just use

    $ python setup.py install

Otherwise, you will need to install from the Github repo, because there is no PyPi package for this project.

    $ pip install git+https://github.com/blagae/whitakers_words.git#egg=whitakers_words

If you have a requirements file, then this is a valid format for the dependency:

    git+git://github.com/blagae/whitakers_words.git#egg=whitakers_words

## Test instructions

The tests use the standard Python `unittest` framework. All tests are in the `whitakers_words.tests` module.
You should be able to run them from the command line, without any further config, by just calling:

    $ python -m unittest
