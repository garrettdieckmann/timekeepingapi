#!/bin/bash

# Main manager page
function main_page {
	# Source virtualenv
	# Just hard-code location for now
	. ../bin/activate

	# Header
	echo '----------------------------'
	echo "|Timekeeping Server Manager|"
	echo '----------------------------'
	
	# Commands to run
	echo '1) Boot Gunicorn'
	echo '2) Show Gunicorn Processes'
	echo '3) Kill Gunicorn Processes'
	echo '4) Boot Development app server'
	echo
	echo 'q) to quit'
	echo 
	
	# read input
	read command

	if [ $command = "1" ]; then
		boot_gunicorn
	elif [ $command = "2" ]; then
		gunicorn_processes
	elif [ $command = "3" ]; then
		kill_gunicorn
	elif [ $command = "4" ]; then
		boot_dev_serv
	elif [ $command = "q" ]; then
		echo 'bye!'
	else
		echo 'I dont know that command'
		main_page
	fi
	
}
# Boot Development App server
function boot_dev_serv {
	# Keeping output in foreground
	`python hourglass.py`
	echo 'dev booted'
	
	return_to_main
}

# return to main page
function return_to_main {
	echo 'Enter to continue...'
	read continuation
	main_page
}

# Boot Gunicorn
function boot_gunicorn {
	# formula = 1 + (2 * num cpus)
	NUM_WORKERS=2

	# boot gunicorn into background
	nohup `gunicorn hourglass:app -b 127.0.0.1:8000 -w $NUM_WORKERS` &
	echo 'Gunicorn booted'
	
	return_to_main
}

# Show Gunicorn Processes
function gunicorn_processes {
	ps -ef | grep -i gunicorn | awk '{print $2,$9,$10}'
	
	return_to_main

}

# Kill Gunicorn Processes
function kill_gunicorn {
	kill `ps axu | grep gunicorn | awk '{print $2}'`
	echo 'Gunicorn processes killed'

	return_to_main
}

# Start the manager
clear
main_page
	
