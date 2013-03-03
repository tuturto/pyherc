#!/usr/bin/python
import os, glob, sys
from pylint.lint import Run

def write_content(files):
    f = open('content.html', 'w')
    f.write('<html><head></head><body><ul>')
    for entry in files:
        if os.path.getsize(entry) > 0:
            link_name = entry
            index = link_name.find('.html')
            if index > -1:
                link_name = link_name[0:index]
            index = link_name.find('_')
            if index > -1:
                link_name = link_name[index+1:]
            f.write('<li><a href="{0}" target="report">{1}</a></li>'.format(entry, link_name))
        else:
            os.remove(entry)
    f.write('</ul></body></html>')
    f.close()

def write_index(title):
    f = open('index.html', 'w')
    f.write('<html><head><title>')
    f.write(title)
    f.write('</title></head><frameset cols="20%, 80%">')
    f.write('<frame src="content.html" name="content"><frame src="pylint_global.html" name="report">')
    f.write('</frameset></html>')
    
print('running static analysis')

os.chdir('doc/pyherc')
files = glob.glob('*')
for f in files:
    os.remove(f)

runner = Run(['--rcfile=../../pylint.rc', '../../src/pyherc'], exit = False)
msg_status_pyherc =  runner.linter.msg_status

files = glob.glob('*')
write_content(files)
write_index('pyherc')

os.chdir('../herculeum')
files = glob.glob('*')
for f in files:
    os.remove(f)

runner = Run(['--rcfile=../../pylint.rc', '../../src/herculeum'], exit = False)
msg_status_herculeum =  runner.linter.msg_status

files = glob.glob('*')
write_content(files)
write_index('herculeum')

result = msg_status_pyherc | msg_status_herculeum

if result == 0:
    print('no problems')
else:
    if result & 2 == 2:
        print('Error detected')
    if result & 4 == 4:
        print('Warning detected')
    if result & 8 == 8:
        print('Need for refactoring detected')
    if result & 16 == 16:
        print('Some conventions are violated')

os.chdir('..')
        
sys.exit(result)
