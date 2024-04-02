![Logo](https://raw.githubusercontent.com/vitroid/GenIce/develop/logo/genice-v0.png)

# [genice2-yaplot](https://github.com/genice-dev/genice2-yaplot)

A [GenIce](https://github.com/vitroid/GenIce) plugin to illustrate the structure in Yaplot format.

version 0.1

## Requirements

* python^3.9
* numpy^1.26.4
* GenIce2>=2
* yaplotlib*


## Installation from PyPI

```shell
% pip install genice2-yaplot
```

## Manual Installation

### System-wide installation

```shell
% make install
```

### Private installation

Copy the files in /formats/ into your local formats/ folder.

## Usage
        
    Usage: genice2 icename -f yaplot[options]

    options:
        H=x   Set the radius of H to be x.


## Test in place

```shell
% make test
```
