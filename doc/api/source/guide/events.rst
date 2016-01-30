Events
******
Events, in the context of this article, are used in relaying information of
what is happening in the game world. They should not be confused with UI events
that are created when buttons of UI are pressed.

Overview of event system
========================
Events are represented by classes found at :mod:`pyherc.events` and they all
inherit from :class:`pyherc.events.event.Event`.

Events are usually created as a result of an action, but nothing prevents
them from being raised from somewhere else too.

Events are relayed by :py:meth:`pyherc.data.model.Model.raise_event` and there
exists convenient :py:meth:`pyherc.data.character.Character.raise_event` too.

:py:meth:`pyherc.data.character.Character.receive_event` method receives an
event that has been raised somewhere else in the system. The default 
implementation is to store it in internal array and process when it is 
character's turn to act. The character can use this list of events to remember
what happened between this and his last turn and react accordingly.
