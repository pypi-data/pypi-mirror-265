class simple_arthmetic_calc:
    def __init__(self) -> None:
        pass
    
    def add(self, a : float, b : float) -> float:
        return a+b
    
    def sub(self, a : float, b : float) -> float:
        return a-b
    
    def mul(self, a : float, b : float) -> float:
        return a*b
    
    def div(self, a : float, b : float) -> float:
        if b == 0:
            return "Divide by zero error"
        return a/b
    
    def abs(self, a: float) -> float:
        return abs(a)
    
    def fact(self, a : int) -> int:
        if a < 0:
            return "Factorial of negative number is not possible"
        if a == 0:
            return 1
        return a*self.fact(a-1)
    
    def power(self, a : float, b : float) -> float:
        return a**b
    
    def sqrt(self, a : float) -> float:
        if a < 0:
            return "Square root of negative number is not possible"
        return a**0.5
    
    def mod(self, a : float, b: float) -> float:
        return a%b
    
    def lcm(self, a : float, b : float) -> float:
        if a == 0 or b == 0:
            return "LCM of zero is not possible"
        return (a*b)//self.gcd(a, b)
    
    def gcd(self, a : float, b : float) -> float:
        if b == 0:
            return a
        return self.gcd(b, a%b)
    
    def is_prime(self, a : int) -> bool:
        if a < 2:
            return False
        for i in range(2, int(a**0.5)+1):
            if a%i == 0:
                return False
        return True
    
    def is_even(self, a : int) -> bool:
        return a%2 == 0
    
    def is_odd(self, a : int) -> bool:
        return a%2 != 0