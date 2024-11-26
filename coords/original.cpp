#include <iostream>

// Define constants for latitude and longitude bounds
const double MIN_LATITUDE = -90.0;
const double MAX_LATITUDE = 90.0;
const double MIN_LONGITUDE = -180.0;
const double MAX_LONGITUDE = 180.0;

bool isValidLatitude(double latitude) {
    // Latitude should be between MIN_LATITUDE and MAX_LATITUDE
    return latitude >= MIN_LATITUDE && latitude <= MAX_LATITUDE;
}

bool isValidLongitude(double longitude) {
    // Longitude should be between MIN_LONGITUDE and MAX_LONGITUDE
    return longitude >= MIN_LONGITUDE && longitude <= MAX_LONGITUDE;
}

int main() {
    double latitude, longitude;

    std::cout << "Enter latitude: ";
    std::cin >> latitude;

    std::cout << "Enter longitude: ";
    std::cin >> longitude;

    if (isValidLatitude(latitude) && isValidLongitude(longitude)) {
        std::cout << "The coordinates are valid.\n";
    } else {
        std::cout << "The coordinates are invalid.\n";
    }

    return 0;
}
