#include <iostream>
#include <limits>
#include <string>
#include <cmath>
#include <iomanip>
#include <sstream>
#include <cassert>

const double MIN_LAT = -90.0, MAX_LAT = 90.0;
const double MIN_LON = -180.0, MAX_LON = 180.0;
const double EPSILON = 1e-10;

struct ValidationResult {
    bool isValid;
    std::string message;
    ValidationResult(bool valid, const std::string& msg = "") 
        : isValid(valid), message(msg) {}
};

ValidationResult parseCoordinate(const std::string& input, double& result) {
    if (input.empty() || input.length() > 50) {
        return ValidationResult(false, "Invalid input length");
    }
    
    std::istringstream iss(input);
    if (!(iss >> result) || iss >> std::ws && !iss.eof()) {
        return ValidationResult(false, "Invalid number format");
    }
    
    if (!std::isfinite(result)) {
        return ValidationResult(false, "Invalid value (infinity or NaN)");
    }
    
    return ValidationResult(true);
}

ValidationResult getInput(const std::string& prompt, double& value) {
    for (int attempts = 0; attempts < 3; ++attempts) {
        std::cout << prompt;
        std::string input;
        std::getline(std::cin, input);
        
        if (!std::cin.good()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            return ValidationResult(false, "Input stream error");
        }
        
        ValidationResult result = parseCoordinate(input, value);
        if (result.isValid) return ValidationResult(true);
        std::cout << "Error: " << result.message << "\n";
    }
    return ValidationResult(false, "Max attempts exceeded");
}

ValidationResult validateCoordinate(double value, double min, double max, 
                                  const std::string& type) {
    if (!std::isfinite(value)) {
        return ValidationResult(false, type + " must be finite");
    }
    if (value < min - EPSILON || value > max + EPSILON) {
        std::ostringstream oss;
        oss << type << " must be between " << min << " and " << max;
        return ValidationResult(false, oss.str());
    }
    return ValidationResult(true);
}

void runTests() {
    std::cout << "\nRunning validation tests...\n";
    
    // Test 1: Special floating point values
    {
        auto result = validateCoordinate(std::numeric_limits<double>::infinity(), 
                                       MIN_LAT, MAX_LAT, "Latitude");
        assert(!result.isValid && "FAIL: Accepts infinity");
        
        result = validateCoordinate(std::numeric_limits<double>::quiet_NaN(), 
                                  MIN_LAT, MAX_LAT, "Latitude");
        assert(!result.isValid && "FAIL: Accepts NaN");
    }
    
    // Test 2: Boundary values
    {
        auto result = validateCoordinate(MIN_LAT - EPSILON * 2, MIN_LAT, MAX_LAT, "Latitude");
        assert(!result.isValid && "FAIL: Accepts below minimum");
        
        result = validateCoordinate(MAX_LAT + EPSILON * 2, MIN_LAT, MAX_LAT, "Latitude");
        assert(!result.isValid && "FAIL: Accepts above maximum");
    }
    
    // Test 3: Input validation
    {
        double value;
        std::string invalidInputs[] = {"abc", "123abc", "-90.0e999", std::string(51, '9')};
        for (const auto& input : invalidInputs) {
            auto result = parseCoordinate(input, value);
            assert(!result.isValid && "FAIL: Accepts invalid input");
        }
    }
    
    // Test 4: Stream corruption test
    {
        std::cout << "Testing stream corruption...\n";
        std::string badInputs[] = {"abc", "123abc", "", "", "-90.0e999"};
        double value;
        
        for (const auto& input : badInputs) {
            std::istringstream iss(input);
            std::cin.rdbuf(iss.rdbuf());
            auto result = getInput("", value);
            assert(!result.isValid && "FAIL: Accepts corrupted input");
        }
    }
    
    // Restore cin to standard input
    std::cin.rdbuf(std::cin.rdbuf());
    std::cout << "All tests passed!\n\n";
}

int main() {
    runTests();
    return 0;
}