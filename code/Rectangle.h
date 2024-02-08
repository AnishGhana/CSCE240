#ifndef RECTANGLE_H
#define RECTANGLE_H

#include "Shape.h"

class Rectangle : public Shape {
private:
    double length;
    double breadth;

public:
    Rectangle(double len, double brd);
    ~Rectangle() override;

    void calculateArea() override;
    void calculatePerimeter() override;
};

#endif // RECTANGLE_H
