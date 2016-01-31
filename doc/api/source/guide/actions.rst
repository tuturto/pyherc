Actions
*******
This section will have a look at actions, how they are created and handled
during play and how to add new actions.

Overview of Action system
==========================
Actions are used to represent actions taken by characters. This include things
like moving, fighting and drinking potions. Every time an action is taken by
a character, new instance of Action class (or rather subclass of it) needs to
be created.

Action creation during play
===========================
Actions are instantiated via ActionFactory, by giving it correct parameter
class. For example, for character to move around, it can do it by:

.. code-block:: hy

    (.execute (action-factory (MoveParameters character
                                              Direction.west)))

This creates a WalkAction and executes it, causing the character to take a 
single step to given direction. Doing this all the time is rather cumbersome,
so there are convenience functions at :mod:`pyherc.ports` that can be used:

.. code-block:: hy

    (move character Direction.west)

For checking if an action can be performed, following ways are generally
supported:

.. code-block:: hy

    (.legal? (action-factory (MoveParameters character
                                             Direction.west)))
                                             
    (move-legal? character Direction.west)
    
The first example will always be supported. The second example is generally
supported, but not always.

Interface
=========
Each function at :mod:`pyherc.ports` should return either ``(Right character)``
if the action was succesfull, or ``(Left character)`` if it couldn't be
completed. First parameter of the function should be the character who is
performing the action. Following these conventions allows us to define more
complex actions as terms of simpler ones:

.. code-block:: hy

    (defn lunge [character direction rng]
      (monad-> (move character direction)
               (attack direction rng)              
               (add-cooldown)))

Character is threaded through consecutive calls. If any of the calls fail for
any reason, calls after that one are automatically bypassed.

Extending
=========
ActionFactory has been designed to allow easy adding of new actions. Each
action has a respective factory function that can create it. These factory
functions are registered at the startup of the system in
:class:`pyherc.config.Configuration` class. When an action is requested, each
factory function is called in turn, until a correct one is found.

Factory function has general structure of:

.. code-block:: hy

    (fn [parameters]
      (if (can-handle? parameters)
        (Just Action)
        (Nothing)))

If factory function can handle the request, new action is returned, wrapped
inside ``Just``. In case function can not handle this request ``Nothing`` is
returned.
