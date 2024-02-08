#include "Rectangle.h"

Rectangle::Rectangle(double len, double brd) : length(len), breadth(brd) {}

Rectangle::~Rectangle() {}

void Rectangle::calculateArea() {
    area = length * breadth;
}

void Rectangle::calculatePerimeter() {
    perimeter = 2 * (length + breadth);
}
