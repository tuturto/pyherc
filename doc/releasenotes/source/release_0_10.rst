############
Release 0.10
############

************
New features
************

 - regular movement and attack can be done only to cardinal directions
 - characters can wait for a bit without doing anything
 - new player character, mage

**********
Fixed bugs
**********



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

 - 53_: moved many actions (moving, combat, etc) from Character class to separate functions

.. _53: https://github.com/tuturto/pyherc/issues/53
.. _42: https://github.com/tuturto/pyherc/issues/42
.. _38: https://github.com/tuturto/pyherc/issues/38
.. _25: https://github.com/tuturto/pyherc/issues/25
.. _21: https://github.com/tuturto/pyherc/issues/21
.. _9: https://github.com/tuturto/pyherc/issues/9
.. _5: https://github.com/tuturto/pyherc/issues/5
