#include <iostream>
#include <limits>

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

int main() {
    double latitude = getDoubleInput("Enter latitude: ");
    double longitude = getDoubleInput("Enter longitude: ");

    if (!isValidLatitude(latitude)) {
        std::cout << "Invalid latitude. Latitude should be between " << MIN_LATITUDE << " and " << MAX_LATITUDE << ".\n";
    } else if (!isValidLongitude(longitude)) {
        std::cout << "Invalid longitude. Longitude should be between " << MIN_LONGITUDE << " and " << MAX_LONGITUDE << ".\n";
    } else {
        std::cout << "The coordinates are valid.\n";
    }

    return 0;
}