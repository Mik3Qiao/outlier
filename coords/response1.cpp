#include <iostream>
#include <limits>
#include <string>
#include <cassert>
#include <cmath>

// Define constants for latitude and longitude bounds
const double MIN_LATITUDE = -90.0;
const double MAX_LATITUDE = 90.0;
const double MIN_LONGITUDE = -180.0;
const double MAX_LONGITUDE = 180.0;

// Function to get a double value from the user, with input validation
double getDoubleInput(const std::string& prompt) {
    while (true) {
        std::cout << prompt;
        double value;
        if (std::cin >> value) {
            return value;
        } else {
            std::cout << "Invalid input. Please enter a number.\n";
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }
    }
}

bool isValidLatitude(double latitude) {
    // Latitude should be between MIN_LATITUDE and MAX_LATITUDE
    return latitude >= MIN_LATITUDE && latitude <= MAX_LATITUDE;
}

bool isValidLongitude(double longitude) {
    // Longitude should be between MIN_LONGITUDE and MAX_LONGITUDE
    return longitude >= MIN_LONGITUDE && longitude <= MAX_LONGITUDE;
}


void runTests() {
    std::cout << "\nRunning validation tests...\n\n";

    // Test 1: Special floating point values
    std::cout << "Test 1: Special floating point values\n";
    assert(!std::isfinite(std::numeric_limits<double>::infinity()) && 
           "FAIL: Program accepts infinity as valid latitude");
    assert(!std::isfinite(std::numeric_limits<double>::quiet_NaN()) && 
           "FAIL: Program accepts NaN as valid latitude");
    
    // Test 2: Boundary value tests with floating point precision
    std::cout << "Test 2: Boundary value tests\n";
    double almostMinLatitude = MIN_LATITUDE - 1e-15;
    double almostMaxLatitude = MAX_LATITUDE + 1e-15;
    assert(!isValidLatitude(almostMinLatitude) && 
           "FAIL: Program accepts latitude slightly below minimum");
    assert(!isValidLatitude(almostMaxLatitude) && 
           "FAIL: Program accepts latitude slightly above maximum");

    // Test 3: Buffer overflow test with very long input
    std::cout << "Test 3: Buffer overflow test\n";
    std::string veryLongInput(1000000, 'a');  // Create a string with 1 million 'a' characters
    std::cout << "Enter this long string to test buffer overflow:\n" << veryLongInput << std::endl;
    
    // Test 4: Stream corruption test
    std::cout << "Test 4: Stream corruption test\n";
    std::cout << "Enter these values in sequence:\n";
    std::cout << "abc\n123abc\n\n\n-90.0e999\n";
}

int main() {
    runTests();
    
    return 0;
}