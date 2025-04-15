from os.path import join, exists, isdir
from flask import Flask, send_from_directory

app = Flask(__name__)

STATIC_PATH = "webpage"

@app.route("/")
def home():
	return send_from_directory(STATIC_PATH, 'index.html')

@app.route("/hacked")
def hacked():
	return "CRA"

@app.route("/<path:path>")
def catch_everything_else(path):
	full_path = join(STATIC_PATH, path)
	if exists(full_path) and not isdir(full_path):
		return send_from_directory(STATIC_PATH, path)
	else:
		return home()

if __name__ == "__main__":
	app.run(debug=True, port=80)
