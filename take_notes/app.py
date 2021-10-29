import os

import re

from take_notes.manager import NoteManager

import typer

from rich.console import Console
from rich.table import Table

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
    table = Table()
    table.add_column("Available Notes")
    for topic in topics:
        table.add_row(topic)

    console = Console()
    console.print(table)


@app.command()
def todo(name: str = typer.Option(None, help="Alterative name for the section")):
    """Display the TODO sections"""
    topics = notes.available_notes

    section_name = name if name is not None else "TODO"

    typer.clear()
    table = Table(show_lines=True)
    table.add_column("Note")
    table.add_column(section_name, no_wrap=False)

    total = 0
    for topic in topics:
        lines = notes.search_section(topic, section_name)
        if lines == "":
            continue

        table.add_row(f"[green]{topic}[/green]", lines)

        total += 1

    if total == 0:
        typer.echo(f'No sections named "{section_name}" founds in your notes.')
        raise typer.Exit()

    console = Console()
    console.print(table)

    open_note_prompt()


def open_note_prompt():
    note_to_open = typer.prompt("What note do you want to open?", default="exit")
    if note_to_open != "exit":
        note_to_open = note_to_open.replace("notes open", "").strip()
        open_note(note_to_open)


@app.command()
def grep(keyword: str, size: int = 0):
    """Search all existings notes for the keyword"""
    topics = notes.available_notes

    typer.clear()

    table = Table()
    table.add_column("Note")
    table.add_column(f"Lines with {keyword}")
    for topic in topics:
        lines = notes.search_notes(topic, keyword, size)
        if len(lines) == 0:
            continue

        lines = [replace_all(keyword, line) for line in lines]

        table.add_row(topic, "\n".join(lines))

    if len(table.rows) != 0:
        console = Console()
        console.print(table)

        open_note_prompt()
    else:
        typer.echo(f'Nothing found under "{keyword}".')


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
    table = Table(show_lines=True)
    table.add_column("Topic")
    table.add_column(f"First {n} lines", no_wrap=False)

    for topic in topics:
        if notes.already_exists(topic):
            lines = notes.view_existing_notes(topic, n)
            if lines != "":
                table.add_row(f"[green]{topic}", lines)

    console = Console()
    console.print(table)

    open_note_prompt()


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


@app.command()
def rename(topic: str, new_topic: str):
    """Rename one topic to another"""
    if not notes.already_exists(topic):
        typer.echo(f"{topic} doesn't exist so cannot be moved!")
        raise typer.Exit()

    if notes.already_exists(new_topic):
        typer.echo(
            f"{new_topic} already exists and shouldn't be overwritten with this command. Use `notes delete {new_topic}` first."
        )
        raise typer.Exit()

    notes.rename_note(topic, new_topic)
    typer.echo(f"{topic} was renamed to {new_topic}")
