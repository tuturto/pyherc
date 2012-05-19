cd doc
cd manual
rmdir /S /Q build
call make html
cd ..
cd releasenotes
rmdir /S /Q build
call make html
cd ..
cd api
rmdir /S /Q build
call make html
call make doctest
cd ..
cd ..
