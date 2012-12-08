@then(u'Game ends')
def impl(context):
    model = context.model
    
    assert model.end_condition == model.ESCAPED_DUNGEON
