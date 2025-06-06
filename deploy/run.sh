#!/bin/sh

#
# Boostrap application with .venv and ensure application is killed on exit.
#

#echo "Ensure proper shell detection (keychain)..."
export SHELL=/bin/sh

#echo "Active .venv..."
. .venv/bin/activate

#echo "Secure file access..."
find conf/ logs/ -type d -exec chmod 700 {} +
find conf/ logs/ -type f -exec chmod 600 {} +

#echo "Run application..."
python -m app &
PID=$!

#echo "Wait and ensure kill signal is relayed to app..."
trap "kill $PID; exit" INT TERM EXIT
wait $PID
