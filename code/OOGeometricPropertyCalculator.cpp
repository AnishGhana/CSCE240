#include "Shape.h"
#include "Rectangle.h"
#include "Circle.h"
#include "Triangle.h"
#include <iostream>
#include <fstream>
#include <sstream>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <property_number>" << std::endl;
        return 1;
    }

    int propertyNumber = std::stoi(argv[1]);

    std::ifstream inputFile("input.txt");
    std::ofstream outputFile("output.txt");

    std::string line;
    while (std::getline(inputFile, line)) {
        std::istringstream iss(line);
        std::string shape;
        double arg1, arg2, arg3;
        iss >> shape >> arg1 >> arg2 >> arg3;

        Shape* currentShape = nullptr;

        if (shape == "RECTANGLE") {
            currentShape = new Rectangle(arg1, arg2);
        } else if (shape == "CIRCLE") {
            currentShape = new Circle(arg1);
        } else if (shape == "TRIANGLE") {
            currentShape = new Triangle(arg1, arg2, arg3);
        }

        if (currentShape) {
            if (propertyNumber == 1) {
                currentShape->calculateArea();
            } else if (propertyNumber == 2) {
                currentShape->calculatePerimeter();
            }

            outputFile << shape << " " << ((propertyNumber == 1) ? "AREA" : "PERIMETER") << " " << currentShape->getErrorMessage() << std::endl;

            delete currentShape;
        }
    }

    inputFile.close();
    outputFile.close();

    return 0;
}
