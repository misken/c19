#!/bin/bash

# This script lives in my main c19 working directory but can be
# launched from anywhere with the alias good_morning
 
# Get new data from Johns Hopkins and NY Times
printf '\nGet new data from Johns Hopkins'
cd ${C19_HOME}/community/COVID-19
git pull

printf '\nGet new data from NY Times'
cd ${C19_HOME}/community/covid-19-data
git pull

# Navigate back to c19 working directory
cd ${C19_HOME}

# Run script to update penn_chime software and copy 
# src files and settings files to their appropriate destinations
printf '\nGet updated penn_chime software'
./update_penn_chime.sh

# Open a few browser tabs
printf '\nOpen a few browser tabs'
xdg-open https://github.com/misken/c19
xdg-open https://github.com/CodeForPhilly/chime/issues?q=is%3Aissue+is%3Aopen+label%3Amodels
xdg-open https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6

