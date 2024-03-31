from setuptools import setup

name = "types-cffi"
description = "Typing stubs for cffi"
long_description = '''
## Typing stubs for cffi

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`cffi`](https://foss.heptapod.net/pypy/cffi) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`cffi`.

This version of `types-cffi` aims to provide accurate annotations
for `cffi==1.16.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/cffi. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `027115e6249f17f9dee2c0372c4609335a1b9e7d` and was tested
with mypy 1.9.0, pyright 1.1.356, and
pytype 2024.3.19.
'''.lstrip()

setup(name=name,
      version="1.16.0.20240331",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/cffi.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-setuptools'],
      packages=['_cffi_backend-stubs', 'cffi-stubs'],
      package_data={'_cffi_backend-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed'], 'cffi-stubs': ['__init__.pyi', 'api.pyi', 'backend_ctypes.pyi', 'cffi_opcode.pyi', 'commontypes.pyi', 'cparser.pyi', 'error.pyi', 'ffiplatform.pyi', 'lock.pyi', 'model.pyi', 'pkgconfig.pyi', 'recompiler.pyi', 'setuptools_ext.pyi', 'vengine_cpy.pyi', 'vengine_gen.pyi', 'verifier.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
