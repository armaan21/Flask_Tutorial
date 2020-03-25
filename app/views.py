# grabs the app variable created from the __init__.py file
from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_file, send_from_directory, safe_join, abort
from datetime import datetime
from werkzeug.utils import secure_filename
import os

@app.route("/")
def index():
	# print(app.config)
	app.config["SECRET_KEY"] = "iuhto743yto34iuho287gh78"
	print(app.config["SECRET_KEY"])
	return render_template("public/index.html")

@app.route("/about")
def about():
	return """
    <h1 style='color: red;'>I'm a red H1 heading!</h1>
    <p>This is a lovely little paragraph</p>
    <code>Flask is <em>awesome</em></code>
    """

@app.route("/jinja")
def jinja():

    # Strings
    my_name = "Armaan"

    # Integers
    my_age = 21

    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Dictionaries
    friends = {
        "Tony": 43,
        "Cody": 28,
        "Amy": 26,
        "Clarissa": 23,
        "Wendell": 39
    }

    # Tuples
    colors = ("Red", "Blue")

    # Booleans
    cool = True

    my_html = "<h1>This is some HTML</h1>"
    suspicious = "<script>alert('NEVER TRUST USER INPUT!')</script>"

    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description 
            self.domain = domain

        def pull(self):
            return f"Pulling repo '{self.name}'"

        def clone(self, repo):
            return f"Cloning into {repo}"

    my_remote = GitRemote(
        name="Learning Flask",
        description="Learn the Flask web framework for Python",
        domain="https://github.com/Julian-Nash/learning-flask.git"
    )

    # Functions
    def repeat(x, qty=1):
        return x * qty

    date = clean_date(datetime.utcnow())
    return render_template(
    	"public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
    	friends=friends, colors=colors, cool=cool, GitRemote=GitRemote, 
    	my_remote=my_remote, repeat=repeat, date=date, my_html=my_html, suspicious=suspicious)

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        req = request.form

        missing = list()

        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("public/sign_up.html", feedback=feedback)

        return redirect(request.url)

    return render_template("public/sign_up.html")


users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creatof of the Flask framework",
        "twitter_handle": "@mitsuhiko"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk"
    }
}

@app.route("/profile/<username>")
def profile(username):

    user = None

    if username in users:
        user = users[username]

    return render_template("public/dynamic.html", username=username, user=user)

@app.route("/multiple/<foo>/<bar>/<baz>")
def multiple(foo, bar, baz):

	print(f"foo is {foo}")
	print(f"bar is {bar}")
	print(f"baz is {baz}")

	return f"foo is {foo}, bar is {bar}, baz is {baz}"

@app.route("/json", methods=["POST"])
def json_example():

    if request.is_json:

        req = request.get_json()

        response_body = {
            "message": "JSON received!",
            "sender": req.get("name")
        }

        res = make_response(jsonify(response_body), 200)

        return res

    else:

        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)

    return res

@app.route("/query")
def query():

    if request.args:

        # We have our query string nicely serialized as a Python dictionary
        args = request.args

        # We'll create a string to display the parameters & values
        serialized = ", ".join(f"{k}: {v}" for k, v in request.args.items())

        # Display the query string to the client in a different format
        return f"(Query) {serialized}", 200

    else:

        return "No query string received", 200

app.config["IMAGE_UPLOADS"] = "/Users/armaa/OneDrive/Desktop/PDF2Audio/app/static/images/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024 * 1024

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            # if "filesize" in request.cookies:
            # 	print("YES")
            # 	if not allowed_image_filesize(request.cookies["filesize"]):
            # 		print("Filesize exceeded maximum limit")
            # 		return redirect(request.url)
            		
            	image = request.files["image"]

            	if image.filename == "":
            		print("No filename")
            		return redirect(request.url)

            	if allowed_image(image.filename):
            		filename = secure_filename(image.filename)
            		image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            		print("Image saved")
            		return redirect(request.url)

            	else:
            		print("That file extension is not allowed")
            		return redirect(request.url)

    return render_template("public/upload_image.html")