#!/bin/bash

while true; do
	python3 atoms.py &
	PID=$!
	sleep 60
	kill $PID
done
