import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Settings for Simulation Run
st.sidebar.title("Simulation Config")
goal = st.sidebar.number_input("Story Point Goal", 0, value=50)
sprint_history = st.sidebar.text_input("Past Sprint Velocity Values", value="10, 8, 20, 11, 15")
past_sprints = [int(x) for x in sprint_history.split(",")]
num_sim_runs = st.sidebar.number_input("Simulation Runs", 50, value=60, max_value=600)


def burn_up(target):
    burnup = []
    total = 0
    while total < target:
        sprint = np.random.choice(past_sprints)
        total += sprint
        burnup.append(sprint)
    return burnup


def simulate(num_sim_runs, story_point_goal):
    return [burn_up(story_point_goal) for _ in range(num_sim_runs)]


def cum_prob(histogram, total):
    return np.cumsum(histogram / total)


data = simulate(num_sim_runs, goal)

counts = list(map(len, data))

max_sprints = max(counts) + 2
(hist, _) = np.histogram(counts, bins=range(1, max(counts) + 2))

probs = cum_prob(hist, num_sim_runs)

sprint = []
runs = []
burnups = []

for (i, run) in enumerate(data):
    for (j, k) in enumerate(np.cumsum(run)):
        runs.append(f"run{i}")
        sprint.append(j + 1)
        burnups.append(k)

df = pd.DataFrame({
    'Sprint': sprint,
    'Runs': runs,
    'Burnups': burnups
})

fig = px.line(df, x="Sprint", y="Burnups", color="Runs", line_group="Runs", title="Number of Sprints to Reach Goal")
fig.update_layout(showlegend=False)
fig.add_hline(y=goal)

st.title("Sprint Simulation")

st.plotly_chart(fig, use_container_width=True)

fig2 = px.area(x=[p + 1 for p in range(len(probs))],
               y=probs,
               labels={'x': 'Sprint', 'y': 'Probability'},
               title="Probability of Achieving Goal")
fig2.add_hline(y=0.5, annotation_text="50%", annotation_position="bottom right", line_color="orange")
fig2.add_hline(y=0.85, annotation_text="85%", annotation_position="bottom right", line_color="green")
fig2.update_xaxes(tick0=1, dtick=0.5)
fig2.update_yaxes(tick0=0, dtick=0.1)
st.plotly_chart(fig2, use_container_width=True)
