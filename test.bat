nosetests --with-xunit --doctest-tests --with-coverage --cover-html --traverse-namespace --cover-html-dir=./doc/cover --cover-package=pyherc --cover-package=herculeum
cd doc
cd api
call make doctest
cd ..
cd ..
cd src\pyherc\test\bdd
behave --junit --junit-directory ./../../../../doc/behave/reports
cd ..\..\..\..
python xunit.py
python run_pylint.py
