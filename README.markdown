# PyReName
========

## Abstract

It is a little Python script to rename a bunch of files using an incremental naming style. It is great to rename your digital photos files.

## Use `doskey` to make this script a global command

This piece of Python script can only nail files within the same directory. So you should copy the script to the directory within where you want to renams the fils.

Or you can use the `doskey` cammand to make this script a global command under cmd.exe (**all these we talked in in Windows**). Do as follows:

1. Open `cmd.exe`.
1. `cd`(change directory) to where you store the `rfs.py` file.
1. Type `doskey rfs=Python rfs.py` in command line.

Then you can use `rfs` to run the script in any directory under `cmd.exe`. It's much easier, right?

