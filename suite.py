#!/usr/bin/python

from subprocess import call
from os import chdir, listdir
from shutil import rmtree
from platform import system

import xunit, run_pylint

call(['nosetests', '--with-xunit',
                   '--doctest-tests',
                   '--with-coverage',
                   '--cover-html',
                   '--traverse-namespace',
                   '--cover-html-dir=./doc/cover',
                   '--cover-package=pyherc',
                   '--cover-package=herculeum'])
                   
chdir('doc/api')

if 'Windows' in system():
    call(['make.bat', 'doctest'])
else:
    call(['make', 'doctest'])

chdir('../../src/pyherc/test/bdd')
call(['behave'])

chdir('../../../..')

xunit.main()
run_pylint.main()
