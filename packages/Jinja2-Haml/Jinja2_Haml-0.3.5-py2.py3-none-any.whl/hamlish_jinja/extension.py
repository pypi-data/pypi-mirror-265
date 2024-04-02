from __future__ import annotations

import re
import typing

from os.path import splitext
from jinja2 import TemplateSyntaxError, nodes as Nodes
from jinja2.environment import Template
from jinja2.ext import Extension

from .exception import TemplateIndentationError
from .parser import Hamlish, Output, OutputMode

if typing.TYPE_CHECKING:
	from collections.abc import MutableMapping
	from jinja2 import Environment
	from jinja2.nodes import Node
	from jinja2.parser import Parser
	from typing import Any, Type


begin_tag_m = re.compile(r"\{%\-?\s*haml.*?%\}")
end_tag_m = re.compile(r"\{%\-?\s*endhaml\s*\-?%\}")


class HamlishExtension(Extension):  # pylint: disable=abstract-method
	"An extension for Jinja2 that adds support for HAML-like templates."


	def __init__(self, environment: Environment):
		Extension.__init__(self, environment)

		environment.extend(
			hamlish_file_extensions = (".haml", ".jhaml", ".jaml"),
			hamlish_indent_string = "    ",
			hamlish_newline_string = "\n",
			hamlish_debug = False,
			hamlish_enable_div_shortcut = True,
			hamlish_from_string = self.from_string,
			hamlish_filters = None,
			hamlish_mode = OutputMode.COMPACT,
			hamlish_set_mode = self.set_mode
		)


	def preprocess(self, source: str, name: str | None, filename: str | None = None) -> str:
		"""
			Transpile a Hamlish template into a Jinja template

			:param source: Full text source of the template
			:param name: Name of the template
			:param filename: Path to the template
			:raises TemplateSyntaxError: When the template cannot be parsed
		"""

		if name is None or splitext(name)[1] not in self.environment.hamlish_file_extensions: # type: ignore
			return source

		h = self.get_preprocessor(self.environment.hamlish_mode) # type: ignore

		try:
			return h.convert_source(source)

		except (TemplateSyntaxError, TemplateIndentationError) as e:
			raise TemplateSyntaxError(e.message, e.lineno, name, filename) from None # type: ignore


	def get_preprocessor(self, mode: OutputMode) -> Hamlish:
		"""
			Gets the preprocessor

			:param mode: Output format to use
			:raises ValueError: When an invalid mode is specified
		"""

		mode = OutputMode.parse(mode)
		placeholders = {
			"block_start_string": self.environment.block_start_string,
			"block_end_string": self.environment.block_end_string,
			"variable_start_string": self.environment.variable_start_string,
			"variable_end_string": self.environment.variable_end_string}

		if mode == OutputMode.COMPACT:
			output = Output(
				indent_string = "",
				newline_string = "",
				**placeholders # type: ignore
			)

		elif mode == OutputMode.DEBUG:
			output = Output(
				indent_string = "    ",
				newline_string = "\n",
				debug = True,
				**placeholders # type: ignore
			)

		else:
			output = Output(
				indent_string = self.environment.hamlish_indent_string, # type: ignore
				newline_string = self.environment.hamlish_newline_string, # type: ignore
				debug = self.environment.hamlish_debug, # type: ignore
				**placeholders # type: ignore
			)

		return Hamlish(
			output,
			self.environment.hamlish_enable_div_shortcut, # type: ignore
			self.environment.hamlish_filters # type: ignore
		)


	def set_mode(self, value: OutputMode | str) -> None:
		"""
			Set the output mode to use when preprocessing templates

			:param value: Output format to use
			:raises ValueError: When a string is provided and connot be parsed into a
				:class:`OutputMode` value
		"""

		self.environment.hamlish_mode = OutputMode.parse(value) # type: ignore


	def from_string(self,
					source: str,
					name: str | None = None,
					global_vars: MutableMapping[str, Any] | None = None,
					template_class: Type[Template] = Template) -> Template:

		global_vars = self.environment.make_globals(global_vars)
		cls = template_class or self.environment.template_class
		template_name = name or "hamlish_from_string"

		if self.environment.hamlish_file_extensions: # type: ignore
			template_name += self.environment.hamlish_file_extensions[0] # type: ignore

		else:
			template_name += ".haml"

		return cls.from_code(
			self.environment,
			self.environment.compile(source, template_name),
			global_vars,
			None
		)


class HamlishTagExtension(HamlishExtension):
	"""
		An extension for Jinja2 that adds a ``{% haml %}`` tag to use the syntax supported by
		:class:HamlishExtension: in an HTML template.
	"""

	tags = set(["haml"])


	def _get_lineno(self, source: str) -> int:
		matches = re.finditer(r"\n", source)

		if matches:
			return len(tuple(matches))

		return 0


	def parse(self, parser: Parser) -> list[Node] | Node:
		"""
			Parse all ``haml`` blocks in a Jinja template
		"""
		haml_data = parser.parse_statements(("name:endhaml",))
		parser.stream.expect("name:endhaml")

		return [
			Nodes.Output([haml_data])
		]


	def preprocess(self, source: str, name: str | None, filename: str | None = None) -> str:
		"""
			Transpile a Hamlish block

			:param source: Full text source of the template
			:param name: Name of the template
			:param filename: Path to the template
			:raises TemplateSyntaxError: When the template cannot be parsed
		"""

		ret_source = ""
		start_pos = 0

		while True:
			tag_match = begin_tag_m.search(source, start_pos)

			if tag_match:
				end_tag = end_tag_m.search(source, tag_match.end())

				if not end_tag:
					raise TemplateSyntaxError(
						"Expecting 'endhaml' tag",
						self._get_lineno(source[:start_pos])
					)

				haml_source = source[tag_match.end():end_tag.start()]
				h = self.get_preprocessor(self.environment.hamlish_mode) # type: ignore

				try:
					ret_source += source[start_pos:tag_match.start()]
					ret_source += h.convert_source(haml_source)

				except (TemplateSyntaxError, TemplateIndentationError) as e:
					raise TemplateSyntaxError(e.message, e.lineno, name, filename) from None # type: ignore

				start_pos = end_tag.end()

			else:
				ret_source += source[start_pos:]
				break

		return ret_source
