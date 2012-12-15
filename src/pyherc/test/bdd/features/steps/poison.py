from pyherc.test.cutesy import affect, weak_poison, potent_poison
from pyherc.test.bdd.features.helpers import get_character

@when(u'{character_name} suffers from {effect_name}')
def impl(context, character_name, effect_name):

    if effect_name == 'weak poison':
        poison_spec = weak_poison()
    elif effect_name == 'strong poison':
        poison_spec = potent_poison()

    character = get_character(context, character_name)

    affect(character, poison_spec)

