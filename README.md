# WFF Parser
A small parser and solver for well-formed forumlas (WFF) in philosopical language, written in Python.

## Example
```python
from solver import Solver

s = Solver()
s.add_premise('A -> B')
s.add_premise('A')
s.set_conclusion('B')

valid = s.solve()
```

## Usage
### Parsing
To just parse a sentence into the computer readable format (or check if the sentence is well formed), create a Parser object and call `parse()` on it with a supplied sentence.
```python
p = Parser()
p.parse(sentence)
``` 
Any syntax errors in the sentence will be found and reported. 
The parser's definition can be set during object creation, such as `Parser('formal')`. By default, the parser will use the informal definition for WFFs. See Definitions for more.

### Solving
To solve a set of premise sentences with a conclusion, create a Solver object. Then, set as many premises as wanted and only one conclusion. 
The `solve()` method will return whether or not the premises and conclusion make a valid argument.

See the Example above for an example.

## Definitions
The parser uses the concept of a definition to handle the tokenizing and parsing strategy. The definition, as held in the `definitions.yaml` file have the following:
 - name: human readable name for the definition.
 - allow-drop-outer-grouping: whether or not this definition is allowed to drop the outermost grouping symbols, if applicable.
 - tokens: a dictionary of all operations and usable token definintions for said operator.

Examples can be found in the `definitions.yaml` file. Two are provided with the program: `formal`, and `informal`.

## Future Improvements
 - Solver definition setting: small chore to add supplying which definition to use for the solver
 - Better error reporting: more similiar to regular compilers where it shows which token caused the tokenizer/parser to fail
 - Short table method: try solving tables from the bottom up instead of top down (start with sentences, not sentence letters)
 - Custom operators: add support for user-defined operators, such as XOR. A much later problem.
