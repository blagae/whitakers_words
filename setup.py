from setuptools import find_namespace_packages, setup

try:
    from whitakers_words.data.addons import addons  # noqa: F401
    from whitakers_words.generated.wordkeys import wordkeys  # noqa: F401
    from whitakers_words.generated.wordlist import wordlist  # noqa: F401
    from whitakers_words.generated.inflects import inflects  # noqa: F401
    from whitakers_words.generated.stems import stems  # noqa: F401
    from whitakers_words.generated.uniques import uniques  # noqa: F401
except ModuleNotFoundError:
    from whitakers_words.datagenerator import generate_all_dicts
    generate_all_dicts()

setup(
    author='Benoit Lagae',
    author_email='benoit.lagae@hotmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.9',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ],
    description=(''),
    # find actual keywords in future
    keywords=['literature', 'philology', 'text processing', 'archive'],
    license='MIT',
    long_description="""Whitaker's Words is a port of William Whitaker's 'Whitaker's Words' original Ada code to Python
    so that it may continue to be useful to Latin students and philologists for years to come.""",
    name='whitakers_words',
    packages=list(["whitakers_words.generated",
                  *find_namespace_packages(include=["whitakers_words", "whitakers_words.*"])]),
    url='https://github.com/blagae/whitakers_words',
    version='0.5.0',
    zip_safe=False,
    package_data={'whitakers_words': ['py.typed'], "whitakers_words.data": ["*.*"]}
)
