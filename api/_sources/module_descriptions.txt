Building blocks
***************

On a high level, pyherc codebase is divided as detailed below:

  * ai - Artificial Intelligence for monsters
  * data - Classes that represent playing world (dungeon, levels, items and so on)
  * debug - Debug webserver
  * generators - Classes used to create the world
  * gui - routines needed to interact with the player
  * rules - rules of the game, for example how creatures move and fight
  * test - test routines

Model
=====
:class:`pyherc.data.model.Model` is the main class representing
current state of the playing world. It holds reference to important things like:

  * Player character
  * Dungeon
  * Configuration
  * Various tables
