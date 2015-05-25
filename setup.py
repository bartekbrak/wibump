from setuptools import setup

setup(
    name='wibump',
    version='1.2.6',
    py_modules=['wibump'],
    install_requires=['GitPython', 'blessings'],
    entry_points={'console_scripts': ['bump=wibump:main']}
)
