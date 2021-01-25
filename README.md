# Readme

Simple python based inference engine

## Usage

To use it as a module checkout to "as_module" branch.

Create a knowledge base json file formated like:
```json
{
	"description": {
		"A": "", // just declares the variable
		"B": "It's raining", // declares and adds a description
		"C": false, // adds a value
		"D": [true, "I have a car"], // value and description
		"E": "",
		"F": ""
	},
	"rules": [
		["A and C", "E"],
		["B or !D", "A"],
		["C and (!B or D)", "F"]
	]
}
```
If you have to do something like "A or !(B and C)", it will cause a syntax error, so do ["B and C", "D"] then "A or !D".

To use the inference engine:
```python
from infeng import Engine
eng = Engine('knoledge_file_path.json')
print(eng.evaluate('A'))
```
