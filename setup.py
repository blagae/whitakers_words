from setuptools import setup, find_namespace_packages

try:
    from open_words.dict_id import WordsIds
    from open_words.dict_line import WordsDict
    from open_words.addons import LatinAddons
    from open_words.stem_list import Stems
    from open_words.uniques import Uniques
    from open_words.inflects import Inflects
except ModuleNotFoundError:
    from open_words.format_data import reimport_all_dicts

    reimport_all_dicts()
    from open_words.dict_id import WordsIds
    from open_words.dict_line import WordsDict
    from open_words.addons import LatinAddons
    from open_words.stem_list import Stems
    from open_words.uniques import Uniques
    from open_words.inflects import Inflects

setup(
    author='Archimedes Digital',
    author_email='root@archimedes.digital',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ],
    description=(''),
    # find actual keywords in future
    keywords=['literature', 'philology', 'text processing', 'archive'],
    license='MIT',
    long_description="""Open Words is a port of William Whitaker's 'Whitaker's Words' original Ada code to Python so that it may continue to be useful to Latin students and philologists for years to come.""",
    name='open_words',
    packages=list(["open_words.files", *find_namespace_packages(include=["open_words", "open_words.*"], exclude=["open_words.tests","open_words.tests.*"])]),
    url='https://github.com/blagae/open_words',
    version='0.1.1',
    zip_safe=True,
    package_data={"open_words.data": ["*.*"]}
)
