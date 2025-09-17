import random
from typing import List, Dict
from .entities import Vehicle, Pedestrian

class Environment:
    def __init__(self, config):
        self.config = config
        self.steps = config.get("steps", 200)
        self.weather = config.get("weather", "clear")
        self.vehicles: List[Vehicle] = []
        self.pedestrians: List[Pedestrian] = []
        self.time = 0
        self.lanes = ["north", "east", "south", "west"]
        self.signals = {lane: "red" for lane in self.lanes}
        self.queue = {lane: [] for lane in self.lanes}
        self.metrics = {"collisions":0, "avg_wait":0.0, "throughput":0}
        self._init_agents()

    def _init_agents(self):
        nv = self.config.get("num_vehicles", 100)
        nped = self.config.get("num_pedestrians", 50)
        for i in range(nv):
            lane = random.choice(self.lanes)
            v = Vehicle(id=i, lane=lane, position=random.uniform(0,500), speed=random.uniform(6,14))
            self.vehicles.append(v)
            self.queue[lane].append(v)
        for i in range(nped):
            p = Pedestrian(id=i, cross_pos=random.uniform(0,20), speed=random.uniform(0.8,1.6))
            self.pedestrians.append(p)

    def step_weather_effects(self):
        if self.weather == "clear":
            speed_mul = 1.0; breakdown_prob = 0.0005
        elif self.weather == "rain":
            speed_mul = 0.7; breakdown_prob = 0.002
        elif self.weather == "heat":
            speed_mul = 0.85; breakdown_prob = 0.001
        else:
            speed_mul = 1.0; breakdown_prob = 0.0005
        return speed_mul, breakdown_prob

    def step(self, control_actions: Dict[str, Dict]):
        speed_mul, breakdown_prob = self.step_weather_effects()
        for lane in self.lanes:
            signal = control_actions.get(lane, {}).get("signal", "red")
            if signal == "green":
                movers = min(3, len(self.queue[lane]))
                for _ in range(movers):
                    v = self.queue[lane].pop(0)
                    v.position += v.speed * speed_mul
                    self.metrics["throughput"] += 1
            else:
                for v in self.queue[lane]:
                    v.waiting_time += 1
                    self.metrics["avg_wait"] += 1
            for v in list(self.queue[lane]):
                if random.random() < breakdown_prob:
                    v.broken = True
                    if random.random() < 0.05:
                        self.metrics["collisions"] += 1
        for p in self.pedestrians:
            if random.random() < 0.01:
                lane = random.choice(self.lanes)
                for v in self.queue[lane]:
                    v.waiting_time += 1
                    self.metrics["avg_wait"] += 1
        self.time += 1
        return self.metrics

    def get_state(self):
        state = {
            "time": self.time,
            "queues": {lane: len(self.queue[lane]) for lane in self.lanes},
            "throughput": self.metrics["throughput"],
            "collisions": self.metrics["collisions"],
            "avg_wait": (self.metrics["avg_wait"] / max(1, sum(len(self.queue[l]) for l in self.lanes)))
        }
        return state
