from flask import Flask, render_template

# create a Flask instance
app = Flask(__name__)

# create a route decorator
@app.route('/')

def index():
    return render_template("index.html")

# Create Custom Error pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", 404)

    # Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", 404)