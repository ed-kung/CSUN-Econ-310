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
    <option value="lec01">1. Econ Review</option>
	<option value="lec02">2. Math Review</option>
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
