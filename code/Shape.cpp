#include "Shape.h"

Shape::Shape() : area(0.0), perimeter(0.0), errorMessage("") {}

Shape::~Shape() {}

double Shape::getArea() const {
    return area;
}

double Shape::getPerimeter() const {
    return perimeter;
}

std::string Shape::getErrorMessage() const {
    return errorMessage;
}
