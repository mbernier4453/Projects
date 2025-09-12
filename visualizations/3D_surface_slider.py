import numpy as np
import plotly.graph_objects as go

# Build an animated 3D surface that shows how returns change as buy/sell thresholds evolve over time.

# Discrete sell and buy thresholds (x/y axes of the surface)
sell = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
buy = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5]
X, Y = np.meshgrid(sell, buy)  # grid for plotting
num_periods = 30  # number of animation frames

# Base return surface used as the starting point for all periods
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

# Create a time series of surfaces by adding a moving peak to the center region
trending_returns = []
peak_max_value = 10  # maximum height added to the peak area over time
for i in range(num_periods):
    # Smoothly vary the peak using a half sine wave across the animation
    peak_modifier = peak_max_value * np.sin(np.pi * i / (num_periods - 1))
    new_returns = original_returns.copy()
    new_returns[4:6, 4:6] += peak_modifier  # boost a 2x2 center block to simulate a shifting hotspot
    trending_returns.append(new_returns)
all_returns = np.array(trending_returns)

# Initial surface for frame 1, with a fixed colorscale and bounds for consistent coloring across frames
fig = go.Figure(data=[go.Surface(
    x=X,
    y=Y,
    z=all_returns[0],
    colorscale='RdYlGn',
    cmin=np.min(original_returns),
    cmax=np.max(original_returns) + peak_max_value
)])

# One frame per period, updating only the Z values
frames = [
    go.Frame(data=[go.Surface(z=all_returns[i])], name=f'Period {i+1}')
    for i in range(num_periods)
]
fig.frames = frames

# Slider to scrub through periods; each step triggers an animation to that frame
sliders = [{
    'steps': [{
        'method': 'animate',
        'args': [[f'Period {i+1}'],
                 {'frame': {'duration': 50, 'redraw': True},
                  'mode': 'immediate'}],
        'label': str(i + 1)
    } for i in range(num_periods)],
    'active': 0,
    'currentvalue': {'prefix': 'Period: '},
    'pad': {'t': 50}
}]

# Play/Pause buttons for the animation
updatemenus = [{
    'type': 'buttons',
    'buttons': [
        {'label': 'Play',
         'method': 'animate',
         'args': [None, {'frame': {'duration': 50, 'redraw': True},
                         'transition': {'duration': 0},
                         'mode': 'immediate'}]},
        {'label': 'Pause',
         'method': 'animate',
         'args': [[None], {'frame': {'duration': 0, 'redraw': False},
                           'mode': 'immediate'}]}
    ]
}]

# Layout: axis ranges, camera angle, aspect ratio, theme, and interactive controls
fig.update_layout(
    title='Return Surface (Interactive)',
    scene=dict(
        xaxis=dict(range=[np.min(X), np.max(X)], title='Sell Values'),
        yaxis=dict(range=[np.min(Y), np.max(Y)], title='Buy Values'),
        zaxis=dict(range=[np.min(original_returns),
                          np.max(original_returns) + peak_max_value],
                    title='Returns (%)'),
        camera=dict(eye=dict(x=2.5, y=2.5, z=2.5)),
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=0.7)
    ),
    sliders=sliders,
    updatemenus=updatemenus,
    template='plotly_dark',
    paper_bgcolor='rgb(30,30,30)',
    plot_bgcolor='rgb(30,30,30)'
)

# Export to a standalone HTML file that contains the interactive, animated plot
fig.write_html("animated_3D_plot.html")
print("Successfully created animated_3D_plot.html with an adjusted camera view.")
