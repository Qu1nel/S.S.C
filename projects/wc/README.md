<div align="center">
  <h1>wc</h1>
  <p>Training copy of the unix program wc</p>
</div>

## Overview

<details>
  <img src="../../../.github/assets/demo_wc1.gif" alt="help doc" />
  <img src="../../../.github/assets/demo_wc2.gif" alt="usages" />
</details>

## Installation

Requirements: >=gcc 10.0, >=clang 13.0.0

The program is built using make.

```bash
make build
```

## Documentation

### -b, --bytes

Adds the number of bytes in the file(s) to the program output.

### -w, --words

Adds the number of words in the file(s) to the program output.

### -lines, --lines

Adds the number of newlines in the file(s) to the program output.

### -L, --max-line-length

Adds the length of the longest line in the file(s) to the output.

#### To display detailed help:

1. --help
2. --usage
3. -?

## License

[MIT](./LICENSE) © [Ivan Kovach](https://github.com/Qu1nel/)
