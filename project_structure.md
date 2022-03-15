# On install

During installation, the `datagenerator` module executes.
This file reads the original data files, which were created by William Whitaker,
into lists and dictionaries that can be used very efficiently by the rest of the program.
The output is stored as large Python files in the `whitakers_words.generated` package.
We generate them on install instead of adding them to version control,
because it is always possible that the format of the generated files changes,
and it's much more intuitive to read the changes in the datagenerator script
than in seeing a thousand random changes in a wall of text.

If you are cloning the project and trying to run the files, first install the package locally:

    (whitakers_words) $ pip install -e .

# Program execution

## Parser

The `Parser` is probably the only entry point users will need.
The default constructor `Parser` will initialise its `DataLayer` with a subset of the full dictionary from the `generated` package.
You can pass the constructor argument `frequency`, which will modify which subset is used:
it will only show results if the word and inflection are common enough to be filtered on this category.

```
parser = Parser(frequency="B")  # analyze using dictionary entries and inflections of frequency A or B
```
**TODO add all metadata modifiers to enums.py**

You can also specify a fully customised dictionary as part of the `DataLayer`,
by using the dictionary's keywords that are used in its initialization.
This is prominently used in the unit tests, to test the API with a "minimal" dictionary.
If you want to do this, then you will have to recreate the data structure of the list(s) and/or dict(s) that you want to override.

## Word

The `Parser` will `parse()` a single word, and create a `Word`, which is a container object with a number of `Form`s.
If the word contains a valid enclitic, then a `Form` is created that separates the enclitic.
In some cases, there may be several `Form`s (e.g. *quoque* can be formed as both *quo* + *que* and a full lexical word from the dictionary).

**TODO is it possible to have multiple enclitics on one word ?**

In the end, only those `Form`s that contain at least one valid analysis are retained.

## Form

The `Form` text is the word without enclitic, and we look for this value in the list of unique forms,
which contains the paradigms of `esse`, `velle`, and other items that cannot easily be fit into a regular paradigm.
If there is a unique form, a simple analysis is created with a `UniqueLexeme` and a (dummy) `UniqueInflection`.
In most cases, however, there is no hit, and we must create a full `Analysis`.

In the end, only those `Analysis` instances that contain at least one valid combination of a `Lexeme` and an `Inflection` are retained in the `Form`.

### Creating and validating an Analysis

At the start, we check in the list called `dictkeys` if the word is available there.
That would mean that a possible analysis is undeclined (with a zero-length `Inflection`).
Then, we iterate over a continuously shorter part of the word to see if both the hypothetical stem part and inflection part exist.
If that happens, we have a possible match - but no decision is made on whether the match is actually valid.

This essential matching step is done in `Form.match_stems_inflections`:
we iterate over the stems and inflections to see whether they actually correlate.
Depending on the word type, the matching is done differently and has different side effects.
The matchers are implemented in the `matcher` module, as is the logic to choose which matcher to use.

## Analysis, Lexeme, and Inflection classes

`Analysis` and `Lexeme` are very simple data containers that pass the information from the dictionary back to the frontend in a more readable way.

`Inflection` is the same, but it will use some extra logic to display the objects in the `enums` module in a more readable way.
