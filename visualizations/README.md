# Visualizations

Collection of scripts and HTML outputs for animated surfaces and heatmaps.

---
## Contents

- **3D_surface_slider.py** – Interactive 3D surface with a slider for thresholds.

- **animated_3D_plot.html** – Saved interactive 3D plot.

- **animated_heatmap.gif** – Animated heatmap as a GIF.

- **animated_heatmap.html** – Interactive heatmap export.

- **heatmap_slider.py** – Heatmap with adjustable levels.

- **return_3D_animation.py** – Animation of returns on a surface.

- **return_heatmap_animation.py** – Heatmap of returns over time.

- **return_plot.html** – Static return plot.

- **Simple_3D_surface.py** – Minimal 3D surface example.

---
## Requirements
Install dependencies from requirements.txt:

pip install -r requirements.txt

requirements.txt should contain:
- [x] numpy
- [x] plotly
- [x] imageio

(os is part of Python’s standard library and doesn’t need to be listed.)

---
## Setup
Clone the repository and navigate to this folder:

git clone https://github.com/mbernier4453/Projects.git

cd Projects/VISUALIZATIONS
python -m venv venv
source venv/bin/activate (Windows: venv\Scripts\activate)
pip install -r requirements.txt

---
## Usage
Run any Python script to generate visualizations:

python 3D_surface_slider.py

Open any .html file in a browser to view saved interactive plots.

---
## Notes
Python 3.10+ recommended.
Scripts may open visualizations in a browser as an HTML file or save as GIF depending on the file.
---