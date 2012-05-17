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

.. code-block:: python

  action = self.action_factory.get_action(MoveParameters(self,
                                                         direction,
                                                         'walk'))
  action.execute()

This creates a WalkAction and executes it, causing the character to take a 
single step to given direction.

Adding a new type of action
===========================

Lets say we want to create an action that allows characters to wait for 
specific amount of ticks.

Overview
--------
Actions are located in :mod:`pyherc.rules`. Custom is to have own package for
each type of action. For example, code related to moving is placed in
:mod:`pyherc.rules.move` while code for various attacks is in 
:mod:`pyherc.rules.attack`. Parameter classes are placed to 
:mod:`pyherc.rules.public` and imported to top level for ease of use.

Last important piece is factory that knows how to read parameter class and
construct action class based on it. Factories are placed in the same location
as the actions.

Creating a sub action factory
-----------------------------
Sub action factory is used to create specific types of actions. Start by
inheriting it and overriding type of action it can be used to construct:

.. code-block:: python

  from pyherc.rules.factory import SubActionFactory
  
  class WaitFactory(SubActionFactory):
  
      def __init__(self):
          self.action_type = 'wait'

Next we need to define factory method that can actually create our new action:

.. code-block:: python

  def get_action(self, parameters):
      wait_time = parameters.wait_time
      target = parameters.target
      return WaitAction(target, wait_time)

Defining new parameter class
----------------------------
WaitParameters class is very simple, almost could do without it even:

.. code-block:: python

  class WaitParameters(ActionParameters):
  
      def __init__(self, target, wait_time):
          self.action_type = 'wait'
          self.target = target
          self.wait_time = wait_time

Constructor takes two parameters: target who is character doing the waiting
and wait_time, which is amount of ticks to wait. action_type is used by the
factory system to determine which factory should be used to create action
based on parameter class. It should match to the action_type we defined in
WaitFactory constructor.

Creating the new action
-----------------------
WaitAction is not much more complex:

.. code-block:: python

  class WaitAction(object):
  
      def __init__(self, target, wait_time):
          self.target = target
          self.wait_time = wait_time

      def is_legal(self):
          return True
      
      def execute(self):
          self.target.tick = self.target.tick + self.wait_time

Constructor is used to create a new instance of WaitAction, with given
Character and wait time. 

is_legal can be called by system before trying to execute the action, in order
to see if it can be safely done. We did not place any validation logic there
this time, but one could check for example if the character is too excited to
wait.

Calling execute will trigger the action and in our case increment internal
timer of the character. This will effectively move his turn further in the
future.

Configuring ActionFactory
-------------------------
:class:`pyherc.rules.public.ActionFactory` needs to be configured in order it
to be able to create our new WaitAction. This is done in 
:class:`pyherc.config.Configuration`:

.. code-block:: python

  wait_factory = WaitFactory()

  self.action_factory = ActionFactory(
                                      self.model,
                                      [move_factory,
                                      attack_factory,
                                      drink_factory,
                                      wait_factory])

Adding easy to use interface
----------------------------
Last finishing step is to add easy to use method to Character class:

.. code-block:: python
 
  def wait(self, ticks = 5):
      action = self.action_factory.get_action(WaitParameters(self,
                                                             ticks))
      action.execute()

Now we can have our character to wait for a bit, just by calling:

.. code-block:: python

  player_character.wait()

Whole code
----------
Below is shown the whole example of wait action and demonstration how it
changes value in character's internal clock.

.. testcode::

    from pyherc.data import Character, Model
    from pyherc.rules import ActionFactory, ActionParameters
    from pyherc.rules.factory import SubActionFactory
    from random import Random
  
    class WaitParameters(ActionParameters):
  
        def __init__(self, target, wait_time):
            self.action_type = 'wait'
            self.target = target
            self.wait_time = wait_time

    class WaitAction(object):
  
        def __init__(self, target, wait_time):
            self.target = target
            self.wait_time = wait_time

        def is_legal(self):
            return True
      
        def execute(self):
            self.target.tick = self.target.tick + self.wait_time
            
    class WaitFactory(SubActionFactory):
  
        def __init__(self):
            self.action_type = 'wait'

        def get_action(self, parameters):
            wait_time = parameters.wait_time
            target = parameters.target
            return WaitAction(target, wait_time)

    model = Model()    
    wait_factory = WaitFactory()
    action_factory = ActionFactory(model = model,
                                   factories = [wait_factory])
    character = Character(model = model, 
                          action_factory = action_factory,
                          rng = Random())
    action = character.create_action(WaitParameters(character, 5))
    
    print('Ticks {0}'.format(character.tick))
    action.execute()
    print('Ticks after waiting {0}'.format(character.tick))

.. testoutput::

    Ticks 0
    Ticks after waiting 5

List of current actions
=======================

- Moving

 - :class:`pyherc.rules.move.action.MoveAction`
 - :class:`pyherc.rules.move.action.WalkAction`

- Combat

 - :class:`pyherc.rules.attack.action.AttackAction`

- Eating and drinking

 - :class:`pyherc.rules.consume.action.DrinkAction`
 
