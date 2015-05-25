from setuptools import setup
setup(
    name='wibump',
    version='1.2.3',
    py_modules=['wibump'],
    install_requires=['GitPython'],
    entry_points={'console_scripts': ['bump=wibump:main']}
)
