<div align="center">
  <h1>wc</h1>
  <p>Training copy of the unix program wc</p>
</div>

## Overview

<details>
  <summary>Usage examples</summary>
  <img src="assets/demo_wc1.gif" alt="Help output" />
  <img src="assets/demo_wc2.gif" alt="Word count examples" />
</details>

## Installation

The Makefile uses Clang and GNU libc's `argp` and `argz` interfaces. Run it on a system that provides those headers.

The program is built using make.

```bash
make build
```

## Documentation

### `-c`, `--bytes`

Adds the number of bytes in the file(s) to the program output.

### `-w`, `--words`

Adds the number of words in the file(s) to the program output.

### `-l`, `--lines`

Adds the number of newlines in the file(s) to the program output.

### `-L`, `--max-line-length`

Adds the length of the longest line in the file(s) to the output.

#### To display detailed help:

1. --help
2. --usage
3. -?

## License

The original project README identifies this example as MIT © [Ivan Kovach](https://github.com/Qu1nel/). The repository's [Apache-2.0 license](../../LICENSE) is available at the root.
