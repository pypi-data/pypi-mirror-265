import unittest
import jinja2

from hamlish_jinja.extension import HamlishTagExtension
from hamlish_jinja.parser import Hamlish, Output

from .base import TestCase


jinja_env = jinja2.Environment(
	extensions = [
		HamlishTagExtension,
	]
)

class TestHamlTags(TestCase):
	def test_basic(self):
		s = jinja_env.from_string(
"""{% haml %}
%div
    %p
        test
{% endhaml %}
""")
		r = "<div><p>test</p></div>"
		self.assertEqual(s.render(),r)


	def test_multiple(self):
		s = jinja_env.from_string(
"""{% haml %}
%div
    %p
        test
{% endhaml %}
<div>hello</div>
{% haml %}
%div
    %p
        test
{% endhaml %}
""")

		r = "<div><p>test</p></div>\n<div>hello</div>\n<div><p>test</p></div>"
		self.assertEqual(s.render(),r)
