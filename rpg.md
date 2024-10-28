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

<label for="dropdown">Generate problem from week:</label>

<select id="dropdown">
    <option value="wk01">1. Math Review</option>
    <option value="wk02">2. Supply and Demand Curves</option>
    <option value="wk03">3. Short Run Equlibrium and Taxation</option>
    <option value="wk04">4. Long Run Equilibrium</option>
    <option value="wk06">6. Multivariate Optimization</option>
    <option value="wk07">7. Consumer Theory</option>
    <option value="wk08">8. Consumer Theory Applications</option>
    <option value="wk09">9. Labor-Leisure Choice</option>
    <option value="wk11">11. Monopolies</option>
	<option value="wk12">12. Game Theory & Oligopolies</option>
	<option value="wk13">13. Consumption Smoothing</option>
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
