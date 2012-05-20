Building blocks
***************

On a high level, pyherc codebase is divided as detailed below:

.. graphviz:: 

    digraph hierarchy {
        node[shape=box]
        edge[dir=forward, arrowtail=empty]
        pyherc
        ai
        data
        debug
        generators
        gui
        rules
        test

        pyherc->ai
        pyherc->data
        pyherc->debug
        pyherc->generators
        pyherc->gui
        pyherc->rules
        pyherc->test    
    }

Convenient links to each of main components

  * :py:mod:`pyherc.ai`
  * :py:mod:`pyherc.data`
  * :py:mod:`pyherc.debug`
  * :py:mod:`pyherc.generators`
  * :py:mod:`pyherc.gui`
  * :py:mod:`pyherc.rules`
  * :py:mod:`pyherc.test`
    
Model
=====
:class:`pyherc.data.model.Model` is the main class representing
current state of the playing world. It holds reference to important things like:

  * Player character
  * Dungeon
  * Configuration
  * Various tables
