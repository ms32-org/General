from flask import Flask,render_template
from random import randint

app = Flask(__name__)
users = []
@app.route("/")
def home():
	code = randint(10000,99999)
	users.append(code)
	return render_template("index.html", id=code)
	
if __name__ == "__main__":
	app.run(debug=True)