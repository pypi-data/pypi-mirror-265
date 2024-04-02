__software__: str = "Hamlish Jinja"
__version__: str = "0.3.5"


try:
	from .exception import TemplateIndentationError
	from .extension import HamlishExtension, HamlishTagExtension
	from .parser import Hamlish, Output, OutputMode

except ModuleNotFoundError:
	pass
