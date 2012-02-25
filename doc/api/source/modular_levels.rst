Modular level generator
***********************
Now that you are aware how level generation works in general, we can have
a look at more modular approach. 
:class:`pyherc.generators.level.generator.LevelGenerator` is a high level
generator that can be used to create different kinds of levels. Usually
the system does not directly use it, but queries a fully setup generator
from :class:`pyherc.generators.level.generator.LevelGeneratorFactory`

Overview of LevelGenerator
==========================
.. code-block:: python

    def generate_level(self, portal, model, new_portals = 0, level=1, room_min_size = (2, 2)):

LevelGenerator has same generate_level - method as other level generators and
calling it functions in the same way. Difference is in the internals of the
generator. Instead of performing all the level generation by itself, 
LevelGenerator breaks it into steps and delegates each step to a sub component.

First new level is created and sent to a partitioner. This component will
divide level into sections and link them to each other randomly. Partitioners
are required to ensure that all sections are reachable.

A room is generated within each section and corridors are used to link rooms
to neighbouring sections. Linking is done according to links set up in the
previous phase. This in turn ensures that each room is reachable.

In decoration step details are added into the level. Walls are built where
empty space meets solid ground and floors are detailed.

Partitioners
============
:class:`pyherc.generators.level.partitioners.grid.GridPartitioner` is basic partitioner,
which knows how to divide level into a grid with equal sized sections.

GridPartitioner has method:

.. code-block:: python

    def partition_level(self, level,  x_sections = 3,  y_sections = 3):
    
Calling this method will partition level to sections, link sections to each other
and return them in a list.

:class:`pyherc.generators.level.partitioners.section.Section` is used to represent
section. It defines a rectangular area in level, links to neighbouring areas and
information how they should connect to each other. It also defines connections
for rooms.