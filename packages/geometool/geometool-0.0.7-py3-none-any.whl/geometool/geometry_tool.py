from math import pi, sqrt
from abc import ABC, abstractmethod

class Shape(ABC):
    
    @abstractmethod
    def calc_area(shape):
        raise NotImplementedError("Subclass of Shape must impliment calc_area() methode")

   
class Circle(Shape):
    
    def __init__(self, radius):
        if radius >= 0:
            self.radius = radius
        else:
            raise ValueError("Radius of a circle must be positive natural number.")            
            
    def calc_area(self):
        return pi * (self.radius ** 2)
    
    
class Triangle(Shape):
    
    def __init__(self, side1, side2, side3):
        if side1 or side2 or side3 >= 0:
            self.side1 = side1
            self.side2 = side2
            self.side3 = side3
        else:
            raise ValueError("A Triangle side must be positive natural number.")
    
    def is_rightangled(self):
        sides = [self.side1, self.side2, self.side3]
        sides.sort()
        
        if ( sides[0]**2 + sides[1]**2 == sides[2]**2 ):
            return True
        
        return False
        
    def calc_area(self):
        # Finding semi-perimeter 
        sp = (self.side1 + self.side2 + self.side3) / 2
        area = sqrt(sp * (sp - self.side1) * (sp - self.side2) * (sp - self.side3))
        if self.is_rightangled():
            return f"Triangle area is: {area}\nand the triangle is rightangled"
        
        return area

def calculate_area(shape):
    try:
        return shape.calc_area()
    except AttributeError:
        print("The shape Object missing calc_area() method.")
        return None


 
# s1 = Circle(5)
# s2 = Triangle(3, 4, 5)
