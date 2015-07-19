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
PyPi_ by using pip. This is recommended if you just want to play the game.

Second option is to install Python interpreter, some libraries and run the game
from source code. This is also the method you want to use in case you would like
to do some hacking with the game.

First step in either method is to install python 3.4 from Python_, if you don't
have it already installed.

Virtualenv
==========
Virtualenv is a tool to create isolated Python environments. For more detailed
information, have a look at the official documentation of virtualenv_.

Create a new virtual environment by executing (Linux specific, equivalent
Windows instructions and testing would be appreciated)::

    virtualenv -p /usr/bin/python3 --system-site-packages pyherc

This will create a virtual environment using Python 3, having access to site-
wide packages (important for PyQt4 to work properly) and giving it name pyherc.
After creating the environment, activate it::

    source pyherc/bin/activate

Install setuptools, by following instructions at: setuptools_.

Install PyQt4, by following instructions at: PyQt4_

After this, proceed with eiher :ref:`pypi_instructions` or :ref:`src_instructions`.

.. _pypi_instructions:

PyPi
====
Install game and dependencies::

    pip install -U herculeum

After this the game can be run by executing script herculeum from command line.

.. _src_instructions:

Source code distribution
========================
.. note::

   This method is recommended only if you plan to modify the game or build your
   own game based on that. If you just want to play, see :ref:`pypi_instructions`.

Source code distribution is more complicated to set up (not much though), but
it gives you possibility to read and modify the source code.

Clone repository by executing following in an empty directory::

    git clone https://github.com/tuturto/pyherc.git

Install libraries by executing ::

    cd pyherc
    pip install -U -r requirements-all.txt

Before you can start the game, a resource file needs to be generated. This will
collect various images and other resources, package them into a single file and copy
the result in a correct directory ::

   cd resources/qt
   ./generate
   cd ../..


If everything went smoothly, you can start the game by executing ::

    cd src
    ./scripts/herculeum

.. _Python: http://python.org/getit/
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _PyQt4: http://www.riverbankcomputing.co.uk/software/pyqt/intro
.. _PyPi: https://pypi.python.org/pypi/herculeum
.. _virtualenv: https://virtualenv.pypa.io/en/latest/
