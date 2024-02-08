#ifndef SHAPE_H
#define SHAPE_H

#include <string>

class Shape {
protected:
    double area;
    double perimeter;
    std::string errorMessage;

public:
    Shape();
    virtual ~Shape();

    virtual void calculateArea() = 0;
    virtual void calculatePerimeter() = 0;

    double getArea() const;
    double getPerimeter() const;
    std::string getErrorMessage() const;
};

#endif // SHAPE_H
