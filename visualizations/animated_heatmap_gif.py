import numpy as np
import plotly.graph_objects as go
import os
import imageio

def generate_heatmap_data(num_periods=30, peak_max_value=10):
    """
    Generate a time series of 10x10 heatmaps by adding a smooth, sinusoidal peak
    to the center of a base return matrix. Returns sell values, buy values,
    the stacked time series array, and the unmodified base matrix.
    """
    sell_values = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95] 
    buy_values = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5] 
    
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

    # Build a trend by boosting the 2x2 center region with a sinusoidal amplitude
    trending_returns = []
    for i in range(num_periods):
        peak_modifier = peak_max_value * np.sin(np.pi * i / (num_periods - 1))
        new_returns = original_returns.copy()
        new_returns[4:6, 4:6] += peak_modifier
        trending_returns.append(new_returns)
    
    all_returns = np.array(trending_returns)

    return sell_values, buy_values, all_returns, original_returns

def main():
    """
    Generate data, render per-period heatmap frames, assemble them into a GIF,
    and remove temporary files.
    """
    # 1. Parameters and paths
    peak_max_value = 10
    num_periods = 30
    output_gif_filename = 'return_heatmap_animation.gif'
    temp_image_folder = 'heatmap_frames'

    # Generate the dataset
    sell, buy, all_returns_data, original_returns_data = generate_heatmap_data(num_periods, peak_max_value)
    
    # Ensure the temporary frame directory exists
    if not os.path.exists(temp_image_folder):
        os.mkdir(temp_image_folder)

    # 2. Create the initial heatmap figure using the first frame
    fig = go.Figure(data=[go.Heatmap(
        x=sell,
        y=buy,
        z=all_returns_data[0],  # first frame
        colorscale='RdYlGn',
        zmin=np.min(original_returns_data),
        zmax=np.max(original_returns_data) + peak_max_value,
        colorbar=dict(title='Return')
    )])

    fig.update_layout(
        title='Return Heatmap',  # will be updated per frame for different periods or metrics
        xaxis_title='Sell values',
        yaxis_title='Buy values',
        template='plotly_dark',
        paper_bgcolor='rgb(30,30,30)',
        plot_bgcolor='rgb(30,30,30)',
        yaxis=dict(autorange='reversed')  # show higher buy values at the top
    )

    # 3. Update z-data and title per period and write each frame as a PNG
    filenames = []
    for i in range(num_periods):
        fig.data[0].z = all_returns_data[i]
        fig.update_layout(title_text=f'Return Heatmap - Period {i+1}')
        filename = f"{temp_image_folder}/frame_{i:02d}.png"
        filenames.append(filename)
        fig.write_image(filename)

    print(f"Generated {len(filenames)} frames.")

    # 4. Stitch frames into a GIF
    with imageio.get_writer(output_gif_filename, mode='I', duration=0.12, loop=0) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    print(f"Successfully created {output_gif_filename}")

    # 5. Delete temporary frames and folder
    for filename in filenames:
        os.remove(filename)
    os.rmdir(temp_image_folder)

if __name__ == '__main__':
    main()
