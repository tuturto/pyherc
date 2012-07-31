pyherc.data.level
*****************
.. automodule:: pyherc.data.level
    :show-inheritance:

    .. autoclass:: Level
      :show-inheritance:
    
        .. automethod:: __init__(size = (0, 0), floor_type = None, wall_type = None, empty_floor = 0, empty_wall = 0)
        
        .. automethod:: get_tile(loc_x, loc_y)
        .. automethod:: get_wall_tile(loc_x, loc_y)
        .. automethod:: add_item(item, location)
        .. automethod:: get_items_at(location)
        .. automethod:: add_portal(portal, location, other_end = None)
        .. automethod:: get_portal_at(location)
        .. automethod:: add_creature(creature, location = None)
        .. automethod:: remove_creature(creature)
        .. automethod:: get_creature_at(location)
        .. automethod:: find_free_space()
        .. automethod:: get_square(x_coordinate, y_coordinate)
        .. automethod:: blocks_movement(loc_x, loc_y)
        .. automethod:: blocks_los(x_coordinate, y_coordinate)
        .. automethod:: get_size()
        .. automethod:: set_location_type(location, location_type)
        .. automethod:: get_location_type(location)
        .. automethod:: get_locations_by_type(location_type)
    
        Following methods are best suited for debugging purposes

        .. automethod:: dump_string()
