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

Dependencies
============
- Python 2.7.3 (2.6.1 should be sufficient if you do not wish to run tests)
- PyQt4
- Aspyct 3.0 beta 4 (packaged with the system)
- web.py 0.3 (only needed for running debug server)
- mockito-python 0.5.0 (only needed for running test cases)
- pyHamcrest 1.6 (only needed for running test cases)
- qc (only needed for running test cases)
- behave (only needed for running test cases)
- satin-python (only needed for running test cases)
- Sphinx 1.1.2 (only needed for generating documentation)

Installing dependencies
=======================
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

Last step is to extract installation package to suitable folder.

****************
Running the game
****************
Run game by double clicking pyherc.bat or pyherc.sh in installation folder.