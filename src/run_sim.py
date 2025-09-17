import argparse, json, time, os
import sys
sys.path.append('.')
from sim.core import Environment
from controller.rl_agent_stub import RLAgentStub

def run(config_path, steps, weather, crowd):
    with open(config_path, 'r') as f:
        cfg = json.load(f)
    cfg['steps'] = steps
    cfg['weather'] = weather
    if crowd:
        cfg['num_pedestrians'] = int(cfg.get('num_pedestrians',50) * (1.0 + crowd))
    env = Environment(cfg)
    agent = RLAgentStub()
    metrics_log = []
    for t in range(steps):
        state = env.get_state()
        action = agent.act(state)
        metrics = env.step(action)
        if t % 10 == 0:
            print(f"t={t}, state={state}, metrics={metrics}")
        metrics_log.append({"t":t, "state":state, "metrics":metrics.copy()})
        time.sleep(0.01)
    out = {"metrics_log":metrics_log}
    os.makedirs("results", exist_ok=True)
    with open("results/sim_out.json","w") as f:
        json.dump(out,f, indent=2)
    print("Simulation complete. Output saved to results/sim_out.json")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='configs/sample_config.json')
    parser.add_argument('--steps', type=int, default=200)
    parser.add_argument('--weather', default='clear')
    parser.add_argument('--crowd', type=float, default=0.0)
    args = parser.parse_args()
    run(args.config, args.steps, args.weather, args.crowd)
