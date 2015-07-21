############
Release 0.14
############

************
New features
************

 - 112_ better installation instructions 

**********
Fixed bugs
**********

 - 114_ fix setup.py
 - 111_ bug: mitosis can create creatures on traps, without triggering them
 - 110_ bug: creatures and stairs are sometimes placed on top of traps
 - 96_ bug: two characters switching places cause level to be in inconsistent state

**********
Known bugs
**********

 - 113_ bug: items dropped in pit are floating
 - 97_ bug: level generation sometimes places multiple characters in same location
 - 89_ bug: CharacterBuilder does not add character to given level
 - 25_ bug: dying should make game to return to main screen
 - 21_ bug: PyQt user interface does not support line of sight
 
***********
Other notes
***********

 - 109_ event system restructure

.. _114: https://github.com/tuturto/pyherc/issues/114
.. _113: https://github.com/tuturto/pyherc/issues/113
.. _112: https://github.com/tuturto/pyherc/issues/112
.. _111: https://github.com/tuturto/pyherc/issues/111
.. _110: https://github.com/tuturto/pyherc/issues/110
.. _109: https://github.com/tuturto/pyherc/issues/109
.. _97: https://github.com/tuturto/pyherc/issues/97
.. _96: https://github.com/tuturto/pyherc/issues/96
.. _89: https://github.com/tuturto/pyherc/issues/89
.. _25: https://github.com/tuturto/pyherc/issues/25
.. _21: https://github.com/tuturto/pyherc/issues/21
