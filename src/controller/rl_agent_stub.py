class RLAgentStub:
    def __init__(self):
        pass
    def act(self, state):
        from .controller.heuristic import simple_heuristic
        return simple_heuristic(state)
