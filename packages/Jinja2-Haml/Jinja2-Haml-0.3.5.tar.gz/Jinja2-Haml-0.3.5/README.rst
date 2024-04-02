========================
Hamlish-Jinja
========================

Overview
========

This extension to jinja makes it possible to use a haml-ish syntax for your jinja templates. It is
implemented as a preprocessor and so it runs only the first time your template is parsed. So it will
not affect the performance of your templates except for the first run.

Forked from `Pitmairen/hamlish-jinja <https://github.com/Pitmairen/hamlish-jinja>`_

Usage
=====

Install
--------

You can install the latest version with pip

::

    pip install git+https://git.barkshark.xyz/barkshark/hamlish-jinja

or

::

    pip install jinja2-haml

Basic Usage
-----------

To use this extension you just need to add it to you jinja environment and use ".haml", ".jhaml", or
".jaml" as an extension for your templates.

.. code-block:: python

    from jinja2 import Environment
    from hamlish_jinja import HamlishExtension

    env = Environment(extensions = [HamlishExtension])


Environment
-----------

*Added in version 0.2.0*

The environment gets extended with a new method ``hamlish_from_string``
which works the same as the standard ``env.from_string`` method, but renders
the template with the hamlish preprocessor.

.. code-block:: haml

    tpl = '''
    %div
        %p
            test
    '''

    env.hamlish_from_string(tpl).render()
