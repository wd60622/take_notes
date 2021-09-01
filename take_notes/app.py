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

    typer.clear()
    topics = notes.available_notes
    for topic in topics:
        typer.echo(f"- {topic}")


@app.command()
def todo(name: str = typer.Option(None, help="Alterative name for the section")):
    """Display the TODO sections"""
    topics = notes.available_notes

    section_name = name if name is not None else "TODO"

    typer.clear()
    total = 0
    for topic in topics:
        lines = notes.search_section(topic, section_name)
        if lines == "":
            continue

        typer.secho(f"{section_name} --- {topic}", fg=typer.colors.GREEN)
        typer.echo(lines)

        typer.echo()

        total += 1

    if total == 0:
        typer.echo(f"No {section_name} sections founds in your notes.")
        raise typer.Exit()

    note_to_open = typer.prompt("What note do you want to open?", default="exit")
    if note_to_open != "exit":
        open_note(note_to_open)


@app.command()
def grep(keyword: str, size: int = 0):
    """Search all existings notes for the keyword"""
    topics = notes.available_notes

    typer.clear()
    for topic in topics:
        lines = notes.search_notes(topic, keyword, size)
        if len(lines) == 0:
            continue
        typer.secho(f"--- {topic} ---", fg=typer.colors.GREEN)

        lines = [replace_all(keyword, line) for line in lines]
        for line in lines[:-1]:
            typer.echo(line)
            typer.echo()

        typer.echo(lines[-1])

        typer.echo()


def replace_all(keyword, line):
    wordlen = len(keyword)
    locations = [m.start() for m in re.finditer(keyword.lower(), line.lower())]

    for start in locations:
        keyword_case = line[start : start + wordlen]
        line = line.replace(
            keyword_case, typer.style(keyword_case, fg=typer.colors.RED)
        )

    return line


@app.command()
def view(
    topics: Optional[List[str]] = typer.Argument(None, help="The topic(s) to view"),
    n: int = 5,
):
    """View the topic(s)"""
    if len(topics) == 0:
        if notes.no_notes:
            raise typer.Exit()
        else:
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
    open_note(topic)


def open_note(topic):
    if not notes.already_exists(topic):
        closest_note = notes.closest_note(topic)
        if closest_note != "":
            typer.echo(f"This note doesn't exist. Did you mean {closest_note}?")
        else:
            typer.echo("This note doesn't exist. Create with the (create) command.")
        raise typer.Exit()

    notes.open_existing_notes(topic)


@app.command()
def delete(topics: List[str] = typer.Argument(..., help="The topic to delete")):
    """Delete existing topic(s)"""
    for topic in topics:
        if notes.already_exists(topic):
            notes.delete_existing_notes(topic)
            typer.echo(f"{topic} was deleted")
