def simple_heuristic(state):
    queues = state.get("queues", {})
    action = {}
    if not queues:
        return {lane: {"signal":"red"} for lane in ["north","east","south","west"]}
    max_lane = max(queues, key=lambda k: queues[k])
    for lane in queues:
        if lane == max_lane:
            action[lane] = {"signal":"green", "duration":5}
        else:
            action[lane] = {"signal":"red", "duration":5}
    return action
