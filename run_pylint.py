#!/usr/bin/python
import os, glob, sys
from pylint.lint import Run

print 'running static analysis'

os.chdir('doc/pyherc')
files = glob.glob('*')
for f in files:
    os.remove(f)

runner = Run(['--rcfile=../../pylint.rc', '../../src/pyherc'], exit = False)
msg_status_pyherc =  runner.linter.msg_status

os.chdir('../herculeum')
files = glob.glob('*')
for f in files:
    os.remove(f)

runner = Run(['--rcfile=../../pylint.rc', '../../src/herculeum'], exit = False)
msg_status_herculeum =  runner.linter.msg_status

result = msg_status_pyherc | msg_status_herculeum

if result == 0:
    print 'no problems'
else:
    if result & 1 == 1:
        print 'Fatal error'
    if result & 2 == 2:
        print 'Error detected'
    if result & 4 == 4:
        print 'Warning detected'
    if result & 8 == 8:
        print 'Need for refactoring detected'
    if result & 16 == 16:
        print 'Some conventions are violated'

sys.exit(result)
