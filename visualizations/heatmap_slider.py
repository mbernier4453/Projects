import numpy as np
import plotly.graph_objects as go

# Data setup
sell = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95] 
buy = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5] 
# Meshgrid is not needed for a heatmap
num_periods = 30

original_returns = np.array([
    [28.0, 24.5, 22.0, 20.5, 19.5, 28.0, 24.5, 22.0, 20.5, 19.5],
    [27.5, 24.0, 21.8, 20.3, 19.3, 27.5, 24.0, 21.8, 20.3, 19.3],
    [27.0, 23.5, 21.5, 20.0, 19.0, 27.0, 23.5, 21.5, 20.0, 19.0],
    [26.5, 23.0, 21.2, 19.8, 18.8, 26.5, 23.0, 21.2, 19.8, 18.8],
    [26.0, 22.5, 21.0, 19.5, 18.5, 26.0, 22.5, 21.0, 19.5, 18.5],
    [28.0, 24.5, 22.0, 20.5, 19.5, 28.0, 24.5, 22.0, 20.5, 19.5],
    [27.5, 24.0, 21.8, 20.3, 19.3, 27.5, 24.0, 21.8, 20.3, 19.3],
    [27.0, 23.5, 21.5, 20.0, 19.0, 27.0, 23.5, 21.5, 20.0, 19.0],
    [26.5, 23.0, 21.2, 19.8, 18.8, 26.5, 23.0, 21.2, 19.8, 18.8],
    [26.0, 22.5, 21.0, 19.5, 18.5, 26.0, 22.5, 21.0, 19.5, 18.5]
])

# Create a moving peak in the center over time
trending_returns = []
peak_max_value = 10 
for i in range(num_periods):
    peak_modifier = peak_max_value * np.sin(np.pi * i / (num_periods - 1))
    new_returns = original_returns.copy()
    new_returns[4:6, 4:6] += peak_modifier
    trending_returns.append(new_returns)
all_returns = np.array(trending_returns)


# Figure setup

# 1. Initialize the heatmap with the first period
fig = go.Figure(data=[go.Heatmap(
    x=sell,
    y=buy,
    z=all_returns[0], 
    colorscale='RdYlGn',
    zmin=np.min(original_returns),
    zmax=np.max(original_returns) + peak_max_value,
    colorbar=dict(title='Return')
)])

# 2. Build animation frames
frames = []
for i in range(num_periods):
    frame = go.Frame(
        # Each frame updates the heatmap z values
        data=[go.Heatmap(z=all_returns[i])],
        name=f'Period {i+1}'
    )
    frames.append(frame)
fig.frames = frames

# 3. Add a slider and play/pause controls
sliders = [{'steps': [{'method': 'animate', 'args': [[f'Period {i+1}'], {'frame': {'duration': 120, 'redraw': True}, 'mode': 'immediate'}], 'label': str(i+1)} for i in range(num_periods)], 'active': 0, 'currentvalue': {'prefix': 'Period: '}, 'pad': {'t': 50}}]
updatemenus = [{'type': 'buttons', 'buttons': [{'label': 'Play', 'method': 'animate', 'args': [None, {'frame': {'duration': 120, 'redraw': True}, 'transition': {'duration': 0}, 'mode': 'immediate'}]}, {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]}]}]

# 4. Layout and styling
fig.update_layout(
    title='Return Heatmap',
    xaxis_title='Sell values',
    yaxis_title='Buy values',
    sliders=sliders,
    updatemenus=updatemenus,
    template='plotly_dark',
    paper_bgcolor='rgb(30,30,30)',
    plot_bgcolor='rgb(30,30,30)',
    # Reverse y so higher buy values appear at the top
    yaxis=dict(autorange='reversed')
)

# Save the output HTML
fig.write_html("animated_heatmap.html")

print("Successfully created animated_heatmap.html")
