#!/bin/bash

# Main manager page
function main_page {
	# Source virtualenv
	# TODO How to source in script from other script?
	source  $TIMEKEEPINGDIR/bin/activate

	# Header
	echo '----------------------------'
	echo "|Timekeeping Server Manager|"
	echo '----------------------------'
	
	# Commands to run
	echo '1) Boot Gunicorn'
	echo '2) Show Gunicorn Processes'
	echo '3) Kill Gunicorn Processes'
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
	elif [ $command = "q" ]; then
		echo 'bye!'
	else
		echo 'I dont know that command'
		main_page
	fi
	
}
# Boot Gunicorn
function boot_gunicorn {
	# formula = 1 + (2 * num cpus)
	NUM_WORKERS=2

	# Figure out how I want to source environment
	# OLD: cd /mnt/timekeeping/timekeepingapi
	# OLD: source ../bin/activate
	nohup `gunicorn hourglass:app -b 127.0.0.1:8000 -w $NUM_WORKERS` &
	echo 'Gunicorn booted'
	
	echo 'Enter to continue...'
	read continuation
}

# Show Gunicorn Processes
function gunicorn_processes {
	`ps -ef | grep -i gunicorn | awk '{print $2}'`
	
	echo 'Enter to continue...'
        read continuation

}

# Kill Gunicorn Processes
function kill_gunicorn {
	kill `ps axu | grep gunicorn | awk '{print $2}'`
	echo 'Gunicorn processes killed'

	echo 'Enter to continue...'
        read continuation
}

# Start the manager
clear
main_page
	
