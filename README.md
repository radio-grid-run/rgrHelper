# Radio Grid Run Helper Tools
Compute a team's territory based on the recorded what3words (w3w) codes

## 1. Setup and configuration

### 1.1 Dev dir setup

```
$ mkdir rgrHelper
$ virtualenv venv
$ source venv/bin/activate
$ vim setup.py
$ pip install -e .
```
For a good tutorial on how to setup venv see:
https://sourabhbajaj.com/mac-setup/Python/virtualenv.html

For a good example on how to use Setuptools see :
    https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/

## 2. Configuration
vir
`conf/gameConfig.ini` contains the game information (to be edited for each game)

`conf/rgrHelper.ini` contains the default for the scripts 

add a `.env` file with the following key-pair value in `rgrHelper` folder.

    w3wapikey = ThisIsMyAPIkey

## 2. Usage

For command line tools usage call:
    rgrHelper --help

Frédéric Noyer - October 2023
