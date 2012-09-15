Effects
*******
This section will have a look at effects, how they are created and handled
during the play and how to add new effects.

Overview of effects system
==========================
Effects can be understood as on-going statuses that have an effect to an 
character. Good example would be poisoning. When character has poison effect
active, he periodically takes small amount of damage, until the effect is
removed or it expires.

Both items and characters can cause effects. Spider can cause poisoning and
healing potion can grant healing.

Effect handles
==============
:class:`pyherc.data.effects.effect.EffectHandle` are sort of prototypes for
effects. They contain information on when to trigger the effect, name of the
effect, possible overriding parameters and amount of charges.

Effect
======
:class:`pyherc.data.effects.effect.Effect` is a baseclass for all effects.
All effects have duration, frequency and tick. Duration tells how long it takes
until effect naturally expires. Frequency tells how often effect is triggered
and tick is internal counter which keeps track when effect should trigger.

When creating a new effect, subclass Effect class and define method:

.. code-block:: python

   def do_trigger(self):

Do trigger method is automatically triggered when effect's internal counter
reaches zero. After the method has been executed, counter will be reset if the
effect has not been expired.

EffectsFactory
==============
Effects are cread by :class:`pyherc.generators.effects.EffectsFactory`. It can 
take EffectHandle, some parameters and create a correctly instantiated Effect.

EffectsFactory is configured during the start up of the system with information
that links names of effects to concrete Effect subclasses and their parameters.

.. testcode::

    from pyherc.generators import EffectsFactory
    from pyherc.data.effects import Poison
    from pyherc.test.cutesy.dictionary import Adventurer
    from pyherc.rules import Dying

    effect_factory = EffectsFactory()
    effect_factory.add_effect('minor poison',
                                        {'type': Poison,
                                        'duration': 240,
                                        'frequency': 60,
                                        'tick': 60,
                                        'damage': 1})

    Pete = Adventurer()
    print('Hit points before poisoning: {0}'.format(Pete.hit_points))
    
    poisoning = effect_factory.create_effect('minor poison', target = Pete)
    poisoning.trigger(Dying())
    
    print('Hit points after poisoning: {0}'.format(Pete.hit_points))

Pete the adventurer gets affected by minor poison and as a result loses 
1 hit point.
    
.. testoutput::

    Hit points before poisoning: 10
    Hit points after poisoning: 9

Note how the effect factory has been supplied by a dictionary of parameters.
These are matched to the constructor of class specified by 'type' key. All
parameters that are present in the constructor, but are not present in the
dictionary needs to be supplied when effect factory creates a new effect
instance. In our example there was only single parameter like this, the target
of poisoning.

It is also possible to supply parameters during call that have been specified
in the dictionary. These parameters are then used to override the default ones.

Effects collection
==================
:class:`pyherc.data.effects.effectscollection.EffectsCollection` is tasked to
keep track of effects and effect handles for particular object. Both Item and
Character objects use it to interact with effects sub system.

Following example creates an EffectHandle and adds it to the collection.

.. testcode::
   
   from pyherc.data.effects import EffectsCollection,EffectHandle
   
   collection = EffectsCollection()
   handle = EffectHandle(trigger = 'on kick',
                         effect = 'explosion',
                         parameters = None,
                         charges = 1)
   collection.add_effect_handle(handle)
   
   print collection.get_effect_handles()
   
The collection now contains a single EffectHandle object.
   
.. testoutput::

   [<pyherc.data.effects.effect.EffectHandle object at 0x...>]

Following example creates an Effect and adds it to the collection.

.. testcode::

   from pyherc.data.effects import EffectsCollection, Poison

   collection = EffectsCollection()
   effect = Poison(duration = 200, 
                   frequency = 10, 
                   tick = 0, 
                   damage = 1, 
                   target = None)
   collection.add_effect(effect)
   
   print collection.get_effects()

The collection now contains a single Poison object.
   
.. testoutput::

   [<pyherc.data.effects.poison.Poison object at 0x...>]
