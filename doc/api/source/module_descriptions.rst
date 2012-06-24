Building blocks
***************

On a high level, pyherc codebase is divided as detailed below:

.. graphviz:: 

    digraph hierarchy {        
        rankdir=LR
        node[shape=box]
        edge[dir=forward, arrowtail=empty, arrowhead=none]
        pyherc
        ai
        config
        config_levels[label="levels"]
        data
        debug
        events
        generators
        generators_level[label="level"]
        generators_level_decorator[label="decorator"]
        generators_level_partitioners[label="partitioners"]
        generators_level_room[label="room"]
        gui
        gui_core[label="core"]
        rules
        rules_attack[label="attack"]
        rules_consume[label="consume"]
        rules_effects[label="effects"]
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

        pyherc->ai
        pyherc->config->config_levels        
        pyherc->data
        pyherc->debug
        pyherc->events
        pyherc->generators->generators_level->generators_level_decorator
        generators_level->generators_level_partitioners
        generators_level->generators_level_room
        pyherc->gui->gui_core
        pyherc->rules->rules_attack
        rules->rules_consume
        rules->rules_effects
        rules->rules_inventory
        rules->rules_move
        pyherc->test->test_bdd
        test->test_builders
        test->test_cutesy
        test->test_helpers
        test->test_integration
        test->test_matchers
        test->test_unit
    }

Convenient links to each of main components

  * :py:mod:`pyherc.ai`
  * :py:mod:`pyherc.config`
  * :py:mod:`pyherc.data`
  * :py:mod:`pyherc.debug`
  * :py:mod:`pyherc.events`
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
