# GrandMA2 macro compiler/decompiler + VSC syntax highlights

The tool `ma2Compiler.py` aims to compile (.ma2macro file -> GrandMA2 XML import) and decompile (GrandMA2 XML export -> .ma2macro file) GrandMa2 macros to edit them more easily on any normal file editor. This repository also supplies a syntax highlighter plugin for VScode for better readability.

# Tool installation

Just run `pip install beautifulsoup4 lxml argparse` in your venv/python installation to download the needed libraries

# VsCode extension installation

Just install it from: https://marketplace.visualstudio.com/items?itemName=stranck.ma2-macro

# Usage

Tldr: `python ma2Compiler.py --file <input file> [-c|d] [--output <output file>]`

- Using the flag `--file` (Or `-f`) you specify the source file we have to compile/decompile
- You must specify or the flag `--compile` (`-c`) or the flag `--decompile` (`-d`) to chose the desired operation
- By default the results are outputted on STDOUT. Using the flag `--output` (`-o`) you can write directly on a destination file

# The language

The `.ma2macro` file follows the following rules:

- Each macro should be written in a Macro block, which is defined as `_macro "MACRO NAME HERE" { YOUR CODE HERE }`
- Each line inside a macro block represents a line in a MA2 macro, even empty lines
- A line can start with a `#`, which marks that macro line as "Disabled" in ma2. The line will still be parsed and later imported in the console
- You can optionally specify a comment at the end of the line, using a `//`. Everything after the double slashes will be put inside the "Info" column of the ma2 macro
- Before a comment, you can specify the wait time for the macro line, using a `!`. The time should be expressed using dots as a separator. An example: `ClearAll !1.5 //The clear all command will be executed 1.5secs after the previous line`

Example code:
```
_macro "Create odd group" {
	# +++++ FRONT +++++
	ClearAll
	Group "Spot group"
	MAtricks "Odd" //Selects only the first half of the lights
	Store Group "Spot group - odd" /o
	MAtricks "Reset" !0.25 //We wait a bit to be sure the store is successful
	ClearAll !0.25
}

_macro "Create even group" {
	# +++++ FRONT +++++
	ClearAll
	Group 20
	MAtricks "Even" //Selects instead the second half of the lights
	Store Group "Spot group - even" /o
	MAtricks 1 !0.25 //We wait a bit to be sure the store is successful
	ClearAll !0.25
}
```

# Important note

I wrote the python script in one hour while bored during uni. It WILL break, specially on complex macros. Don't judge me plz and don't ask rudely for fixes. Talk is cheap, send patches