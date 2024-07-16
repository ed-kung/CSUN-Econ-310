---
layout: default
title: pyscript example
nav_order: 5
python: pyscript
---

# Pyscript Example

<label for="problem_selection">Generate problem for lecture:</label>

<select id="problem_selection">
    <option value="01_math_review">1. Math Review</option>
    <option value="02_single_variable_optimization">2. Single Variable Optimization</option>
    <option value="03_supply_curves">3. Supply Curves</option>
</select>

<button id="generate_button" pys-onClick="generate_problem">Generate</button>

<p><h3>Problem:</h3></p>

<div id="problem">
</div>

---

<details>
<summary>Solution:</summary>
<div id="solution">
</div>
</details>

<script type="py" src="/CSUN-Econ-310/main.py" config="/CSUN-Econ-310/pyscript.toml">
</script>
