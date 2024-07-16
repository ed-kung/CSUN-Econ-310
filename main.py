from js import MathJax
from pyscript import window, document, when
import utils

SETUP = r"""
Supply and demand are given by the following equations:

$$\begin{align}
q_d &= 120 - p \\
q_s &= 2p - 30
\end{align}$$

Calculate the equilibrium price and quantity of this market.
"""

@when("click", "#generate_button")
def generate_problem():
    
    prob = utils.SREQ()
    
    problem_selection = document.getElementById("problem_selection").value
    
    element = document.getElementById("problem")
    element.innerHTML = SETUP
    
    element = document.getElementById("solution")
    element.innerHTML = prob.general_solution()

    #child = document.createElement("div")
    #child.innerHTML = f"You selected problem type: {problem_selection}"
    #element = document.getElementById("problem")
    #element.appendChild(child)

    MathJax.typesetPromise()

