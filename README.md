# weather-test

This script `extract_rainfall_with_coordinates.py` processes a radar image downloaded from the Thai Meteorological Department (TMD) website (https://weather.tmd.go.th/bma_ncLoop.php), extracts rainfall data by detecting contours within specified color ranges, converts pixel coordinates to latitude and longitude, and outputs the data to a CSV file and a debug image with labeled contours.

```
./install.sh
python extract_rainfall_with_coordinates.py
```
