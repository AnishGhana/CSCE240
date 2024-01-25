#include <iostream>
#include <fstream>
#include <math.h>
#include <sstream>
#include <string>

double calculateRectangleArea(double length, double breadth)
{
    return length * breadth;
}

double calculateRectanglePerimeter(double length, double breadth)
{
    return 2 * (length + breadth);
}

double calculateCircleArea(double radius)
{
    return M_PI * radius * radius;
}

double calculateCirclePerimeter(double radius)
{
    return 2 * M_PI * radius;
}

double calculateTriangleArea(double side1, double side2, double side3)
{
    // Heron's formula
    double s = (side1 + side2 + side3) / 2;
    return sqrt(s * (s - side1) * (s - side2) * (s - side3));
}

double calculateTrianglePerimeter(double side1, double side2, double side3)
{
    return side1 + side2 + side3;
}

void processInputLine(std::ofstream &outputFile, const std::string &shape, const std::string &property, const double &arg1, const double &arg2, const double &arg3)
{
    if (property == "AREA")
    {
        double result;
        if (shape == "RECTANGLE")
        {
            result = calculateRectangleArea(arg1, arg2);
        }
        else if (shape == "CIRCLE")
        {
            result = calculateCircleArea(arg1);
        }
        else if (shape == "TRIANGLE")
        {
            if (arg1 + arg2 > arg3 && arg1 + arg3 > arg2 && arg2 + arg3 > arg1)
            {
                result = calculateTriangleArea(arg1, arg2, arg3);
            }
            else
            {
                outputFile << shape << " " << property << " "
                           << "Not enough info to calculate" << std::endl;
                return;
            }
        }
        outputFile << shape << " " << property << " " << result << std::endl;
    }
    else if (property == "PERIMETER")
    {
        double result;
        if (shape == "RECTANGLE")
        {
            result = calculateRectanglePerimeter(arg1, arg2);
        }
        else if (shape == "CIRCLE")
        {
            result = calculateCirclePerimeter(arg1);
        }
        else if (shape == "TRIANGLE")
        {
            result = calculateTrianglePerimeter(arg1, arg2, arg3);
        }
        outputFile << shape << " " << property << " " << result << std::endl;
    }
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " <property_number>" << std::endl;
        return 1;
    }

    int propertyNumber = std::stoi(argv[1]);

    std::ifstream inputFile("input.txt");
    std::ofstream outputFile("output.txt");

    std::string line;
    while (std::getline(inputFile, line))
    {
        std::istringstream iss(line);
        std::string shape;
        double arg1, arg2, arg3;
        iss >> shape >> arg1 >> arg2 >> arg3;

        if (propertyNumber == 1)
        {
            processInputLine(outputFile, shape, "AREA", arg1, arg2, arg3);
        }
        else if (propertyNumber == 2)
        {
            processInputLine(outputFile, shape, "PERIMETER", arg1, arg2, arg3);
        }
    }

    inputFile.close();
    outputFile.close();

    return 0;
}
