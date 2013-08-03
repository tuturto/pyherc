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
- Python 3.2
- PyQt4
- decorator
- mockito-python 0.5.0 (only needed for running test cases)
- pyHamcrest 1.6 (only needed for running test cases)
- behave (only needed for running test cases)
- satin-python (only needed for running test cases)
- Sphinx 1.1.3 (only needed for generating documentation)

Installing dependencies
-----------------------
Install python 3.2 from Python_.

Install setuptools, by following instructions at: setuptools_.

Install PyQt4, by following instructions at: PyQt4_

Install libraries::

    pip install -U -r dependencies

Install more libraries for playing around with the code::

    pip install -U -r dependencies-dev

.. _Python: http://python.org/getit/
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _PyQt4: http://www.riverbankcomputing.co.uk/software/pyqt/intro
.. _Microsoft: http://www.microsoft.com/en-us/download/details.aspx?id=29
