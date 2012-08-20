###########
Release 0.5
###########

************
New features
************

  - User interface rewrite with PyQt
  - Message is shown for missed attack
  - Message is shown for dying monster
  - Player character can be given a name

Following new features are more technical in nature and not visible during
gameplay.
  
  - _at function added to Cutesy
  - is_dead matcher added
  - other components can register to receive updates from domain objects

**********
Fixed bugs
**********

  - #17	Taking stairs do not update display correctly

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
