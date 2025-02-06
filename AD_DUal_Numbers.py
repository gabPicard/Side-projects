import numpy as np

class Dual:
    def __init__(self, real, dual):
        """
        real: real part of the dual number
        dual: dict
        """
        self.real = real
        self.dual = dual
    
    def conj(self):
        return Dual(self.real, {key: -self.dual[key] for key in self.dual})
    
    def __add__(self, other):
        real = self.real
        dual = {}
        for key in self.dual:
            dual[key] = self.dual[key]
        if isinstance(other, Dual):
            for key in other.dual:
                if key in dual:
                    dual[key] += other.dual[key]
                else:
                    dual[key] = other.dual[key]
            real += other.real
        else:
            real += other
        return Dual(real, dual)
    
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        real = self.real
        dual = {}
        for key in self.dual:
            dual[key] = self.dual[key]
        if isinstance(other, Dual):
            for key in other.dual:
                if key in dual:
                    dual[key] -= other.dual[key]
                else:
                    dual[key] = other.dual[key]
            real -= other.real
        else:
            real -= other
        return Dual(real, dual)

    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __mul__(self, other):
        real = self.real
        dual = {}
        if isinstance(other, Dual):
            for key in self.dual:
                dual[key] = self.dual[key] * other.real
            for key in other.dual:
                if key in dual:
                    dual[key] += self.real * other.dual[key]
                else:
                    dual[key] = self.real * other.dual[key]
            real *= other.real
        else:
            for key in self.dual:
                dual[key] = self.dual[key] * other
            real *= other
        return Dual(real, dual)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, Dual):
            real = self.real / other.real
            dual = (self.__mul__(other.conj())).dual / (other.real ** 2)
        else:
            real = self.real / other
            dual = {}
            for key in self.dual:
                dual[key] = self.dual[key] / other
        return Dual(real, dual)
    
    def __pow__(self, power):
        real = self.real ** power
        dual = {}
        for key in self.dual:
            dual[key] = power * self.real ** (power - 1) * self.dual[key]
        return Dual(real, dual)

    def __neg__(self):
        return Dual(-self.real, {key: -self.dual[key] for key in self.dual})

    def log(self):
        real = np.log(self.real*a)
        dual = {key: self.dual[key] / self.real for key in self.dual}
        return Dual(real, dual)
    
    def sin(self):
        real = np.sin(self.real)
        dual = {key: np.cos(self.real) * self.dual[key] for key in self.dual}
        return Dual(real, dual)
    
    def cos(self):
        real = np.cos(self.real)
        dual = {key: - np.cos(self.real) * self.dual[key] for key in self.dual}
        return Dual(real, dual)
    
    def exp(self):
        real = np.exp(self.real)
        dual = {key: np.exp(self.real) * self.dual[key] for key in self.dual}
        return Dual(real, dual)
    
    def sigmoid(self):
        real = 1 / (1 + np.exp(-self.real))
        dual = {key: np.exp(-self.real) / (1 + np.exp(-self.real)) ** 2 * self.dual[key] for key in self.dual}
        return Dual(real, dual)

    def __str__(self):
        s = "f(" + ",".join(self.dual.keys()) + ") = " + str(self.real)+ "\n"
        for key in self.dual:
            s += "df/d"+str(key)+" = " + str(self.dual[key]) + "\n"
        return s
    
    def to_vector(self):
        return np.array([self.dual[key] for key in self.dual])

    
x = Dual(1, {"x": 1})
y = Dual(2, {"y": 1})
z = Dual(3, {"z": 1})

f = x ** 2 + y ** 2 + z.sin()
print(f)
