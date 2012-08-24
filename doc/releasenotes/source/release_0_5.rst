###########
Release 0.5
###########

************
New features
************
New features that are readily visible to players:

  - User interface rewrite with PyQt
  - 16_ inventory window
  - Message is shown for missed attack
  - Message is shown for dying monster
  - Message is shown for picked up item
  - Message is shown for dropped item
  - Player character can be given a name

Following new features are more technical in nature and not visible during
gameplay:
  
  - _at function added to Cutesy
  - is_dead matcher added
  - other components can register to receive updates from domain objects
  - pyherc.rules.items.drop replaced with DropAction

**********
Fixed bugs
**********

  - 17_ Taking stairs do not update display correctly

***********
Other notes
***********

  - Services are no longer injected to domain objects
  - pyherc.rules.effects moved to pyherc.data.effects
  - EffectsCollection moved to pyherc.data.effects
  - qc added for testing
  - poisoning and dying from poison tests moved to BDD side
  - is_at and is_not_at changed to is_in and is_not_in
  - herculeum.gui.core removed
  - PGU and pygame removed as dependecies

.. _16: https://github.com/tuturto/pyherc/issues/16
.. _17: https://github.com/tuturto/pyherc/issues/17
