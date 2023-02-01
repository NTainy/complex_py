# Complex numbers pylib

Python library with a single class that represents complex numbers - ```complex.Complex```

Class consists of following methods:

### Number constructor
* ```Complex(re=x, im=y)``` creates ```z = x + yi```. If you omit ```re``` or ```im```,
corresponding part of the number will be set to 0 by default.
* ```Complex('x+yi')``` creates ```z = x + yi```, too. This
method auto-parses strings to numbers.

### Methods
In following parts will be used assumption that numbers
```z, z1, z2, etc.``` are instances of ```Complex```.
#### Re & Im
* ```z.re(), z.real(), z.re``` return real part of the number
* ```z.im(), z.imag(), z.im``` return imaginary part of the number.
#### Trigonometry
* ```abs(z) and z.mag()``` returns the magnitude (== absolute value)
of the complex number ```z```.
* ```z.arg()``` returns the argument of the complex number in `radians`.
* `z.to_trig()` returns `tuple (mag, arg)`
#### Conjugate & negative complex numbers
* `z -> ~z`. `z` and `~z` are conjugate numbers. `~~z == z`.
* Unary operator `-` returns `3-2i -> -3+2i`, `z -> -z`.
#### Operations
> It's sufficient to have only one complex number in any of operations.
> You don't have to write `Complex('1+3i') + Complex('2i')`, you can
> write the other component in `float | str | Complex`, e.g.:
> * `Complex('1+3i') + 2.5 == Complex('3.5+3i')`
> * `Complex('1+3i') + '5-7i' == Complex('6-4i')`
> 
> The second component will be auto-parsed to `Complex` type.
> 
> Any operation leaves source numbers immutable, and returns `Complex` number instance.
* Addition - `z1 + z2`
* Subtraction - `z1 - z2`
* Multiplication - `z1 * z2`
* Division - `z1 / z2`
#### Power
> You can raise numbers to the power, there are 3 ways:
> `Real ** Complex`, `Complex ** Real`, `Complex ** Complex`.
* `z1 ** z2` always returns `Complex` instance.

#### Roots
* `z.roots(n) -> list` returns list of roots of `z` of n-th power.
> That means that for every `el` in that list, `el^n == z`, and this
> list contains all solutions to this equation.

#### Additional methods
* `str_to_complex(line: str) -> Complex` - this method parses
strings e.g. `1-4i`, `3i` or `-54i + 23` and returns
corresponding `Complex` complex number instance.
* `i()` is an alias for `i` complex number and returns
`Complex(im=0)` number.

----------------
`NTainy, 2023.`