# Geometool - Geometric Shape Calculation Library

**```MB Task-1```**

This Python package provides functions to calculate the area and perimeter of various geometric shapes.


## Installation

You can install the package using pip:

```bash
$ pip install geometool
```

## Methods

The package provides the following functions (yet):

- `calculate_area(shape)` : Calculates the area of a given shape. Supported shapes include:
    - Circle(radius)
    - Triangle(3 sides)


## Classes

### Shape
Abstract base class for geometric shapes.

### Circle
- `calc_area()` to calculate the area.

### Triangle
- `calc_area()` to calculate the area 
- `is_rightangled()` to check if the triangle is right-angled.


## Usage

```bash
import geometool as g

# Declare a shape object 

s1 = g.Circle(5)
s2 = g.Triangle(6, 8, 9)

# Use calculate_area() to calculate the area of the object 

g.calculate_area(s1)
g.calculate_area(s2)

```


## Authors: Idris Taha
- Contact: dri.taha24@gmail.com