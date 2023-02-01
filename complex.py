import math


def str_to_complex(line: str):
    line = line.strip(' ').strip('+').rstrip('-')

    str_num = ''
    if line[0] == '-':
        str_num += '-'
        line = line.lstrip('-')

    _real = 0
    _imag = 0

    for c in line:
        if c in ['+', '-']:
            if str_num in ['', '+', '-']:
                if c == '-' and str_num == '':
                    str_num += c
                continue
            _real = float(str_num)
            str_num = ''
            if c == '-':
                str_num += '-'
            continue
        if c == 'i':
            if str_num.strip(' ') in ['', '-', '+']:
                _imag += float(str_num + '1')
                continue
            _imag += float(str_num)
            str_num = ''
            continue
        str_num += c

    if str_num not in ['+', '-', '']:
        _real = float(str_num)
    return Complex(re=_real, im=_imag)


def i():
    return Complex(re=0, im=1)


class Complex:
    real: float
    imag: float
    repr_precision = 8

    def __init__(self, *args, **kwargs):
        if not kwargs:
            z = str_to_complex(args[0])
            self.real = z.real
            self.imag = z.imag
        else:
            self.real = kwargs['re'] if ('re' in kwargs) else 0
            self.imag = kwargs['im'] if ('im' in kwargs) else 0

    def __repr__(self):
        _real = self.real
        _imag = self.imag

        if _real == int(_real):
            _real = int(_real)

        if _imag == int(_imag):
            _imag = int(_imag)

        _real_str = f'{round(_real, self.repr_precision)}'
        _imag_str = f'{round(_imag, self.repr_precision)}'

        try:
            if float(_real_str) == int(float(_real_str)):
                _real_str = str(int(float(_real_str)))
        except ValueError:
            pass

        try:
            if float(_imag_str) == int(float(_imag_str)):
                _imag_str = str(int(float(_imag_str)))
                _imag = int(_imag_str)
        except ValueError:
            pass

        if _imag == 0:
            return f'{_real_str}'
        if _real == 0:
            return f'{_imag_str}i'

        if _imag > 0:
            return f'{_real_str}+{_imag_str}i'

        return f'{_real_str}-{round(abs(_imag), self.repr_precision)}i'

    def __add__(self, other):
        z = Complex(re=self.real, im=self.imag)
        if isinstance(other, Complex):
            z.real += other.real
            z.imag += other.imag
        elif isinstance(other, float | int):
            z.real += other
        elif isinstance(other, str):
            z = z.__add__(str_to_complex(other))
        return z

    def __sub__(self, other):
        if isinstance(other, Complex):
            return self.__add__(-other)
        elif isinstance(other, float | int):
            return self.__add__(Complex(re=-other, im=0))
        elif isinstance(other, str):
            return self.__sub__(str_to_complex(other))

    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(re=(self.real * other.real - self.imag * other.imag),
                           im=(self.imag * other.real + self.real * other.imag))
        elif isinstance(other, float | int):
            return Complex(re=self.real * other, im=self.imag * other)
        elif isinstance(other, str):
            return self.__mul__(str_to_complex(other))

    def __truediv__(self, other):
        if isinstance(other, Complex):
            denominator = other.real ** 2 + other.imag ** 2
            re = self.real * other.real + self.imag * other.imag
            im = other.real * self.imag - self.real * other.imag
            return Complex(re=re / denominator, im=im / denominator)
        elif isinstance(other, float | int):
            return Complex(re=self.real / other, im=self.imag / other)
        elif isinstance(other, str):
            return self.__truediv__(str_to_complex(other))

    def _pow_complex(self, other):
        r = abs(self)
        theta = self.arg()

        c = other.real
        d = other.imag

        ln = math.log(r, math.e)

        z = Complex(re=(c * ln - d * theta),
                    im=(d * ln + c * theta))

        return z._exp_e()

    def __pow__(self, power, modulo=None):
        if isinstance(power, Complex):
            return self._pow_complex(power)
        elif isinstance(power, float):
            ln = math.log(self.mag(), math.e)
            return Complex(re=power * ln, im=power * self.arg())._exp_e()
        elif not isinstance(power, int):
            print("unrecognized power type")
            raise Exception(f"Power number type should be [int], [float] or [Complex], not {type(power)}")

        if power == 0:
            return Complex(re=1, im=0)
        elif power == 1:
            return self
        elif power == 2:
            return self * self

        if self.imag == 0:
            return Complex(re=self.real ** power, im=0)

        if power % 2 == 0:
            return self.__pow__(power // 2) ** 2
        else:
            return (self.__pow__(power // 2) ** 2) * self

    def __str__(self):
        return self.__repr__()

    def __neg__(self):
        return Complex(re=-self.real, im=-self.imag)

    def mag(self):
        return math.sqrt(self.real ** 2 + self.imag ** 2)

    def arg(self):
        """
        Returns degree of an angle in trigonometry form of complex number, in radians.
        :return: Returns angle of complex number in [rad].
        """
        return math.atan2(self.imag, self.real)

    def to_trig(self) -> tuple:
        return self.mag(), self.arg()

    def __abs__(self):
        return self.mag()

    def __invert__(self):
        return Complex(re=self.real, im=-self.imag)

    def re(self):
        return self.real

    def real(self):
        return self.real

    def im(self):
        return self.imag

    def imag(self):
        return self.imag

    def roots(self, degree: int) -> list:
        mag = self.mag() ** (1. / degree)
        alpha = math.atan2(self.imag, self.real)

        out = []
        for k in range(0, degree):
            phi = (alpha + 2 * math.pi * k) / degree
            _sin = math.sin(phi)
            if float(f'{math.sin(phi):.10f}') in [0, 3.1415926535]:
                _sin = 0
            # custom _sin variable is required because of floating point pi
            # sin error: sin(0) is 1.2246467991473532e-16, and so we need to correct this exact error,
            # but don't touch perfectly working math.cos()
            out.append(Complex(re=mag * math.cos(phi), im=mag * _sin))
        return out

    def _exp_e(self, base: float = math.e):
        b = self.real
        c = self.imag
        ln = 1 if base == math.e else math.log(base, math.e)
        return Complex(re=math.cos(c * ln), im=math.sin(c * ln)) * (base ** b)

    def __rpow__(self, other):
        return self._exp_e(other)

    def __rmul__(self, other):
        return self * other

    def __rsub__(self, other):
        return -(self - other)

    def __radd__(self, other):
        return self + other

    def __rtruediv__(self, other):
        return Complex(re=other) / self
