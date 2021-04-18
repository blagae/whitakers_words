# What can I do ?

If you see this list and are unsure what you can do to help, add integration tests !
The integration tests are written as a full analysis of one word, checking every result.

They are usually structured like so, which makes them (relatively) easy to understand:

```
def test_regem(self):
    result = self.par.parse("regem")
    self.assertEqual(len(result.forms), 1)
    self.assertEqual(len(result.forms[0].analyses), 1)

    # there is only one entry, but it's easier to just iterate than to retrieve the element if you don't know the key
    for key, analysis in result.forms[0].analyses.items():
        self.assertEqual(analysis.lexeme.roots[0], 'rex')
        self.assertEqual(analysis.lexeme.wordType, WordType.N)

        self.assertEqual(len(analysis.inflections), 1)
        inflection = analysis.inflections[0]  # if there is more than one inflection for this analysis, look in the tests how we test for similar variants

        self.assertEqual(inflection.stem, 'reg')
        self.assertEqual(inflection.affix, 'em')
        self.assertEqual(inflection.wordType, WordType.N)
        self.assertTrue(inflection.has_feature(Case.ACC))
        self.assertTrue(inflection.has_feature(Number.S))
        self.assertTrue(inflection.has_feature(Gender.C))
```

More tests are always welcome, because:

* If the result is as you expected, then the test you wrote actively prevents bugs on the parts of the logic it traverses
* If you see unexpected results, either you learn something about Latin inflections, or you've discovered a bug
* Once you've discovered a bug, you can try fixing it ! That way, you get to know the code base better
* Once the bug has been fixed, the test you wrote actively prevents the bug from reoccurring

# TODOs in the implementation

## parser

* create shortcut for undeclined words, so that we don't need to check 60+ empty declensions for each word
* see if there is a more elegant way to insert the data layer into relevant methods
* decide if class names are OK

## matcher

* decide if using method names is OK
* do we need the lambda
* fix pronoun matching (use pronoun types from enums ?)

## generator

* clean up the entire file

## formatter

* rewrite JSON output module from scratch

## datalayer

* do we need the filter() inception ?
* allow filtering on other metadata than frequency

## enums

* add more types of metadata and word subtypes (and integrate them into the code base)

# tests

## unit

* unit tests for matcher
* more unit tests for methods that use the datalayer

## integration

* fix dummy tests in integration
* many more tests are needed

## nonfunctional

* write some actual benchmarks including warmup time etc
