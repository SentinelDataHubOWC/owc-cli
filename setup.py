from setuptools import setup

setup(
    name="owcli",
    version='0.1',
    py_modules=['owcli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        owcli=owcli:cli
    ''',
)
