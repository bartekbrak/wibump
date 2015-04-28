from setuptools import setup
import re
import os


def read_file(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as f:
        return f.read()


def get_module_description(module_init):
    RE_INIT_DOCSTRING = re.compile('"""(?P<description>.*?)"""', flags=re.DOTALL)
    try:
        return RE_INIT_DOCSTRING.match(module_init).group('description')
    except AttributeError:
        raise Exception('Module has no description in init docstring.')


the_module = read_file('wibump.py')
metadata = dict(re.findall("^__([a-z_]+)__ = '([^']+)'$", the_module, re.MULTILINE))
description = get_module_description(the_module)
setup(
    name='wibump',
    author=metadata['author'],
    author_email=metadata['author_email'],
    version=metadata['version'],
    description=description,
    py_modules=['wibump'],
    entry_points={'console_scripts': ['bump=wibump:main']}
)
