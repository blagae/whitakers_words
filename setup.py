from setuptools import setup, find_namespace_packages

try:
    from whitakers_words.dict_id import WordsIds
    from whitakers_words.dict_line import WordsDict
    from whitakers_words.addons import LatinAddons
    from whitakers_words.stem_list import Stems
    from whitakers_words.uniques import Uniques
    from whitakers_words.inflects import Inflects
except ModuleNotFoundError:
    from whitakers_words.format_data import reimport_all_dicts

    reimport_all_dicts()
    from whitakers_words.dict_id import WordsIds
    from whitakers_words.dict_line import WordsDict
    from whitakers_words.addons import LatinAddons
    from whitakers_words.stem_list import Stems
    from whitakers_words.uniques import Uniques
    from whitakers_words.inflects import Inflects

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
    name='whitakers_words',
    packages=list(["whitakers_words.files", *find_namespace_packages(include=["whitakers_words", "whitakers_words.*"], exclude=["whitakers_words.tests","whitakers_words.tests.*"])]),
    url='https://github.com/blagae/whitakers_words',
    version='0.1.1',
    zip_safe=True,
    package_data={"whitakers_words.data": ["*.*"]}
)
