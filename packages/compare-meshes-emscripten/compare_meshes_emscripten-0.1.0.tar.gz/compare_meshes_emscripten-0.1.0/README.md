# compare-meshes-emscripten

[![PyPI version](https://badge.fury.io/py/compare-meshes-emscripten.svg)](https://badge.fury.io/py/compare-meshes-emscripten)

Compare meshes and polydata for regression testing. Emscripten implementation.

This package provides the Emscripten WebAssembly implementation. It is usually not called directly. Please use the [`compare-meshes`](https://pypi.org/project/compare-meshes/) instead.


## Installation

```sh
import micropip
await micropip.install('compare-meshes-emscripten')
```

## Development

```sh
pip install hatch
hatch run download-pyodide
hatch run test
```
