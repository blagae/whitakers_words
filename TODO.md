# What can I do ?

If you see this list and are unsure what you can do to help, add integration tests !
The integration tests are written as a full analysis of one word, checking every result.

They are usually structured like so, which makes them (relatively) easy to understand:

```
def test_regem(self):
    result = self.par.parse("regem")
    self.assertEqual(len(result.forms), 1)
    self.assertEqual(len(result.forms[0].analyses), 1)

    # there is only one entry here, but it's easier to just iterate than to retrieve the element if you don't know the key
    for analysis in result.forms[0].analyses.values():
        self.assertEqual(analysis.lexeme.roots[0], 'rex')
        self.assertEqual(analysis.lexeme.wordType, WordType.N)  # Noun

        self.assertEqual(len(analysis.inflections), 1)
        # if there is more than one inflection for this analysis, look in the tests how we test for similar variants
        inflection = analysis.inflections[0]

        self.assertEqual(inflection.stem, 'reg')
        self.assertEqual(inflection.affix, 'em')
        self.assertEqual(inflection.wordType, WordType.N)
        self.assertTrue(inflection.has_feature(Case.ACC))  # Accusative
        self.assertTrue(inflection.has_feature(Gender.M))  # Masculine
        self.assertTrue(inflection.has_feature(Number.S))  # Singular
```

More tests are always welcome, because:

* If the result is as you expected, then the test you wrote actively prevents bugs on the parts of the logic it traverses
* If you see unexpected results, either you learn something about Latin inflections, or you've discovered a bug
* Once you've discovered a bug, you can try fixing it ! That way, you get to know the code base better
* Once the bug has been fixed, the test you wrote actively prevents the bug from reoccurring

# TODOs in the implementation

## parser

* see if there is a more elegant way to insert the data layer into relevant methods
* decide if class names are OK

## matcher

* decide if using method names is OK
* fix "PACKON" type

## datalayer

* make it more generic (e.g. allow a custom backend)
* do we need the filter() inception ?
* allow filtering on other metadata than frequency
* filtering on frequency should also filter the wordlist to prevent homonymic false positives

# tests

## unit

* unit tests for matcher
* more unit tests for methods that use the datalayer

## integration

* many more tests are needed

## nonfunctional

* write some actual benchmarks including warmup time etc
