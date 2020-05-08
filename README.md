# ICSDI - my personal programming language

I'm following this playlist https://www.youtube.com/playlist?list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD

## Building blocks of a programming language

**Lexer**: it goes through the input and divides it into a list of _tokens_. A token in an object characterized by a type and optionally a value.

**Parser**: creates a _syntax tree_ of the program from the tokens created by the Lexer. This tree defines the hierarchy of the operations. More deails about the grammar are in [grammar.txt](https://github.com/albertomosconi/icsdi/blob/master/grammar.txt "details about the grammar").

![syntax tree](https://raw.githubusercontent.com/albertomosconi/icsdi/master/syntax-tree.png "Syntax Tree")
