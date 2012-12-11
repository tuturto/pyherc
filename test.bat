nosetests --with-xunit --doctest-tests --with-coverage --cover-html --traverse-namespace --cover-html-dir=./cover --cover-package=pyherc --cover-package=herculeum
cd doc
cd api
call make doctest
cd ..
cd ..
cd src\pyherc\test\bdd
behave --junit --junit-directory ./../../../../behave/reports
cd ..\..\..\..
python xunit.py
python run_pylint.py
