########
Commands
########

*************
Main controls
*************
The game has been designed to be played with keyboard or with joypad with help
of correct tools. Buttons used to control the game are:

 * move: keypad, cursor keys, vi keys
 * action a: space, z, keypad 5
 * action b: control, x
 * menu: return
 * switch to sub menu left: insert, page up, q
 * switch to sub menu right: delete, page down, w

.. hint:: a tool like Xpadder_ enables you to use joypad for playing, thus
   making the game more fun.
 
*******************
Starting a new game
*******************
When the game starts, the character selection screen is shown. Use left and
right to scroll through different characters and action a to select your
character.

**************
Main interface
**************
Player character is shown in the middle of the screen with the dungeon shown
surrounding him. Items and monsters are also shown on this area.

.. image:: images/game_area.png
   :alt: Picture of playing area

At the top portio of the screen amount of hit points and mana are being shown.
Next to them are icons of currently active effects (poisoning and healing in
this case).

Bottom of the screen is reserved for the battle log, which can be used to check
details of previous actions.

Player can move in eight directions using move keys and descent or ascent 
stairs by using action a button.

----------------
Picking up items
----------------
Easiest way to pick up an item is to walk on top of it and press action a to
pick it up. If there are multiple items, player can either pick them up one
by one or open inventory page and use it to manipulate items.

-----------------
Attacking enemies
-----------------
Character automatically attacks an enemy if player tries to enter same location
where the enemy is.

****
Menu
****
Menu can be opened by pressing menu key. This will bring up a multipage menu,
where player can navigate by using switch keys.

---------
Inventory
---------
Iventory window shows items on the ground, carried items and items in use at
the same time.

.. image:: images/inventory.png
   :alt: Picture of inventory screen

Inventory is accessible from menu. In inventory window, move selector around by
using move keys. Action a will use an item if it is in your invetory or pick it
up if it is on ground.

Action b is used to drop items on to ground.

----------------
Player character
----------------
Details of the player character are shown on a separate page of menu (accessed
with switch buttons).

.. image:: images/character_screen.png
   :alt: Picture of character screen

Top of the screen shows his current statistics: body, mind, finesse, hit points
and mana. Below of them are details of currently active effects.

.. _Xpadder: http://www.xpadder.com/
