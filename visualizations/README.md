# Visualizations

Collection of scripts and HTML outputs for animated surfaces and heatmaps.

---
## Contents

- **3D_surface_slider.py** – Interactive 3D surface with a slider for thresholds.
- **Simple_3D_surface.py** – Minimal 3D surface example.
- **animated_3D_surface_gif.py** – Script to make 3D animated GIFs.
- **animated_3D_plot.html** – Saved interactive 3D plot.
- **animated_heatmap.gif** – Animated heatmap as a GIF.
- **animated_heatmap.html** – Interactive heatmap export.
- **animated_heatmap_gif.py** – Script to generate heatmap GIFs.
- **heatmap_slider.py** – Heatmap with adjustable levels.
- **return_3D_animation.gif** – Animation of returns on a surface.
- **return_heatmap_animation.gif** – Heatmap of returns over time.
- **return_plot.html** – Static return plot.
- **requirements.txt** – Package requirements.

---
## Requirements
Install dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```
requirements.txt should contain:
- [x] numpy
- [x] plotly
- [x] imageio

(os is part of Python’s standard library and doesn’t need to be listed.)

---
## Setup
Clone the repository and create a virtual environment:
```
git clone https://github.com/mbernier4453/Projects.git
```
```bash
cd Projects/visualizations
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows cmd
.\venv\Scripts\Activate.ps1    # Windows PowerShell
pip install -r requirements.txt
```
---
## Usage
Run any Python script to generate visualizations:
```bash
python 3D_surface_slider.py
```
Open any .html file in a browser to view saved interactive plots.

GIF files can be opened in any image viewer.

---
## Notes

Python 3.10+ recommended.

Scripts may open visualizations in a browser as an HTML file or save as GIF depending on the file.

---



