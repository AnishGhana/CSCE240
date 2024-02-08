#include "Triangle.h"
#include <cmath>

Triangle::Triangle(double s1, double s2, double s3) : side1(s1), side2(s2), side3(s3) {}

Triangle::~Triangle() {}

void Triangle::calculateArea() {
    double s = (side1 + side2 + side3) / 2;
    area = sqrt(s * (s - side1) * (s - side2) * (s - side3));
}

void Triangle::calculatePerimeter() {
    perimeter = side1 + side2 + side3;
}
