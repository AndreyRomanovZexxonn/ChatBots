#!/usr/bin/python
import os, subprocess, sys
from config import basedir

def setupVirtualEnv():
    if sys.platform == 'win32':
        bin = 'Scripts'
    else:
        bin = 'bin'

    if not os.path.exists( os.path.join(basedir, 'flask') ):
        print("RUN SETUP...")
        subprocess.call(['virtualenv', 'flask'])

        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask'])
        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'sqlalchemy'])
        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-sqlalchemy'])
        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'sqlalchemy-migrate'])
        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-whooshalchemy'])
        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-wtf'])
        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-babel'])
        #subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flup'])
        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'wikipedia'])
        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'requests'])
        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'forex_python'])
        subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'yahoo_finance'])
    else:
        print("SETUP WAS ALREADY DONE...")


def setupDatabase():
    if not os.path.exists( os.path.join(basedir, "app.db") ):
        subprocess.call(['python', os.path.join(basedir, "dbCreate.py")])