#####
Intro
#####

**********
Background
**********
Herculeum is a dungeon adventuring game in a spirit of Rogue and Nethack.
Player assumes the role of an adventurer whose people have been trapped inside
of the labyrinth under city of Herculeum. The adventurer has been preparing for
the escape for a long time and now it is finally time to start the journey.

*******************
Installing the game
*******************
There are two ways of installing the game. First one is to install from
PyPi_ by using pip.

Second option is to install Python interpreter, some libraries and run the game
from source code.

PyPi
====

Install python 3.3 from Python_.

Install setuptools, by following instructions at: setuptools_.

Install PyQt4, by following instructions at: PyQt4_

Install game and dependencies::

    pip install -U hy
    pip install -U decorator
    pip install -U docopts
    pip install -U herculeum

After this the game can be run by executing script herculeum from command line.

Source code distribution
========================
Source code distribution is more complicated to set up (not much though), but
it gives you possibility to read and modify the source code. Start by
installing required dependencies, unpack the distribution package to a folder
and run the program by executing the herculeum script in scripts folder.

Dependencies
------------
- Python 3.3
- Hy 0.9.10
- docopts 0.6.1
- PyQt4
- decorator
- mockito-python 0.5.0 (only needed for running test cases)
- pyHamcrest 1.6 (only needed for running test cases)
- behave (only needed for running test cases)
- satin-python (only needed for running test cases)
- Sphinx 1.1.3 (only needed for generating documentation)

Installing dependencies
-----------------------
Install python 3.3 from Python_.

Install setuptools, by following instructions at: setuptools_.

Install PyQt4, by following instructions at: PyQt4_

Install libraries::

    pip install -U -r dependencies

Install more libraries for playing around with the code::

    pip install -U -r dependencies-dev

.. _Python: http://python.org/getit/
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _PyQt4: http://www.riverbankcomputing.co.uk/software/pyqt/intro
.. _PyPi: https://pypi.python.org/pypi/herculeum
