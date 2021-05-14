# radon-report

generates a Radon report from indoor climate sensor data

Currently only processes CSV file format exported from AirThings sensors

Calculates Yearly Mean as prescribed by Norwegian standard - see https://dsa.no/radon/slik-maler-du-radon#
In short - use a full year if the data is available. 
Otherwise use at least two months in the winter period starting November 1, and ending April 1. 
The correction factor when based on a whole year is 1.0, and 0.75 when based on the wintertime months only.
There must be at least two months of wintertime data available in order to generate a valid report.

Uses Python pandas, matlib

The 7-day average is calculated, and it's plot is displayed together with the Yearly Average, and saved as an image file.

Tested with Python v3.8 on macOS v11
