#ifndef CIRCLE_H
#define CIRCLE_H

#include "Shape.h"

class Circle : public Shape {
private:
    double radius;

public:
    Circle(double rad);
    ~Circle() override;

    void calculateArea() override;
    void calculatePerimeter() override;
};

#endif // CIRCLE_H
