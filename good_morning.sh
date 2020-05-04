#!/bin/bash

# This script lives in my main c19 working directory but can be
# launched from anywhere with the alias goodmorning
 
# Get new data from Johns Hopkins and NY Times
printf '\nGet new data from Johns Hopkins\n'
printf '\n-------------------------------\n'
cd ${C19_HOME}/community/COVID-19
git pull

printf '\nGet new data from NY Times\n'
printf '\n--------------------------\n'
cd ${C19_HOME}/community/covid-19-data
git pull

# Navigate back to c19 working directory
cd ${C19_HOME}

# Run script to update penn_chime software and copy 
# src files and settings files to their appropriate destinations
printf '\nGet updated penn_chime software\n'
printf '\n-------------------------------\n'
./update_penn_chime.sh

# Open a few browser tabs
# printf '\nOpen a few browser tabs\n'
# printf '\n-----------------------\n'
# xdg-open https://github.com/misken/c19
# xdg-open https://penn-chime.phl.io/
# xdg-open https://github.com/CodeForPhilly/chime/issues?q=is%3Aissue+is%3Aopen+label%3Amodels

