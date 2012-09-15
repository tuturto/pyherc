###########
Release 0.6
###########

************
New features
************

 - Support for Qt style sheets
 - Splash screen at start up
 - icons can be specified in level specific configuration scripts
 - new weapons added
 - new inventory screen
 - player can drink potions
 - on-screen counters to show damage, healing and status effects
 - player can wield and unwield weapons

**********
Fixed bugs
**********

 - 22_ python path is not modified before first imports
 - 19_ mdi user interface is clumsy to use

**********
Known bugs
**********

 - 26_ spider poisons in combat even when it misses
 - 25_ dying should make game to return to main screen
 - 21_ PyQt user interface does not support line of sight
 - 18_ Entities created by debug server are not shown on map
 - 5_ Raised events are not filtered, but delivered to all creatures
 
***********
Other notes
***********

 * behave_ taken into use for BDD
 * testing guidelines updated
 * "{character_name} is almost dead" added to behave
 * pyherc.rules.magic package removed

.. _26: https://github.com/tuturto/pyherc/issues/26
.. _25: https://github.com/tuturto/pyherc/issues/25
.. _22: https://github.com/tuturto/pyherc/issues/22
.. _21: https://github.com/tuturto/pyherc/issues/21
.. _19: https://github.com/tuturto/pyherc/issues/19
.. _18: https://github.com/tuturto/pyherc/issues/18
.. _5: https://github.com/tuturto/pyherc/issues/5
.. _behave: http://pypi.python.org/pypi/behave
