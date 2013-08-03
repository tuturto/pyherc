Error Handling
**************
Pyherc, like any other software contains errors and bugs. Some of them are
so fatal that they could potentially crash the program. This chapter gives
an overview on how runtime errors are handled.

General idea
============
The general idea is to avoid littering the code with error handling and only
place it where it actually makes difference. Another goal is to keep the game
running as long as possible and avoid error dialogs. Instead of displaying
an error dialog, errors are masked as magical or mystical events. There should
be enough logs though to be able to investigate the situation later.

Specific cases
==============

Character
---------
:class:`pyherc.data.character.Character` is a central location in code.
Majority actions performed by the characters flow through there after they
have been initiated either by a user interface or artificial intelligence
routine.

:func:`pyherc.data.character.guarded_action` is a decorator that should
only be used in Character class. In the following example a move method has
been decorated with both logged and guarded_action decorators:

.. code-block:: python

   @guarded_action
   @logged
   def move(self, direction, action_factory):
      ...

In case an exception is thrown, guarded_action will catch and handle it. The
game might be in inconsistent state after this, but at least it did not crash.
The decorator will set tick of the character to suitable value, so that other
characters have a chance to act before this one is given another try. It will
also emit :class:`pyherc.events.error.ErrorEvent` that can be processed to
inform the player that there is something wrong in the game.

Since the decorator is emitting an event, it should not be used for methods
that are integral to event handling. This might cause an infinite recursion
that ultimately will crash the program. It is best suited for those methods
that are used to execute actions, like 
:meth:`pyherc.data.character.Character.move`
and :meth:`pyherc.data.character.Character.pick_up`