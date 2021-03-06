############
Release 0.10
############

************
New features
************

 - new set of graphics and animations
 - regular movement and attack can be done only to cardinal directions
 - characters can wait for a bit without doing anything
 - new player character, mage
 - 68_ feature: change direction of character when walking

**********
Fixed bugs
**********

 - 72_ bug: moving does not take armour into account
 - 69_ bug: layering of icons
 - 54_ bug: weapons with multiple damage types cause attacker to move
 - 9_ bug: Attacks use hard coded time

**********
Known bugs
**********

 - 42_ bug: character generator generates incorrect amount of items in inventory
 - 38_ bug: damage effect does not take damage modifiers into account
 - 25_ bug: dying should make game to return to main screen
 - 21_ bug: PyQt user interface does not support line of sight
 - 5_ bug: Raised events are not filtered, but delivered to all creatures
 
***********
Other notes
***********

 - 53_: moved many actions (moving, combat, etc) from Character class to separate functions

.. _72: https://github.com/tuturto/pyherc/issues/72
.. _69: https://github.com/tuturto/pyherc/issues/69
.. _68: https://github.com/tuturto/pyherc/issues/68
.. _54: https://github.com/tuturto/pyherc/issues/54
.. _53: https://github.com/tuturto/pyherc/issues/53
.. _42: https://github.com/tuturto/pyherc/issues/42
.. _38: https://github.com/tuturto/pyherc/issues/38
.. _25: https://github.com/tuturto/pyherc/issues/25
.. _21: https://github.com/tuturto/pyherc/issues/21
.. _9: https://github.com/tuturto/pyherc/issues/9
.. _5: https://github.com/tuturto/pyherc/issues/5
