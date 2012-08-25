from pyherc.test.cutesy import affect, weak_poison, potent_poison

@when(u'{character_name} suffers from {effect_name}')
def impl(context, character_name, effect_name):

    if effect_name == 'weak poison':
        poison_spec = weak_poison()
    elif effect_name == 'strong poison':
        poison_spec = potent_poison()

    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]

    affect(character, poison_spec)

