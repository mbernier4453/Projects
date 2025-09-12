import numpy as np  # math stuff
import plotly.graph_objects as go  # plotly figure API

# Data for the 3D surface
# Indicator values
sell = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]  # x-axis levels I sweep for sell
buy = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5]   # y-axis levels I sweep for buy

# fake data for returns
returns = np.array([
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
])  # rows map to buy, cols map to sell

# Create meshgrid for 3D surface
X, Y = np.meshgrid(sell, buy)  # make coordinate grid so each z maps to a (sell,buy) pair

# Create the 3D surface plot
fig = go.Figure(data=[go.Surface(
    x=X,
    y=Y,
    z=returns,            # surface heights
    colorscale='viridis'  # readable gradient, dark-to-light
)])

# Update layout
fig.update_layout(
    title='Return Surface',  # I swap this title per metric when I loop (Sharpe, Sortino, etc)
    scene=dict(
        xaxis_title='Sell Values',
        yaxis_title='Buy Values',
        zaxis_title='Returns (%)',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.2)  # initial view angle so the surface looks clean
        )
        # note: if I need equal scaling, I can set aspectmode='cube' or 'manual' here
    ),
    width=800,   # canvas size in pixels
    height=600,  # tweak if I want a wider view
    template='plotly_dark',
    paper_bgcolor='rgb(30,30,30)',
    plot_bgcolor='rgb(30,30,30)'
)

# Show the plot
# New, more reliable line
fig.write_html("return_plot.html")  # export to html so I can open it full-screen in a browser
print("Successfully created return_plot.html")