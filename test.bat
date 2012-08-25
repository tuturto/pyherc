nosetests --with-xunit --doctest-tests --with-coverage --cover-html --traverse-namespace --cover-html-dir=./cover --cover-package=pyherc --cover-package=herculeum
cd doc
cd api
call make doctest
cd ..
cd ..
cd behave
behave --junit
cd ..
python xunit.py
