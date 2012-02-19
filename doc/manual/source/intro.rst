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
- Python 2.6.1
- PyGame 1.9.2
- PGU 0.18
- pyDoubles 1.4 (only needed for running test cases)
- pyHamcrest 1.6 (only needed for running test cases)
- Sphinx 1.1.2 (only needed for generating documentation)

Installing dependencies
=======================
Install python 2.7 from Python_.

Install setuptools, by following instructions at: setuptools_.

Rest of the dependencies can be automatically located and installed by following
steps:

Install PyGame by typing::

    easy_install -U pygame

Install PGU by typing::

    easy_install -U pgu

If you want to be able to run test cases, install pyDoubles and pyHamcrest::

    easy_install -U pydoubles
    easy_install -U pyhamcrest

If you want to generate html manual and programmers guide, install Sphinx::

    easy_install -U Sphinx

.. _Python: http://python.org/getit/
.. _setuptools: http://pypi.python.org/pypi/setuptools

Last step is to extract installation package to suitable folder.

****************
Running the game
****************
Run game by double clicking pyherc.bat or pyherc.sh in installation folder.