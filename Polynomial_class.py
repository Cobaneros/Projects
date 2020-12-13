class Polynomial:
    def __init__(self, *args):
        self.poly = {}
        for elem in args:
            if isinstance(elem, int):
                for i in range(len(args)):
                    self.poly.update({i: args[i]})
            elif isinstance(elem, list):
                self.poly = dict(enumerate(elem))
            elif isinstance(elem, dict):
                for key in sorted(elem.keys()):
                    self.poly[key] = elem[key]
            elif isinstance(elem, Polynomial):
                self.poly = elem.poly
        j = 0
        self.koefs = list(self.poly.values())
        for elem in self.koefs:
            if elem == -1 and j != 0:
                self.koefs[j] = '-'
            elif elem == 1 and j != 0:
                self.koefs[j] = ''
            j += 1
        k = len(self.koefs) - 1
        while self.poly.get(k, 0) == 0 and k > 0:
            self.poly.pop(k, 0)
            k -= 1

    def __repr__(self):
        self.repr = [self.poly.get(i, 0) for i in range(max(list(self.poly.keys())) + 1)]
        return 'Polynomial' + ' ' + str(self.repr)

    def __str__(self):
        v = self.koefs
        if len(v) == 1:
            return str(v[0])
        else:
            answer = []
            ans = [f'{v[i]}x^{list(self.poly.keys())[i]}' if i != 0 and v[i] != 0 else f'{v[i]}' for i in range(len(v))
                   if v[i] != 0]
            ans = ans[::-1]
            if len(ans) > 1:
                for i in range(2):
                    if ans[-i - 1][-2:] == '^1':
                        ans[-i - 1] = ans[-i - 1][:-2]
            for i in range(len(ans)):
                if '-' not in set(ans[i]) and i != 0:
                    answer.append(f'+ {ans[i]}')
                elif '-' not in set(ans[i]) and i == 0:
                    answer.append(ans[i])
                elif '-' in set(ans[i]) and i == 0:
                    answer.append(f'-{ans[i][1:]}')
                elif '-' in set(ans[i]):
                    answer.append(f'- {ans[i][1:]}')
            if not answer:
                return '0'
            else:
                return ' '.join(answer)

    def degree(self):
        return max(list(self.poly.keys()))

    def __add__(self, other):
        other = Polynomial(other)
        res = []
        l = max(len(self.koefs), len(other.koefs))
        m = min(len(self.koefs), len(other.koefs))
        if self.degree() >= other.degree():
            dlinniy = list(self.poly.values())
        else:
            dlinniy = list(other.poly.values())
        for i in range(l):
            if i < m:
                res.append(list(self.poly.values())[i] + list(other.poly.values())[i])
            elif i >= m:
                res.append(dlinniy[i])
        return Polynomial(res)

    def __radd__(self, other):
        return self + other

    def __eq__(self, other):
        other = Polynomial(other)
        return self.__str__() == other.__str__()

    def __neg__(self):
        for key in self.poly.keys():
            self.poly.update({key: -self.poly[key]})
        self.koefs = list(self.poly.values())
        return Polynomial(self.koefs)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __call__(self, x):
        s = 0
        for key in self.poly.keys():
            s += self.poly[key] * x ** key
        return s

    def der_1(self):
        new_dict = self.poly.copy()
        for key in self.poly.keys():
            if key != 0:
                new_dict.update({key - 1: key * new_dict[key]})
        new_dict.pop(max(new_dict.keys()))
        return Polynomial(new_dict)

    def der(self, d=1):
        if self.degree() < d:
            return '0'
        else:
            answer_dict = Polynomial(self.poly)
            for i in range(d):
                answer_dict = Polynomial(answer_dict.der_1())
            return answer_dict

    def __mul__(self, other):
        other = Polynomial(other)
        new_poly = {}
        for key1 in self.poly.keys():
            for key2 in other.poly.keys():
                new_poly.update({key1 + key2: new_poly.get(key1 + key2, 0) + self.poly[key1] * other.poly[key2]})

        return Polynomial(new_poly)

    def __rmul__(self, other):
        return self * other

    def __iter__(self):
        self.max = len(self.poly)
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            result = (list(self.poly.keys())[self.n],
                      self.poly[list(self.poly.keys())[self.n]])
            self.n += 1
            return result
        else:
            raise StopIteration


