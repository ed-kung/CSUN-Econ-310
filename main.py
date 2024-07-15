import panel as pn
import numpy as np
import pandas as pd
import time

pn.extension('mathjax', sizing_mode="stretch_width")

lectures = [
    "1. Math Review",
    "2. Single Variable Optimization",
    "3. Supply Curves",
    "4. Demand Curves"
]

latex_example = r"""
$y = f(x)$
"""

intro_pane = pn.pane.LaTeX(object=r"Generate a problem for lecture:")
intro_pane = "Generate a problem for lecture:"
problem_pane = pn.pane.LaTeX(object=r"Please select a problem type.")
solution_pane = pn.pane.HTML("$$y=f(x)$$", disable_math=False)

problem_selector = pn.widgets.RadioBoxGroup(
    name='RadioBoxGroup',
    options=lectures,
    inline=False
)

generate_button = pn.widgets.Button(
    name='Generate!',
    button_type='primary'
)

def b(event):
    problem_pane.object = fr"You selected {problem_selector.value}."

generate_button.on_click(b)

pn.Column(
    intro_pane, 
    problem_selector, 
    generate_button,
    problem_pane, 
    solution_pane, 
    height=400
).servable(target='problem_generator')

time.sleep(2)
