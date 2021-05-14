# radon-report
generates a Radon report from indoor climate sensor data

Currently only processes CSV file format exported from AirThings sensors

Calculates yearly mean as prescribed by Norwegian standard - see https://dsa.no/radon/slik-maler-du-radon#
In short - use a full year if available. Otherwise use at least two months in winter period starting November 1 and ending April 1. The correction factor when based on a whole yeat is one, and when based on wintertime months only, it's 0.75.

Uses Python pandas, matlib

Tested with Python v3.8 on macOS v11
