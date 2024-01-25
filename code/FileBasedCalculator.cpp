#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

int main()
{
    std::ifstream inputFile;
    inputFile.open("input.txt");

    if (!inputFile.is_open())
    {
        std::cerr << "Error opening the file: input.txt" << std::endl;
        return 1; // Exit with an error code
    }

    std::string line;
    if (std::getline(inputFile, line))
    {
        std::istringstream lineStream(line);

        char operation;
        int num1, num2;

        // Get the values from the lineStream
        if (lineStream >> operation >> num1 >> num2)
        {

            // The section of code which performs calculations
            int result;
            switch (operation)
            {
            case '+':
                result = num1 + num2;
                break;
            case '-':
                result = num1 - num2;
                break;
            case '*':
                result = num1 * num2;
                break;
            case '/':
                // Checks for division by zero
                if (num2 != 0)
                {
                    result = num1 / num2;
                }
                else
                {
                    std::cerr << "Error: Division by zero." << std::endl;
                    return 1;
                }
                break;
            default:
                std::cerr << "Error: Invalid operation." << std::endl;
                return 1;
            }

            // Write the two lines to the output file
            std::ofstream outputFile("output.txt", std::ios::trunc); // This puts it in truncation mode
            if (outputFile.is_open())
            {
                std::string myString = "The result of " + std::string(1, operation) + " on " +
                                       std::to_string(num1) + " and " + std::to_string(num2) +
                                       " is below.";
                outputFile << myString << std::endl;
                outputFile << result << std::endl;

                outputFile.close();
            }
            else
            {
                std::cerr << "Error opening or writing to the output file." << std::endl;
                return 1;
            }
        }
        else
        {
            std::cerr << "Error parsing line: " << line << std::endl;
            return 1;
        }
    }
    else
    {
        std::cerr << "Error: Empty file or unable to read from the input file." << std::endl;
        return 1;
    }

    inputFile.close();

    return 0;
}
