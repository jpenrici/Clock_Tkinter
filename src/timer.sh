#!/bin/bash

echo "start $(basename $0) ..."

PATH_TIMER="$HOME/Clock_Tkinter/src"

if [[ $PATH_TIMER  != $PWD ]]; then
	cd $PATH_TIMER
fi

echo clock_tk.py minutes="$@"
python3 clock_tk.py minutes="$@"

echo "exit ..."
exit