#include <iostream>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <chrono>
#include <fstream>
#include "../../../../../../../msys64/ucrt64/include/c++/13.1.0/bits/algorithmfwd.h"

using namespace std;
using namespace std::chrono;

// Bubble sort algorithm
void bubbleSort(vector<int> &arr)
{
    int n = arr.size();
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                // Swap
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// Function to generate random numbers
void generateRandomNumbers(vector<int> &arr, int n)
{
    srand(time(0)); // Seed for random number generation
    for (int i = 0; i < n; i++)
    {
        arr.push_back(rand() % 1000); // Generating numbers between 0 and 999
    }
}

// Validation function
bool validateSort(vector<int> &arr1, vector<int> &arr2)
{
    if (arr1.size() != arr2.size())
        return false;

    for (int i = 0; i < arr1.size(); i++)
    {
        if (arr1[i] != arr2[i])
            return false;
    }

    return true;
}

int main()
{
    vector<int> sizes = {100, 1000, 10000, 100000};
    vector<double> bubble_array_times;
    vector<double> standard_array_times;
    vector<double> bubble_vector_times;
    vector<double> standard_vector_times;

    for (int n : sizes)
    {
        vector<int> arr;
        generateRandomNumbers(arr, n);
        vector<int> arr1 = arr; // Copying for validation
        vector<int> arr2 = arr; // Copying for sorting

        auto start = high_resolution_clock::now();
        bubbleSort(arr1);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(stop - start);
        bubble_array_times.push_back(duration.count());

        start = high_resolution_clock::now();
        sort(arr2.begin(), arr2.end());
        stop = high_resolution_clock::now();
        duration = duration_cast<milliseconds>(stop - start);
        standard_array_times.push_back(duration.count());

        arr1 = arr; // Resetting for vector sort
        arr2 = arr; // Resetting for vector sort

        start = high_resolution_clock::now();
        bubbleSort(arr1);
        stop = high_resolution_clock::now();
        duration = duration_cast<milliseconds>(stop - start);
        bubble_vector_times.push_back(duration.count());

        start = high_resolution_clock::now();
        sort(arr2.begin(), arr2.end());
        stop = high_resolution_clock::now();
        duration = duration_cast<milliseconds>(stop - start);
        standard_vector_times.push_back(duration.count());
    }

    ofstream file("sort_times.dat");
    file << "# Size Bubble_Array Standard_Array Bubble_Vector Standard_Vector\n";
    for (size_t i = 0; i < sizes.size(); ++i)
    {
        file << sizes[i] << " " << bubble_array_times[i] << " " << standard_array_times[i] << " " << bubble_vector_times[i] << " " << standard_vector_times[i] << endl;
    }
    file.close();

    // Generate GNU Plot script
    ofstream script("plot_script.gnu");
    script << "set terminal png\n";
    script << "set output 'sorting_times.png'\n";
    script << "set title 'Sorting Time Comparison'\n";
    script << "set xlabel 'Input Size'\n";
    script << "set ylabel 'Time (ms)'\n";
    script << "set logscale xy\n";
    script << "plot 'sort_times.dat' using 1:2 with lines title 'Bubble Sort with Array', \\\n";
    script << "     'sort_times.dat' using 1:3 with lines title 'Standard Sort with Array', \\\n";
    script << "     'sort_times.dat' using 1:4 with lines title 'Bubble Sort with Vector', \\\n";
    script << "     'sort_times.dat' using 1:5 with lines title 'Standard Sort with Vector'\n";
    script.close();

    // Execute GNU Plot
    system("gnuplot -persist plot_script.gnu");

    return 0;
}
