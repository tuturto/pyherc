###########
Release 0.8
###########

************
New features
************
 - amount of damage done is reported more clearly
 - new area: Crimson Lair
 - weapons may have special effects that are triggered in combat
 - 45_ feature: ranged combat
 - 44_ feature: armours
 - 43_ feature: support for vi and cursor keys
 - 40_ feature: executable for Windows
 - 39_ feature: the Tome of Um'bano
 - 37_ feature: creating a new character
 - 36_ feature: escaping the dungeon
 - 35_ feature: crimson jaw
 - equiping and unequiping raise events

**********
Fixed bugs
**********

 - 26_ bug: spider poisons in combat even when it misses
 - 10_ bug: Player character creation has hard coded values

**********
Known bugs
**********

 - 42_ bug: character generator generates incorrect amount of items in inventory
 - 38_ bug: damage effect does not take damage modifiers into account
 - 25_ bug: dying should make game to return to main screen
 - 21_ bug: PyQt user interface does not support line of sight
 - 9_ bug: Attacks use hard coded time
 - 5_ bug: Raised events are not filtered, but delivered to all creatures
 
***********
Other notes
***********

 - 41_ player character configuration
 - Aspyct is no longer needed to run the game
 - behave tests moved under src/pyherc/test/BDD
 - parts of the manual are generated directly from game data

.. _45: https://github.com/tuturto/pyherc/issues/45
.. _44: https://github.com/tuturto/pyherc/issues/44
.. _43: https://github.com/tuturto/pyherc/issues/43
.. _42: https://github.com/tuturto/pyherc/issues/42
.. _41: https://github.com/tuturto/pyherc/issues/41
.. _40: https://github.com/tuturto/pyherc/issues/40
.. _39: https://github.com/tuturto/pyherc/issues/39
.. _38: https://github.com/tuturto/pyherc/issues/38
.. _37: https://github.com/tuturto/pyherc/issues/37
.. _36: https://github.com/tuturto/pyherc/issues/36
.. _35: https://github.com/tuturto/pyherc/issues/35
.. _26: https://github.com/tuturto/pyherc/issues/26
.. _25: https://github.com/tuturto/pyherc/issues/25
.. _21: https://github.com/tuturto/pyherc/issues/21
.. _10: https://github.com/tuturto/pyherc/issues/10
.. _9: https://github.com/tuturto/pyherc/issues/9
.. _5: https://github.com/tuturto/pyherc/issues/5
