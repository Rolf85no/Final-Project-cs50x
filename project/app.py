import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import textwrap
import re

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


MEALS = [
    "Breakfast",
    "Lunch",
    "Dinner",
    "Side-dish",
    "Dessert",
    "Snack"
]
conn = sqlite3.connect('recipes.db', check_same_thread=False)
db = conn.cursor()


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]
    db.execute("SELECT DISTINCT tags FROM recipes WHERE recipes_user= ?", [user_id])
    tags = db.fetchall()

    if request.method == "POST":
        choice = request.form.get("choice")
        if choice != "All":
            db.execute("SELECT id, name, recipe, website, tags, photo FROM recipes WHERE recipes_user= ? AND tags= ? ORDER BY name",
                        (user_id, choice))
            recipes = db.fetchall()
        else:
            db.execute("SELECT id, name, recipe, website, tags, photo FROM recipes WHERE recipes_user= ? ORDER BY tags, name", [user_id])
            recipes = db.fetchall()
        return render_template("index.html", recipes=recipes, tags=tags)

    else:

        db.execute("SELECT id, name, recipe, website, tags, photo FROM recipes WHERE recipes_user= ? ORDER BY tags, name", [user_id])
        recipes = db.fetchall()
        return render_template("index.html", recipes=recipes, tags=tags)


@app.route("/all", methods=["GET", "POST"])
@login_required
def all_recep():
    #Lagrer session id under user_id
    user_id = session["user_id"]
    db.execute("SELECT DISTINCT tags FROM recipes")
    tags = db.fetchall()
    if request.method == "POST":
        choice = request.form.get("choice")

        # En enkel måte å si at hvis ikke all er valget så skal man sjekke choice opp mot database
        if choice != "All":
            db.execute("SELECT id, name, recipe, website, tags, photo FROM recipes WHERE tags= ? ORDER BY name", [choice])
            recipes = db.fetchall()
        else:
            db.execute("SELECT id, name, recipe, website, tags, photo FROM recipes ORDER BY tags, name")
            recipes = db.fetchall()
        return render_template("all.html", recipes=recipes, tags=tags)

    else:
        db.execute("SELECT id, name, recipe, website, tags, photo, recipes_user FROM recipes ORDER BY tags, name")
        recipes = db.fetchall()
        return render_template("all.html", recipes=recipes, tags=tags)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Legge inn brukernavn, sjekker at feltet er fylt inn
        username = request.form.get("username")
        if not username:
            flash('No username')
            return redirect("/register")
        # Legge inn passord, sjekker at feltet er fylt inn
        password = request.form.get("password")
        if not password:
            flash('No password')
            return redirect("/register")
        # Sjekker passord mot confirmation
        if request.form.get("confirmation") != password:
            flash('Password and confirmation are not the same')
            return redirect("/register")

        # Dette er bare en fancy måte å si at hvis noen i rows matcher username
        db.execute("SELECT * FROM users WHERE username = ?", [username])
        rows = db.fetchall()
        if len(rows) == 1:
            flash('username already in use')
            return redirect("/register")

        # Kryptering av passord
        pw = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        # Lagre brukernavn og passord i SQL, og enkode passord samtidig.
        with conn:
            db.execute("INSERT INTO users (username, hash) VALUES(?,?)", (username, pw))
        flash('Registered')
        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            flash('Must provide username')
            return render_template("login.html")

        # Ensure password was submitted
        if not password:
            flash('Must provide password')
            return render_template("login.html")

        # Query database for username
        db.execute("SELECT * FROM users WHERE username = ?", [username])
        rows = db.fetchall()
        # Ensure username exists and password is correct
        if not rows or not check_password_hash(rows[0][2], password):
            flash('Invalid username and/or password')
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        flash('Logged in')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    user_id = session["user_id"]
    if request.method == "POST":
        # Sørger for at alle navnet har stor forbokstav, liten bokstav resten
        name = request.form.get("recipe_name").capitalize()
        recipe_text = request.form.get("recipe_text")
        website = request.form.get("link")
        photo = request.form.get("photo")
        tags = request.form.get("tag")

        # Fjerner tegn som ikke er ascii
        recipe = re.sub(r'[^\x00-\x7f]', r'', recipe_text)
        # Sørger for at alle linjer har maks 48 ord og fjerner space foran og bak
        textwrap.wrap(text=recipe, width=48)
        textwrap.dedent(text=recipe)

        if not name:
            flash('Please write name of recipe')
            return render_template("upload.html")

        if not website:
            flash('Please write link to recipe')
            return render_template("upload.html")

        if not tags:
            flash('Please choose meal type')
            return render_template("upload.html")

        else:
            with conn:
                db.execute("INSERT INTO recipes (name, recipe, website, tags, recipes_user, photo) VALUES (?,?,?,?,?, ?)",
                       (name, recipe, website, tags, user_id, photo))
            flash('Recipe uploaded')

    return render_template("upload.html", meals=MEALS)


@app.route("/inspiration")
@login_required
def inspiration():

    user_id = session["user_id"]

    return render_template("inspiration.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

