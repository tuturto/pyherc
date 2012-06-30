Building blocks
***************

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

        herculeum
        herculeum_config[label="config"]
        herculeum_config_levels[label="levels"]
        herculeum_gui[label="gui"]
        herculeum_gui_core[label="core"]
        
        pyherc->ai
        pyherc->config->config_dsl
        pyherc->data
        pyherc->debug
        pyherc->events
        pyherc->generators->generators_level->generators_level_decorator
        generators_level->generators_level_partitioners
        generators_level->generators_level_room
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
  
Model
=====
:class:`pyherc.data.model.Model` is the main class representing
current state of the playing world. It holds reference to important things like:

  * Player character
  * Dungeon
  * Configuration
  * Various tables
