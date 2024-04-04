"""
    Loads the environment variables from the .export file if
        - The DB environment variable is not set that means either:
            - I am running in the console
            - or other user than me is running the script.
    """

import subprocess
from os import environ
from pathlib import Path

import dotsi

ENV = dict(environ)

def read_env() :
    if 'DB' in ENV :
        return dotsi.fy(ENV)

    fn = Path(f"{ENV['HOME']}/.export")
    if not fn.exists() :
        fn = Path(f"/homes/nber/mahdimir/.export")

    with open(fn) as f :
        script = f.read()
    script = script.encode() + b'\nenv'

    with subprocess.Popen(['sh'] ,
                          stdin = subprocess.PIPE ,
                          stdout = subprocess.PIPE) as p :
        result = p.communicate(script)

    for line in result[0].decode().splitlines() :
        var , _ , value = line.partition('=')
        environ[var] = value

    if not 'DB' in environ :
        raise Exception('DB is not set')

    return dotsi.fy(dict(environ))
