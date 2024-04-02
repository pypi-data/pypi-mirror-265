import unittest

from .compact_output import TestCompactOutput
from .debug_output import TestDebugOutput
from .div_shortcut import TestDivShortcut
from .filters import TestFilters
from .haml_tags import TestHamlTags
from .html_tags import TestHtmlTags
from .jinja_tags import TestJinjaTags, TestJinjaTagsCustomPlaceholders
from .syntax import TestSyntax

unittest.main()
