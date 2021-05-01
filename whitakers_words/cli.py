#!/usr/bin/env python
import click

from whitakers_words.parser import Parser


@click.group()
def whitaker() -> None:
    """A CLI wrapper for the Parser class in Whitaker's Words."""


@whitaker.command()
@click.option('--frequency', default='C', help='how strict to be in filtering the dictionary')
@click.argument('word')
def parse(frequency: str, word: str) -> None:
    result = Parser(frequency=frequency).parse(word)
    for val in result.forms:
        click.echo(val)
