# pylint: disable=wrong-import-order,no-value-for-parameter
import click

from pathlib import Path

from .parser import Hamlish

# todo: replace click with argpars
@click.command
@click.option("--destination", "-d", type = Path, default = ".",
	help = "Destination directory for input files")
@click.option("--mode", "-m", type = click.Choice(["indented", "compact", "debug"]),
	default = "indented", help = "Formatting mode for the resulting template")
@click.option("--indent-str", "-i",
	help = "String to use for indents when mode is not set to compact")
@click.argument("files", type = Path, nargs = -1)
def convert(destination: Path, mode: str, indent_str: str, files: tuple[Path]) -> None:
	destination = destination.expanduser().resolve()
	destination.mkdir(exist_ok = True, parents = True)

	parser = Hamlish.new(
		mode = mode,
		indent_string = indent_str
	)

	for path in files:
		path = path.expanduser().resolve()

		if not path.exists():
			click.echo(f"ERROR: Path does not exist: {path}")
			return

		if not path.is_file():
			click.echo(f"ERROR: Path is not a file: {path}")
			return

		with path.open("r", encoding = "utf-8") as fd:
			text = parser.convert_source(fd.read())

		with destination.joinpath(f"{path.stem}.html").open("w", encoding = "utf-8") as fd:
			fd.write(text)

	click.echo(f"Saved templates to {destination}")


convert()
