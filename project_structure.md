# Project structure

## On install

During installation, the `generator` module executes. This file reads the original data files, which were created by William Whitaker,
into lists and dictionaries that can be used very efficiently by the rest of the program.
The output is stored as large Python files in the `whitakers_words.generated` package.
We generate them on install instead of adding them to version control, because it is always possible that the format of the generated files changes,
and it's much more intuitive to do this in generator code than just in a big wall of text.

If you are cloning the project and trying to run the files, first install the package locally:

    (whitakers_words) $ python setup.py install

## Program execution

### Parser

The `Parser` is probably the only entry point users will need. You can pass it the argument `frequency`, which will modify the results: it will only
show results if the word is common enough to be filtered on this category. **TODO add all metadata modifiers to enums.py**

