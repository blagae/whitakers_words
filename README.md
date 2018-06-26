# Open Words

## Project history

Open Words is a port of William Whitaker's original Ada code to Python for future maintenance and improvement.
You can find the current state of development that started with the original Whitaker's Words, written in Ada, on
[Martin Keegan's Github repository](https://github.com/mk270/whitakers-words).
More information about William Whitaker and the Words program is available there.  

## Changes since fork

This specific project is a fork of the initial effort by [Luke Hollis](https://github.com/ArchimedesDigital/open_words).
A few functions have been deleted:

* the promise of english-to-latin lookups has been abandoned
* multi-word lookups are no longer possible

Other changes include:

* inefficient dictionary loops (`O(n)`) have been replaced by lookups (`O(log n)`)
* `Parse` has been renamed to `Parser`
* the formatting logic has moved to its own module, named `formatter`
* tests were added
* `format_data` is now a data feeding program which reads Whitaker's file lists into Python dictionaries and lists
* `format_data` logic is called automatically if necessary (should be only once)

## License

This project is under the MIT license. The license was taken over from the
[Luke Hollis project](https://github.com/ArchimedesDigital/open_words).

# Usage

To use the standard dictionary lookup, use the `Parser` class as follows:

```
from open_words.parse import Parser
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
        { "stem": "reg",  "ending": "is", "pos": "noun",
          "form": { "declension": "accusative", "number": "plural", "gender": "masculine" }
        }]
    },
    { "orth": [ "rego", "regere", "rexi", "rectus" ],
      "senses": [ "rule, guide", "manage, direct" ],
      "infls": [
        { "stem": "reg", "ending": "is", "pos": "verb",
          "form": { "tense": "present", "voice": "active", "mood": "indicative", "person": 2, "number": "singular" }
        }]
    }
  ]
}
```
