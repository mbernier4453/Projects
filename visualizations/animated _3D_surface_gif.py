import numpy as np
import plotly.graph_objects as go
import os
import imageio

# Data setup
sell = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95] 
buy = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5] 
X, Y = np.meshgrid(sell, buy)  # grid of sell (x) and buy (y) values
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

# Add a moving peak in the center to create a visible trend over time
trending_returns = []
for i in range(num_periods):
    peak_modifier = 10 * np.sin(np.pi * i / (num_periods - 1))  # smooth rise and fall
    new_returns = original_returns.copy()
    new_returns[4:6, 4:6] += peak_modifier  # boost a 2x2 center region
    trending_returns.append(new_returns)
all_returns = np.array(trending_returns)


# GIF setup
if not os.path.exists("images"):
    os.mkdir("images")

# Build the initial surface using the first period
fig = go.Figure(data=[go.Surface(
    x=X, y=Y, z=all_returns[0], 
    colorscale='RdYlGn',
    cmin=np.min(original_returns),
    cmax=np.max(original_returns) + 10
)])

# Layout and styling
fig.update_layout(
    title='Return Surface',  # reused for different metrics like Sharpe or Sortino in other runs
    autosize=False,
    scene=dict(
        # Manually set axis ranges and labels
        xaxis=dict(range=[np.min(X), np.max(X)], title='Sell values'),
        yaxis=dict(range=[np.min(Y), np.max(Y)], title='Buy values'),
        zaxis=dict(range=[np.min(original_returns), np.max(original_returns) + 10], title='Returns (%)'),
        
        camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=0.7)
    ),
    template='plotly_dark', paper_bgcolor='rgb(30,30,30)', plot_bgcolor='rgb(30,30,30)'
)

# Render each period to a PNG frame
filenames = []
for i in range(num_periods):
    fig.data[0].z = all_returns[i]
    filename = f"images/frame_{i:02d}.png"
    filenames.append(filename)
    fig.write_image(filename)

print(f"Generated {num_periods} frames.")

# Assemble frames into an animated GIF
with imageio.get_writer('return_3D_animation.gif', mode='I', duration=0.05, loop=0) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

print("Successfully created return_3D_animation.gif")

# Remove temporary frame files and folder
for filename in filenames:
    os.remove(filename)
os.rmdir("images")
