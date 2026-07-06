#!/usr/bin/env python
import os
from typing import Optional

import click

from .datalayer import default_database_path
from .formatter import Formatter, JsonFormatter, WordsFormatter, YamlFormatter
from .parser import Parser, Word


@click.group()
def whitaker() -> None:
    """A CLI wrapper for the Parser class in Whitaker's Words."""


@whitaker.command()
@click.option(
    "--frequency", default="C", help="how strict to be in filtering the dictionary"
)
@click.option(
    "--formatter",
    default="json",
    help="the format of the output: json, yaml, or words (the old Whitaker format)",
)
@click.option(
    "--database/--no-database",
    default=None,
    help="look up words in the sqlite database instead of the generated dictionaries"
    " (default: use the database if it has been generated)",
)
@click.argument("word")
def parse(frequency: str, formatter: str, database: Optional[bool], word: str) -> None:
    """Parse a single word with a format of your choice"""
    clz: Formatter
    if formatter.lower() == "words":
        clz = WordsFormatter()
    elif formatter.lower() == "json":
        clz = JsonFormatter()
    elif formatter.lower() == "yaml":
        clz = YamlFormatter()
    else:
        raise ValueError("Value for --formatter must be one of the listed options")
    result = create_parser(frequency, database).parse(word)
    fmt(result, clz)


@whitaker.command()
@click.option(
    "--frequency", default="C", help="how strict to be in filtering the dictionary"
)
@click.option(
    "--database/--no-database",
    default=None,
    help="look up words in the sqlite database instead of the generated dictionaries"
    " (default: use the database if it has been generated)",
)
@click.argument("word")
def words(frequency: str, database: Optional[bool], word: str) -> None:
    """Parse a single word, and use Whitaker's Words formatting for output"""
    result = create_parser(frequency, database).parse(word)
    fmt(result, WordsFormatter())


def create_parser(frequency: str, database: Optional[bool]) -> Parser:
    if database is None:
        database = os.path.exists(default_database_path())
    if database:
        return Parser(frequency=frequency, database=True)
    return Parser(frequency=frequency)


def fmt(word: Word, formatter: Formatter) -> None:
    click.echo(formatter.format_result(word))
