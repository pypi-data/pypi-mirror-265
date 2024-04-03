from setuptools import setup

name = "types-aiofiles"
description = "Typing stubs for aiofiles"
long_description = '''
## Typing stubs for aiofiles

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`aiofiles`](https://github.com/Tinche/aiofiles) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`aiofiles`.

This version of `types-aiofiles` aims to provide accurate annotations
for `aiofiles==23.2.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/aiofiles. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `6d19a17f57762815426942c21d0fadc91aa1e817` and was tested
with mypy 1.9.0, pyright 1.1.356, and
pytype 2024.3.19.
'''.lstrip()

setup(name=name,
      version="23.2.0.20240403",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/aiofiles.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['aiofiles-stubs'],
      package_data={'aiofiles-stubs': ['__init__.pyi', 'base.pyi', 'os.pyi', 'ospath.pyi', 'tempfile/__init__.pyi', 'tempfile/temptypes.pyi', 'threadpool/__init__.pyi', 'threadpool/binary.pyi', 'threadpool/text.pyi', 'threadpool/utils.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
