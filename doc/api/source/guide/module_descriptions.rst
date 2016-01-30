Building blocks
***************
Codebase is divided in two main pieces :py:mod:`pyherc` and :py:mod:`herculeum`. 
pyherc is a sort of platform or library for writing roguelike games. herculeum 
on the other hand is a sample game that has been written on top of pyherc.


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

Ports
=====
:mod:`pyherc.ports` is the interface that rest of the code uses to connect with
actions subsystem. Instead of interfacing with ActionFactory and relatively
complex logic, client code should use functions defined in this module.
