Magic
*****
This section will outline how spells are implemented.

Overview of Magic system
========================
SpellCastingAction created by SpellCastingFactory
SpellCastingAction has
 - caster
 - spell
 - effects_factory
 - dying_rules

Spell has
 - targets []
 - EffectsCollection
 - spirit

Spell is created by SpellGenerator by using SpellSpecification

SpellSpecification has
 - effect_handles
 - targeter
 - spirit

How spells are cast
===================


Spell creation during play
==========================


Adding a new type of spell
==========================

Overview
--------
  
Whole code
----------
