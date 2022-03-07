#!/usr/bin/env python
import click

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
@click.argument("word")
def parse(frequency: str, formatter: str, word: str) -> None:
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
    result = Parser(frequency=frequency).parse(word)
    fmt(result, clz)


@whitaker.command()
@click.option(
    "--frequency", default="C", help="how strict to be in filtering the dictionary"
)
@click.argument("word")
def words(frequency: str, word: str) -> None:
    """Parse a single word, and use Whitaker's Words formatting for output"""
    result = Parser(frequency=frequency).parse(word)
    fmt(result, WordsFormatter())


def fmt(word: Word, formatter: Formatter) -> None:
    click.echo(formatter.format_result(word))
