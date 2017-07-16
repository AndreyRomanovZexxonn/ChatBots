__author__ = 'zexxonn'

from setupTools import setupDatabase
from setupTools import setupVirtualEnv

import os, subprocess, sys
from config import basedir


setupVirtualEnv()
setupDatabase()

def run():
    bin = 'Scripts' if sys.platform == 'win32' else 'bin'
    subprocess.call([os.path.join(basedir, 'flask', bin, "python.exe"), os.path.join(basedir, "runServer.py")])

run()