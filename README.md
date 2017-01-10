# ScientificCalculator
Scientific calculator written in python

## Usage
clone the repository and cd into the project directory.
Run the REPL environment with the following command:

```
$ python calc.py
```

You can enter expressions as demonstrated below

```
> 72 * 3 / 9 * (6 + 4)
240.0
```

At this point in time the calculator supports the following operations:

| command | usage | description
|---|---|---|
| ans | ans() | returns the last evaluated answer
| exit | exit() | exits the REPL
| average / mean | mean(x, y, ...) | returns the mean value of given expressions
| sum | sum(x, y, ...) | returns the sum of the given expressions
| add | x + y | adds left operand to right operand
| subtract | x - y | subtracts left operand from right operand
| multiply | x * y | multiplies left operand by right operand
| divide | x / y | divides left operand byt right operand
| remainder | x % y | remainder of left operand divided by right operand

expressions can be passed to the calculator via the command line too:

```
$ python calc.py "1 + 2"
3.0
```