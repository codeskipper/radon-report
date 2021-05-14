# radon-report
generates a Radon report from indoor climate sensor data

Currently only processes CSV file format exported from AirThings sensors

Calculates yearly mean as prescribed by Norwegian standard - see https://dsa.no/radon/slik-maler-du-radon#
In short - use a full year if available, otherwise use at least two months in winter period starting November 1 and ending April 1.

Uses Python pandas, matlib

Tested with Python v3.8 on macOS v11
