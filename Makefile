run:
	gnome-terminal -e "./ngrok http 5000"
	sleep 5
	python3 app.py
