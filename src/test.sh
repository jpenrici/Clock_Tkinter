#!/bin/bash

echo "start $(basename $0) ..."

PATH_TIMER="$HOME/Clock_Tkinter/src"

if [[ $PATH_TIMER  != $PWD ]]; then
    cd $PATH_TIMER
fi

t=5 # interval

h=$(date +"%H")
m=$(date +"%M")
echo "now = $h:$m"
python3 clock_tk.py now=$h:$m minutes=$t &&

h1=$(expr $h + 1)
echo "now = $h:$m"
python3 clock_tk.py now=$h1:$m minutes=$t &&

h1=$(expr $h - 1)
echo "now = $h:$m"
python3 clock_tk.py now=$h1:$m minutes=$t &&

echo "exit ..."
exit