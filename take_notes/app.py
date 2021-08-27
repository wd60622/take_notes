import os

import re

from take_notes.manager import NoteManager

import typer

from typing import List, Optional

app = typer.Typer()

notes = NoteManager()

@app.command()
def list():
    """List the available notes"""
    if notes.no_notes:
        typer.echo("There are no notes. Create with (create) command.")
        raise typer.Exit()

    topics = notes.available_notes
    for topic in topics:
        typer.echo(f"- {topic}")

@app.command()
def grep(keyword: str):
    """Search all existings notes for the keyword"""
    topics = notes.available_notes

    typer.clear()
    for topic in topics:
        lines = notes.search_notes(topic, keyword)
        if len(lines) == 0:
            continue
        typer.secho(f"--- {topic} ---", fg=typer.colors.GREEN)

        lines = [replace_all(keyword, line) for line in lines]
        for line in lines[:-1]:
            typer.echo("keyword found:")
            typer.echo(line)
            typer.echo()

        typer.echo("keyword found:")
        typer.echo(lines[-1])

        typer.echo()

def replace_all(keyword, line):
    wordlen = len(keyword)
    locations = [m.start() for m in re.finditer(keyword.lower(), line.lower())]

    for start in locations:
        keyword_case = line[start:start + wordlen]
        line = line.replace(keyword_case, typer.style(keyword_case, fg=typer.colors.RED))

    return line

@app.command()
def view(topics: Optional[List[str]] = typer.Argument(None, help="The topic(s) to view"), n: int = 5):
    """View the topic(s)"""
    if len(topics) == 0:
        if notes.no_notes:
            raise typer.Exit()

        topics = notes.available_notes

    typer.clear()
    for topic in topics:
        if notes.already_exists(topic):
            lines = notes.view_existing_notes(topic, n)
            if lines != "":
                typer.secho(f"--- {topic} ---", fg=typer.colors.GREEN)
                typer.echo(lines)
                typer.echo()

@app.command()
def create(topics: List[str] = typer.Argument(..., help="The topic to create")):
    """Create new topic(s)"""
    for topic in topics:
        if notes.already_exists(topic):
            typer.echo(f"The note on {topic} already exists. Open with (open) command.")
        else:
            notes.create_new_notes(topic)
            typer.echo(f"The note {topic} was created.")


@app.command()
def open(topic: str = typer.Argument(..., help="The topic to open")):
    """Open existing topic"""
    if not notes.already_exists(topic):
        typer.echo("This note doesn't exists. Create with (create) command.")
        raise typer.Exit()

    notes.open_existing_notes(topic)


@app.command()
def delete(topics: List[str] = typer.Argument(..., help="The topic to delete")):
    """Delete existing topic(s)"""
    for topic in topics:
        if notes.already_exists(topic):
            notes.delete_existing_notes(topic)
            typer.echo(f"{topic} was deleted")
