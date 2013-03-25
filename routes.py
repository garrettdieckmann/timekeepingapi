from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def api_root():
	return 'Root of API'

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
