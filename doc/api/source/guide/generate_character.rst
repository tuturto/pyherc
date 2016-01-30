Generating characters
*********************
This section will have a look at character generation and related actions.

Character generator
===================
Characters can be created with ``generate-creature`` function:

.. code-block:: hy

    (generate-creature config model item-generator rng "rat")

Supplying creature configuration, model instance, item generator and random
number generator every time is tedious. For that reason, application
configuration :class:`pyherc.config.Configuration` has attribute
``creature_generator`` that holds reference to function with a simpler
interface, that is configured when system starts:

.. code-block:: hy

    (creature-generator "rat")

Only name is required, all other parameters are automatically using the values
supplied when the system started. This is also the function that is usually
passed around in the system to places where creatures might be generated (level
generators mainly).

Character selector
==================
When a specific part of the system requires ability to generate characters,
there are two options. First option is to pass a full fledged creature
generator and use that as explained in the previous paragraph. Another, much
simpler option is to use character selector. This is just a function, that
takes no parameters and will return a list of generated creatures. Advantage
of using them over creature generator is simplified usage:

.. code-block:: hy

    (defn skeletons [empty-pct character-generator rng]
      "create character selector for skeletons"
      (fn []
        (if (> (.randint rng 1 100) empty-pct)
          (character-generator "skeleton warrior")
          [])))

    (setv character-selector (skeletons 50
                                        creature-generator
                                        random))

    (setv monster (character-selector))

Usually character selector are given a descriptive name, like ``skeletons``
or ``common-critters``. For example :func:`pyherc.data.features.new_cache`
uses selectors to configure what kind of creatures or items might reside inside
of the cache.
