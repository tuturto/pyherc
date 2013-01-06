####################
Commands (Text mode)
####################

*************
Main controls
*************
It is possible to run the game in text only mode, using library called curses.
Most Unix distributions include this library, but for Windows it often has to
be installed separately.

To start the game in text mode, add command line switch 'curses' when starting
the game.
 
*******************
Starting a new game
*******************
When the game starts, the character selection screen is shown. Press letter
that is displayed next to a character to select it.

**************
Main interface
**************
Player character is shown in the middle of the screen with the dungeon shown
surrounding him. Items and monsters are also shown on this area.

.. image:: images/curses_main.png
   :alt: Picture of playing area

Bottom of the screen shows player's current hitpoints and mana.

Top of the screen is reserved for the battle log, which can be used to check
details of previous actions.

Player can move in eight directions using keypad and descent or ascent 
stairs by using 5.

----------------
Picking up items
----------------
Easiest way to pick up an item is to walk on top of it and press 5 to
pick it up.

-----------------
Attacking enemies
-----------------
Character automatically attacks an enemy if player tries to enter same location
where the enemy is. For close combat you do not need weapon, although having
one can make quite a difference.

For ranged attack you need to have a weapon and suitable ammunition for it.
Attack enemies in distance by pressing 'a' and then direction from keypad.

---------
Inventory
---------
Iventory window shows items on the ground, carried items and items in use at
the same time.

.. image:: images/curses_inventory.png
   :alt: Picture of inventory screen

To use inventory, press first a command letter and then letter shown before an item
to perform the command on that item. Commands are:

 * u - use
 * d - drop
 * r - remove from use

Close inventory by pressing space.
