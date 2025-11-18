---
layout: default
title: Random Problem Generator
nav_order: 5
python: pyscript
---

# Random Problem Generator

<dialog id="loading">
<p><img src="/CSUN-Econ-310/assets/images/loading-wheel.gif" width="100"></p>
</dialog>

<label for="dropdown">Generate problem from lecture:</label>

<select id="dropdown">
	<option value="math-review">Math Review</option>
	<option value="single-variable-optimization">Single Variable Optimization</option>
	<option value="commodity-market">Commodity Market Models</option>
	<option value="labor-market">Labor Market Models</option>
	<option value="general-equilibrium">General Equilibrium Models</option>
	<option value="productivity-shocks">Application: Productivity Shocks</option>
	<option value="multivariate-optimization-1">Multivariate Optimization</option>
	<option value="multivariate-optimization-2">Constrained Multivariate Optimization</option>
	<option value="consumer-theory">Consumer Choice Theory</option>
	<option value="consumer-theory-applications">Consumer Choice: Applications</option>
	<option value="labor-leisure">Labor/Leisure Choice</option>
	<option value="consumption-savings">Consumption and Savings</option>
	<option value="production-theory">Theory of Production</option>
	<option value="monopolies">Monopolies</option>
	<option value="game-theory-1">Game Theory</option>
	<option value="imperfect-competition-1">Imperfect Competition I</option>
	<option value="risk-and-uncertainty">Risk and Uncertainty</option>
</select>

<button id="button" pys-onClick="generate_problem">Generate</button>

<p><h3>Problem:</h3></p>

<div id="problem">
</div>

---

<details id="details">
<summary>Solution:</summary>
<div id="solution">
</div>
</details>

<script type="py" src="/CSUN-Econ-310/rpg.py" config="/CSUN-Econ-310/rpg.toml">
</script>
