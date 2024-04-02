from setuptools import setup, find_packages

setup(
    name="deepl_translator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'python-dotenv',
    ],
    entry_points='''
        [console_scripts]
        deepl=deepl_translator:translate
    ''',
)
