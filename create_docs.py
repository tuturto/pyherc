#!/usr/bin/python

from subprocess import call
from os import chdir, listdir
from shutil import rmtree
from platform import system

chdir('doc/manual')
if 'build' in listdir('.'):
    rmtree('build')
if 'Windows' in system():
    call(['make.bat', 'html'])
else:
    call(['make', 'html'])

chdir('../releasenotes')
if 'build' in listdir('.'):
    rmtree('build')
if 'Windows' in system():
    call(['make.bat', 'html'])
else:
    call(['make', 'html'])

chdir('../api')
if 'build' in listdir('.'):
    rmtree('build')
if 'Windows' in system():
    call(['make.bat', 'html'])
else:
    call(['make', 'html'])

if 'Windows' in system():
    call(['make.bat', 'doctest'])
else:
    call(['make', 'doctest'])

chdir('../..')
