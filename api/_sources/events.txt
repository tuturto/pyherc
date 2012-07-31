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

Events and UI
=============
One important factor of events are their ability to tell UI what pieces of map
were affected and should be redrawn next time the screen is updated. This is
done by passing a list of coordinates (int, int) in affected_tiles parameter
that each and every event has in constructor.

Events that modify location of characters, shape of the map or otherwise affect
to the world visible to the player should list the affected tiles for fast UI
update. For example, move action will usually have two tiles in the list: the
original location of character and the new location. If character were carrying
a lightsource when moving, appropriate squares should be listed too (those that
were lighted, but are now in darkness and vice versa).

List of events
==============
 - :class:`pyherc.events.combat.AttackHitEvent`
 - :class:`pyherc.events.move.MoveEvent`
