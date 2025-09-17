import streamlit as st
import subprocess, json, os, time, threading

st.set_page_config(layout="wide", page_title="Climate+Crowd Traffic Twin")
st.title("🌧️ Climate + Crowd Resilient Smart Traffic Twin (Demo)")

with st.sidebar:
    st.header("Scenario Controls")
    steps = st.number_input("Steps (समय अवधि)", min_value=50, max_value=2000, value=300, step=50)
    st.caption("यह सिमुलेशन के चलने की अवधि निर्धारित करता है")
    
    weather = st.selectbox("Weather (मौसम)", ["clear","rain","heat"])
    st.caption("मौसम की स्थिति: clear (साफ), rain (बारिश), heat (गर्मी)")
    
    crowd = st.slider("Crowd surge (भीड़ का स्तर)", 0.0, 1.0, 0.0, 0.1)
    st.caption("0.0 = सामान्य भीड़, 1.0 = अधिकतम भीड़ (दोगुनी)")
    st.caption("अधिक भीड़ होने पर ट्रैफिक प्रभावित होता है")
    
    start = st.button("Start Simulation (सिमुलेशन शुरू करें)")

if "running" not in st.session_state:
    st.session_state.running = False

placeholder = st.empty()

def run_sim_thread(steps, weather, crowd):
    cmd = ["python", "src/run_sim.py", "--steps", str(steps), "--weather", weather, "--crowd", str(crowd)]
    proc = subprocess.Popen(cmd)
    proc.wait()

if start and not st.session_state.running:
    st.session_state.running = True
    placeholder.info("Simulation started... (check console for logs)")
    thread = threading.Thread(target=run_sim_thread, args=(steps, weather, crowd))
    thread.start()
    for i in range(1000):
        if os.path.exists("results/sim_out.json"):
            break
        time.sleep(0.2)
    if os.path.exists("results/sim_out.json"):
        data = json.load(open("results/sim_out.json"))
        st.success("Simulation finished, loading results...")
        last = data["metrics_log"][-1]
        st.write("Final state:", last["state"])
        st.write("Final metrics:", last["metrics"])
        times = [m["t"] for m in data["metrics_log"]]
        throughput = [m["metrics"]["throughput"] for m in data["metrics_log"]]
        import pandas as pd
        df = pd.DataFrame({"t":times, "throughput":throughput})
        
        # Adding chart with proper labels
        st.subheader("Traffic Throughput Over Time (समय के साथ ट्रैफिक प्रवाह)")
        st.caption("X-axis: Time Steps (समय) | Y-axis: Vehicles Throughput (वाहनों की संख्या)")
        chart = st.line_chart(df.set_index("t"))
        
        # Adding more metrics visualization
        if "avg_wait" in last["metrics"]:
            st.subheader("Average Wait Time (औसत प्रतीक्षा समय)")
            st.metric("Average Wait Time", f"{last['metrics']['avg_wait']:.2f} seconds")
    else:
        st.error("Simulation did not produce results in time.")
    st.session_state.running = False
