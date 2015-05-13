from setuptools import setup
setup(
    name='wibump',
    version='1.1.1',
    py_modules=['wibump'],
    entry_points={'console_scripts': ['bump=wibump:main']}
)
