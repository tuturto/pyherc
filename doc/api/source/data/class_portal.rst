Portal
******

Portals are used to link levels together. They can be stairs, ladders or
magical portals. Anything that allows characters to move from one level to
another is a portal.

.. autoclass:: pyherc.data.dungeon.Portal
   :members:

Connecting levels
=================

Two levels can be connected in following way

.. code-block:: python

    level_a = Level()
    level_b = Level()
    	
    portal_a = Portal()
    portal_b = Portal()
    	
    level_a.add_portal(portal_a, (5, 10))
    level_b.add_portal(portal_b, (2, 2), portal_a)

Proxies
=======

Proxies are special type of portal. They have only one end, while another end
is left unspecified. They also have reference to a level generator. When a
character tries to enter a proxy portal, new level is generated and linked with
old level, via the portal. After this level generator is removed.

Proxies are used to generate dungeon while the player descents deeper and
deeper. This speeds up start up of the game, allows game to adapt to player
progress and reduces memory consumption.
