import os
import json
import numpy as np
from js import MathJax
from pyscript import window, document, when

@when("click", "#button")
def generate_problem():
    
    wk = document.getElementById("dropdown").value
    filename = f"{wk}_practice.json"
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            probs = json.load(f)
        myprob = np.random.choice(probs)
        setup = myprob['setup']
        solution = myprob['solution']
        element = document.getElementById("problem")
        element.innerHTML = setup
        element = document.getElementById("solution")
        element.innerHTML = solution
    else:
        element = document.getElementById("problem")
        element.innerHTML = "Sorry, there aren't any practice problems for this week yet!"
        element = document.getElementById("solution")
        element.innerHTML = ""
    
    element = document.getElementById("details")
    element.removeAttribute('open')
    
    MathJax.typesetPromise()

