#####
Intro
#####

**********
Background
**********

Herculeum is a dungeon adventuring game in a spirit of Rogue and Nethack.
Player assumes the role of adventurer who has made perilous journey through
jungles of Thynian and finally reached ruins of Herculeum. His tasks is to
descent into deep caverns found underneath of the ruins and gather as much loot
as possible before returning back to the surface. Rumours are that there is
an ancient artifact hidden somewhere in the ruins and the adventurer wishes to
posses it.

*******************
Installing the game
*******************
There are two ways of installing the game. First one is to use the provided
Windows executable. This is the easiest method, but will only work on computers
running on Windows operating system.

Second option is to install Python interpreter, some libraries and run the game
from source code.

Windows executable
==================
Windows executable bundles together Python interpreter, all required libraries
and the game. Just unpack the distribution package to a folder, install
required dependencies and start the game by double clicking herculeum.exe

Dependencies
------------
- Microsoft Visual C++ 2008 Redistributable Package 

Installing dependencies
-----------------------
Install Microsoft Visual C++ 2008 Redistributable Package from Microsoft_.

Source code distribution
========================
Source code distribution is more complicated to set up (not much though), but
it gives you possibility to read and modify the source code. Start by
installing required dependencies, unpack the distribution package to a folder
and start the game by double clicking pyherc.bat or pyherc.sh in installation
folder.

Dependencies
------------
- Python 2.7.3 (2.6.1 should be sufficient if you do not wish to run tests)
- PyQt4
- web.py 0.3 (only needed for running debug server)
- mockito-python 0.5.0 (only needed for running test cases)
- pyHamcrest 1.6 (only needed for running test cases)
- qc (only needed for running test cases)
- behave (only needed for running test cases)
- satin-python (only needed for running test cases)
- Sphinx 1.1.2 (only needed for generating documentation)

Installing dependencies
-----------------------
Install python 2.7 from Python_.

Install setuptools, by following instructions at: setuptools_.

Install PyQt4, by following instructions at: PyQt4_

Install pip (only needed for installing qc)::

    easy_install -U pip

Rest of the dependencies can be automatically located and installed by following
steps:

If you want to run debug server, install web.py::

    easy_install -U web.py
    
If you want to be able to run test cases, install mockito-python, pyHamcrest,
qc and behave::

    easy_install -U mockito
    easy_install -U pyhamcrest
    pip install -e git://github.com/dbravender/qc.git#egg=qc
    easy_install -U behave

If you want to generate html manual and programmers guide, install Sphinx::

    easy_install -U Sphinx

.. _Python: http://python.org/getit/
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _PyQt4: http://www.riverbankcomputing.co.uk/software/pyqt/intro
.. _Microsoft: http://www.microsoft.com/en-us/download/details.aspx?id=29