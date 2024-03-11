import random
import string
import json
import os
from flask import send_from_directory
from flask import Flask, render_template, redirect, url_for, request
from logging import FileHandler, WARNING
import sys;

print('Python %s on %s' % (sys.version, sys.platform))
app = Flask(__name__, template_folder="templates")
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
shortened_urls = {}


def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url] = long_url
        with open("urls.json", "w") as f:
            json.dump(shortened_urls, f)

        return render_template('shortened_url.html', short_url=short_url)
    return render_template("index.html")


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found",


if __name__ == "__main__":
    app.run(debug=True)
