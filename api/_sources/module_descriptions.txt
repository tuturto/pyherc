Building blocks
***************

Codebase is divided in two main pieces :py:mod:`pyherc` and :py:mod:`herculeum`. 
pyherc is a sort of platform or library for writing roguelike games. herculeum 
on the other hand is a sample game that has been written on top of pyherc.

On a high level, pyherc and herculeum codebases are divided as detailed below:

.. graphviz:: 

    digraph hierarchy {        
        rankdir=LR
        node[shape=box]
        edge[dir=forward, arrowtail=empty, arrowhead=none]
        pyherc
        ai
        config
        config_dsl[label="dsl"]
        data
        data_effects[label="effects"]
        debug
        events
        generators
        generators_level[label="level"]
        generators_level_decorator[label="decorator"]
        generators_level_partitioners[label="partitioners"]
        generators_level_room[label="room"]
        rules
        rules_attack[label="attack"]
        rules_consume[label="consume"]        
        rules_inventory[label="inventory"]
        rules_move[label="move"]
        test
        test_bdd[label="bdd"]
        test_builders[label="builders"]
        test_cutesy[label="cutesy"]
        test_helpers[label="helpers"]
        test_integration[label="integration"]
        test_matchers[label="matchers"]
        test_unit[label="unit"]

        herculeum
        herculeum_config[label="config"]
        herculeum_config_levels[label="levels"]
        herculeum_gui[label="gui"]
        herculeum_gui_core[label="core"]
        
        pyherc->ai
        pyherc->config->config_dsl
        pyherc->data->data_effects
        pyherc->debug
        pyherc->events
        pyherc->generators->generators_level->generators_level_decorator
        generators_level->generators_level_partitioners
        generators_level->generators_level_room
        pyherc->rules->rules_attack
        rules->rules_consume
        rules->rules_inventory
        rules->rules_move
        pyherc->test->test_bdd
        test->test_builders
        test->test_cutesy
        test->test_helpers
        test->test_integration
        test->test_matchers
        test->test_unit
        
        herculeum->herculeum_config->herculeum_config_levels
        herculeum->herculeum_gui->herculeum_gui_core
    }

Convenient links to each of main components

  pyherc:
  
  * :py:mod:`pyherc`
  * :py:mod:`pyherc.ai`
  * :py:mod:`pyherc.config`
  * :py:mod:`pyherc.data`
  * :py:mod:`pyherc.debug`
  * :py:mod:`pyherc.events`
  * :py:mod:`pyherc.generators`
  * :py:mod:`pyherc.rules`
  * :py:mod:`pyherc.test`

  herculeum:
  
  * :py:mod:`herculeum`
  * :py:mod:`herculeum.config`
  * :py:mod:`herculeum.gui`

Main components
***************
  
Model
=====
:class:`pyherc.data.model.Model` is the main class representing
current state of the playing world. It holds reference to important things like:

  * Player character
  * Dungeon
  * Configuration
  * Various tables

Character
=========
:class:`pyherc.data.character.Character` is used to represent both player 
character and monsters. It manages things like:

  * Stats
  * Inventory
  * Location

Dungeon
=======
:class:`pyherc.data.dungeon.Dungeon` is currently very sparse and is only
used to hold reference to first level in the dungeon.

Level
=====
:class:`pyherc.data.level.Level` is key component, as it is used to store
layout and content of levels where player adventures. It manages:

  * Shape of the level, including stairs leading to other levels
  * Items
  * Characters

Rules
=====
:mod:`pyherc.rules` is what defines what kind of actions player and monsters
are allowed to take and how they affect the world around them. Rules for things
like moving, fighting and drinking potions are found here. Refer to
:doc:`actions` for more detailed description how actions are created and how to
add more.
