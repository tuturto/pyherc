###########
Release 0.7
###########

************
New features
************

 - damage is shown negative in counters
 - weapons deal different types of damage
 - split damage is supported
 - more streamlined user interface
 - status effects are shown on main screen
 - 32_ view to show player character
 - 31_ better ai for skeleton warrior
 - 30_ showing hit points of player
 - 29_ being weak against damage
 - 28_ damage resistance
 - 24_ skeleton warrior

**********
Fixed bugs
**********

 - 34_ Split damage weapons do not show full damage on screen
 - 33_ using stairs while there is damage counter on screen crashes game
 - 27_ dropping a weapon in use retains the weapon in use

**********
Known bugs
**********

 - 26_ bug: spider poisons in combat even when it misses
 - 25_ bug: dying should make game to return to main screen
 - 21_ bug: PyQt user interface does not support line of sight
 - 18_ bug: Entities created by debug server are not shown on map
 - 10_ bug: Player character creation has hard coded values
 - 9_ bug: Attacks use hard coded time
 - 5_ bug: Raised events are not filtered, but delivered to all creatures
 - 3_ bug: FlockingHerbivore has no memory
 
***********
Other notes
***********

 - web.py is not required unless using debug server

.. _34: https://github.com/tuturto/pyherc/issues/34
.. _33: https://github.com/tuturto/pyherc/issues/33
.. _32: https://github.com/tuturto/pyherc/issues/32
.. _31: https://github.com/tuturto/pyherc/issues/31
.. _30: https://github.com/tuturto/pyherc/issues/30
.. _29: https://github.com/tuturto/pyherc/issues/29
.. _28: https://github.com/tuturto/pyherc/issues/28
.. _27: https://github.com/tuturto/pyherc/issues/27
.. _26: https://github.com/tuturto/pyherc/issues/26
.. _25: https://github.com/tuturto/pyherc/issues/25
.. _24: https://github.com/tuturto/pyherc/issues/24
.. _21: https://github.com/tuturto/pyherc/issues/21
.. _18: https://github.com/tuturto/pyherc/issues/18
.. _10: https://github.com/tuturto/pyherc/issues/10
.. _9: https://github.com/tuturto/pyherc/issues/9
.. _5: https://github.com/tuturto/pyherc/issues/5
.. _3: https://github.com/tuturto/pyherc/issues/3
