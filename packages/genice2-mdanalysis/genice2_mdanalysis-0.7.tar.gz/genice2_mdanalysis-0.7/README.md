![Logo](https://raw.githubusercontent.com/vitroid/GenIce/develop/logo/genice-v0.png)

# [genice2-mdanalysis](https://github.com/vitroid/genice-mdanalysis)

A format plugin for [GenIce2](https://github.com/vitroid/GenIce) to make a Universe of MDAnalysis.

version 0.7

## Requirements

* python^3.9
* GenIce2^2.2.5.2
* MDAnalysis*


## Installation from PyPI

```shell
% pip install genice2-mdanalysis
```

## Usage
        
    Write the ice structure in various file formats with the help of MDAnalysis.

    Usage:
        % genice 1c -f mdanalysis > 1c.pickle
        % genice 1c -f mdanalysis[1c.gro]
        % genice 1c -f mdanalysis[1c.xtc]

    Options:
        filename  The file name to be written. The file type is specified by the
                  suffix. All the supported file types are listed in the
                  [MDAnalysis web page](https://docs.mdanalysis.org/stable/documentation_pages/coordinates/init.html#supported-coordinate-formats).
                  If the file name is not specified, the Universe instance of
                  MDAnalysis is written to the stdout in the python pickle
                  format.




## Test in place

```shell
% make test
```
