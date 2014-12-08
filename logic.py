class LogicManager(object):
    def update(self, entities, input_m, dt):
        for e in entities:
            e.update_logic(input_m, entities, dt)
