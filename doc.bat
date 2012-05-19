cd doc
cd api
rmdir /S /Q build
call make html
cd ..
cd manual
rmdir /S /Q build
call make html
cd ..
cd releasenotes
rmdir /S /Q build
call make html
cd ..
cd ..
