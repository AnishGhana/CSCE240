#include "Circle.h"
#include <cmath>

Circle::Circle(double rad) : radius(rad) {}

Circle::~Circle() {}

void Circle::calculateArea() {
    area = M_PI * radius * radius;
}

void Circle::calculatePerimeter() {
    perimeter = 2 * M_PI * radius;
}
