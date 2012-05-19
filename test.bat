nosetests --with-doctest --with-xunit --with-coverage --cover-html --cover-inclusive --traverse-namespace --cover-html-dir=./cover --cover-package=pyherc
cd doc
cd api
call make doctest
cd ..
cd ..
