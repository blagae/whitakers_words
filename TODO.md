# List of TODOs

If you see this list and are unsure what you can do, add integration tests !

More tests are always welcome, because:

* if you see unexpected results, either you've learned something or you've discovered a bug
* once you've discovered a bug and it has been fixed, the test actively prevents the bug from reoccurring

## whitakers_words

### parser

* create shortcut for undeclined words, so that we don't need to check 60+ empty declensions for each word
* see if there is a more elegant way to insert the data layer into relevant methods
* decide if class names are OK

### matcher

* decide if using method names is OK
* do we need the lambda
* fix pronoun matching (use pronoun types from enums ?)

### generator

* clean up the entire file

### formatter

* rewrite JSON output module from scratch

### datalayer

* do we need the filter() inception ?
* allow filtering on other metadata than frequency

### enums

* add more types of metadata and word subtypes (and integrate them into the code base)

## tests

### unit

* unit tests for matcher
* more unit tests for methods that use the datalayer

### integration

* fix dummy tests in integration
* many more tests are needed

### nonfunctional

* write some actual benchmarks including warmup time etc
