from pyherc.data.model import ESCAPED_DUNGEON

@then(u'Game ends')
def impl(context):
    model = context.model

    assert model.end_condition == ESCAPED_DUNGEON
