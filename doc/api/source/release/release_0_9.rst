###########
Release 0.9
###########

************
New features
************

 - 46_ curses interface

**********
Fixed bugs
**********

 - 48_ bug: Effects with None as duration or frequency cause crash when triggered

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

 - 47_ switch to Python 3

.. _48: https://github.com/tuturto/pyherc/issues/48
.. _47: https://github.com/tuturto/pyherc/issues/47
.. _46: https://github.com/tuturto/pyherc/issues/46
.. _42: https://github.com/tuturto/pyherc/issues/42
.. _38: https://github.com/tuturto/pyherc/issues/38
.. _25: https://github.com/tuturto/pyherc/issues/25
.. _21: https://github.com/tuturto/pyherc/issues/21
.. _9: https://github.com/tuturto/pyherc/issues/9
.. _5: https://github.com/tuturto/pyherc/issues/5
