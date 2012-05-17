Effects
*******
This section will have a look at effects, how they are created and handled
during the play and how to add new effects.

Overview of effects system
==========================

Effect handles
==============
:class:`pyherc.rules.effects.effect.EffectHandle` are sort of prototypes for effects.
They contain information on when to trigger the effect, name of the effect,
possible overriding parameters and amount of charges.

Effects collection
==================
:class:`pyherc.data.effectscollection.EffectsCollection`

.. testcode::
   
   from pyherc.rules.effects import EffectHandle
   from pyherc.data import EffectsCollection
   
   collection = EffectsCollection()
   handle = EffectHandle(trigger = 'on kick',
                         effect = 'explosion',
                         parameters = None,
                         charges = 1)
   collection.add_effect_handle(handle)