class DegreeIsTooBigException(BaseException):
    pass


class NotOddDegreeException(BaseException):
    pass


class QuadraticPolynomial(Polynomial):
    def __init__(self, *args):
        self.poly = {}
        for elem in args:
            if isinstance(elem, int):
                for i in range(len(args)):
                    self.poly.update({i: args[i]})
            elif isinstance(elem, list):
                self.poly = dict(enumerate(elem))
            elif isinstance(elem, dict):
                for key in sorted(elem.keys()):
                    self.poly[key] = elem[key]
            elif isinstance(elem, Polynomial):
                self.poly = elem.poly
        j = 0
        self.koefs = list(self.poly.values())
        for elem in self.koefs:
            if elem == -1 and j != 0:
                self.koefs[j] = '-'
            elif elem == 1 and j != 0:
                self.koefs[j] = ''
            j += 1
        k = len(self.koefs) - 1
        while self.poly.get(k, 0) == 0 and k > 0:
            self.poly.pop(k, 0)
            k -= 1
        if self.degree() > 2:
            raise DegreeIsTooBigException('Введите многочлен степени не больше 2')
        self.discrim = self.poly[1] ** 2 - 4 * self.poly[0] * self.poly[2]
        self.solution = []

    def solve(self):
        if self.degree() == 2:
            self.solution = [(-self.poly[1] + self.discrim ** 0.5) / (2 * self.poly[2]),
                             (-self.poly[1] - self.discrim ** 0.5) / (2 * self.poly[2])]
        elif self.degree() == 1:
            self.solution = [-self.poly[0] / self.poly[1]]
        else:
            self.solution = []
        if len(self.solution) < 2:
            return self.solution
        else:
            if self.solution[0] == self.solution[1]:
                self.solution = [self.solution[0]]
        return self.solution


class RealPolynomial(Polynomial):
    def __init__(self, *args):
        self.poly = {}
        for elem in args:
            if isinstance(elem, int):
                for i in range(len(args)):
                    self.poly.update({i: args[i]})
            elif isinstance(elem, list):
                self.poly = dict(enumerate(elem))
            elif isinstance(elem, dict):
                for key in sorted(elem.keys()):
                    self.poly[key] = elem[key]
            elif isinstance(elem, Polynomial):
                self.poly = elem.poly
            elif isinstance(elem, float):
                for i in range(len(args)):
                    self.poly.update({i: args[i]})
        j = 0
        self.koefs = list(self.poly.values())
        for elem in self.koefs:
            if elem == -1 and j != 0:
                self.koefs[j] = '-'
            elif elem == 1 and j != 0:
                self.koefs[j] = ''
            j += 1
        k = len(self.koefs) - 1
        while self.poly.get(k, 0) == 0 and k > 0:
            self.poly.pop(k, 0)
            k -= 1
        if self.degree() % 2 == 0:
            raise NotOddDegreeException('Введите многочлен нечетной степени')

    def find_root(self):  # бинарный поиск корня многочлена
        a = -10000
        b = a
        eps = 1e-6
        if self(a) == 0:
            return a
        if self(a) < 0:
            while self(b) < 0 and b < 10000:
                b += 1
        if self(a) > 0:
            while self(b) > 0 and b < 10000:
                b += 1
        while abs(self(a)) > eps:
            x = (a + b) / 2
            if self(a) < 0 and self(x) <= 0:
                a = x
            elif self(a) < 0 and self(x) >= 0:
                b = x
            elif self(a) > 0 and self(x) >= 0:
                a = x
            elif self(a) > 0 and self(x) < 0:
                b = x
        a = b
        return a
