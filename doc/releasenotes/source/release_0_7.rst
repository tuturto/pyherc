###########
Release 0.7
###########

************
New features
************

 - damage is shown negative in counters
 - weapons deal different types of damage
 - split damage is supported
 - 30_ showing hit points of player
 - 29_ being weak against damage
 - 28_ damage resistance

**********
Fixed bugs
**********

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

.. _30: https://github.com/tuturto/pyherc/issues/30
.. _29: https://github.com/tuturto/pyherc/issues/29
.. _28: https://github.com/tuturto/pyherc/issues/28
.. _27: https://github.com/tuturto/pyherc/issues/27
.. _26: https://github.com/tuturto/pyherc/issues/26
.. _25: https://github.com/tuturto/pyherc/issues/25
.. _21: https://github.com/tuturto/pyherc/issues/21
.. _18: https://github.com/tuturto/pyherc/issues/18
.. _10: https://github.com/tuturto/pyherc/issues/10
.. _9: https://github.com/tuturto/pyherc/issues/9
.. _5: https://github.com/tuturto/pyherc/issues/5
.. _3: https://github.com/tuturto/pyherc/issues/3