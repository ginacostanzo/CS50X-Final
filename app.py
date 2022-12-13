import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///cocktails.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show homepage"""
    USERS = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
    bar_name = USERS[0]["bar_name"]
    return render_template("index.html", bar_name=bar_name)

@app.route("/mybar")
@login_required
def mybar():
    """Show homepage"""

    BARS = db.execute("SELECT * FROM bars WHERE user_id=? ORDER BY ingredients", session["user_id"])
    USERS = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
    bar_name = USERS[0]["bar_name"]
    return render_template("mybar.html", bars=BARS, bar_name=bar_name)

@app.route("/myingredients")
@login_required
def myingredients():
    """Show homepage"""

    BARS = db.execute("SELECT * FROM bars WHERE user_id=? ORDER BY ingredients", session["user_id"])
    USERS = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
    bar_name = USERS[0]["bar_name"]
    return render_template("myingredients.html", bars=BARS, bar_name=bar_name)

@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    """Show homepage"""
    FAVORITES = db.execute("SELECT * FROM favorites WHERE user_id=? ORDER BY drink", session["user_id"])
    if request.method == "POST":
        drink = request.form.get("drink")
        DRINKS = db.execute("SELECT drink FROM recipes GROUP BY drink")
        favorites = []

        for i in range(len(FAVORITES)):
            favorite = FAVORITES[i]["drink"]
            favorites.append(favorite)
        if drink not in favorites:
            db.execute("INSERT INTO favorites (user_id, drink) VALUES (?, ?)", session["user_id"], drink)
            FAVORITES = db.execute("SELECT * FROM favorites WHERE user_id=? ORDER BY drink", session["user_id"])
            return render_template("drinks.html", drinks=DRINKS, favorites=FAVORITES)
        if drink in favorites:
            return (render_template("favorites.html", favorites=FAVORITES))
    else:
        return render_template("favorites.html", favorites=FAVORITES)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Code copied over from Finance pset in CS50x
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", error="Must provide username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error="Must provide password.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", error="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        #create a row for the user in BARS
        BARS = db.execute("SELECT * FROM bars WHERE user_id=?", session["user_id"])
        if len(BARS) == 0:
            db.execute("INSERT INTO bars (id, bar_name) VALUES (?, ?)", session["user_id"], rows[0]["bar_name"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    """Forgot Password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username and email submitted
        if not username or not email or not password or not confirmation:
            return render_template("forgot.html", error="Must complete all fields.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ? AND email = ?", request.form.get("username"), request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return render_template("forgot.html", error="invalid username and/or email")

        # hash the password the user entered
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # store the username and hashed password in the database of users
        db.execute("UPDATE users SET hash=? WHERE username=?", hash, username)

        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("forgot.html")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    """Forgot Password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        new = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # if the user updates their username
        if username:
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            if len(rows) != 0:
                return render_template("settings.html", error="Username already exists.")
            # otherwise update the username in the database
            db.execute("UPDATE users SET username = ? WHERE id = ?", username, session["user_id"])

        # if the user updates their email address
        if email:
            db.execute("UPDATE users SET email = ? WHERE id = ?", email, session["user_id"])

        # if the user enters a new password
        if new:
            if not password or not confirmation:
                return render_template("forgot.html", error="Must complete all fields.")
            # hash the new password
            hash = generate_password_hash(new, method='pbkdf2:sha256', salt_length=8)
            # replace the password in the users database
            db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session["user_id"])

        return render_template("settings.html", message="Saved!")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("settings.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # If user clicks register via posting form
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("confirmation")
        name = request.form.get("name")
        name = name.title()
        email = request.form.get("email")
        # default bar name is person name's Bar
        bar_name = (f"{name}'s Bar")

        # if the username, password, or re-enter password field are left blank, provide error message
        if not username or not password or not password2 or not name or not email:
            return render_template("register.html", error="Invalid registration. Must complete all fields.")

        # if the username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return render_template("register.html", error="Username already exists.")

        # if the passwords do not match, return error message
        if not password == password2:
            return render_template("register.html", error="Passwords must match.")

        # hash the password the user entered
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # store the username and hashed password in the database of users
        db.execute("INSERT INTO users (username, hash, name, email, bar_name) VALUES (?, ?, ?, ?, ?)", username, hash, name, email, bar_name)

        return render_template("login.html")

    # if the user just clicks the register link on the page, take them to the html page to register
    else:
        return render_template("register.html")

@app.route("/update", methods=["GET", "POST"])
def update():
    SPIRITS = db.execute("SELECT ingredient FROM ingredients WHERE type='Spirit' ORDER BY ingredient")
    SYRUPS = db.execute("SELECT ingredient FROM ingredients WHERE type='Syrup' ORDER BY ingredient")
    JUICES = db.execute("SELECT ingredient FROM ingredients WHERE type='Juice' ORDER BY ingredient")
    ALCS = db.execute("SELECT ingredient FROM ingredients WHERE type='Other Alcoholic' ORDER BY ingredient")
    BITTERS = db.execute("SELECT ingredient FROM ingredients WHERE type='Bitters' ORDER BY ingredient")
    NON_ALCS = db.execute("SELECT ingredient FROM ingredients WHERE type='Non-Alcoholic' ORDER BY ingredient")
    MISCS = db.execute("SELECT ingredient FROM ingredients WHERE type='Misc.' ORDER BY ingredient")
    USERS = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])

    if request.method == "POST":
        bar_name = request.form.get("bar_name")
        ingredients = request.form.getlist("ingredient")
        ids = request.form.getlist("id")
        BARS = db.execute("SELECT * FROM bars WHERE user_id=? ORDER BY ingredients", session["user_id"])

        # if the user types in a new bar name
        if bar_name != "":
            bar_name = request.form.get("bar_name")
            db.execute("UPDATE users SET bar_name=? WHERE id=?", request.form.get("bar_name"), session["user_id"])

        # delete ingredients
        if ids:
            for i in range(len(ids)):
                id = ids[i]
                db.execute("DELETE FROM bars WHERE id=?", id)

        # add ingredients
        for i in range(len(ingredients)):
            ingredient = ingredients[i]
            db.execute("INSERT INTO bars (user_id, bar_name, ingredients) VALUES (?, ?, ?)", session["user_id"], USERS[0]["bar_name"], ingredient)

        return redirect("/mybar")

    else:
        BARS = db.execute("SELECT * FROM bars WHERE user_id=? ORDER BY ingredients", session["user_id"])
        # only display the ingredients the user DOESN'T have
        spirits =[]
        syrups = []
        juices = []
        alcs = []
        bitters = []
        non_alcs = []
        miscs = []
        bar = []

        for i in range(len(BARS)):
            bar.append(BARS[i]["ingredients"])

        for i in range(len(SPIRITS)):
            if SPIRITS[i]["ingredient"] not in bar:
                spirits.append(SPIRITS[i]["ingredient"])
        for i in range(len(SYRUPS)):
            if SYRUPS[i]["ingredient"] not in bar:
                syrups.append(SYRUPS[i]["ingredient"])
        for i in range(len(JUICES)):
            if JUICES[i]["ingredient"] not in bar:
                juices.append(JUICES[i]["ingredient"])
        for i in range(len(ALCS)):
            if ALCS[i]["ingredient"] not in bar:
                alcs.append(ALCS[i]["ingredient"])
        for i in range(len(BITTERS)):
            if BITTERS[i]["ingredient"] not in bar:
                bitters.append(BITTERS[i]["ingredient"])
        for i in range(len(NON_ALCS)):
            if NON_ALCS[i]["ingredient"] not in bar:
                non_alcs.append(NON_ALCS[i]["ingredient"])
        for i in range(len(MISCS)):
            if MISCS[i]["ingredient"] not in bar:
                miscs.append(MISCS[i]["ingredient"])

        return render_template("update.html", bar_name=USERS[0]["bar_name"], bars=BARS, spirits=spirits, syrups=syrups, juices=juices, alcs=alcs, bitters=bitters, non_alcs=non_alcs, miscs=miscs)

@app.route("/available")
def available():
    # get a dict of all the ingredients the user has
    rows = db.execute("SELECT * FROM bars WHERE user_id=?", session["user_id"])

    # if the user has no ingredients, redirect them to add ingredients first
    if len(rows) == 0:
        return render_template("setup.html")
    else:
        bar_name = rows[0]["bar_name"]

        # create a list of the user's ingredients
        on_hand = []
        for i in range(len(rows)):
            ingredient = (rows[i]["ingredients"]).upper().strip()
            on_hand.append(ingredient)

        DRINKS = db.execute("SELECT drink FROM recipes GROUP BY drink")
        # make a LIST of drink names
        drinks = []
        for i in range(len(DRINKS)):
            drink = DRINKS[i]["drink"]
            drinks.append(drink)

        # check for each ingredient in a drink if the user has it on hand
        available_drinks = []
        missing1 = []
        missing2 = []
        missing3 = []
        missingmore = []

        # for each drink in the recipe database
        for i in range(len(drinks)):
            recipes = db.execute("SELECT * FROM recipes WHERE drink=?", drinks[i])
            # start with an empty list of ingredients, start the count of missing ingredients at 0
            ingredients = []
            count = 0
            # go throught the length of the recipe to the ingredient column, label that ingredient=ingredient, add that ingredient to the ingredients list
            for j in range(len(recipes)):
                ingredient = (recipes[j]["ingredient"]).upper().strip()
                ingredients.append(ingredient)
            # for the length of the ingredients list, add 1 to the count each time the ingredient is missing from user's ingredients
            for s in range(len(ingredients)):
                if ingredients[s] not in on_hand:
                    count += 1

            if count == 0:
                available_drinks.append(drinks[i])
            if count == 1:
                missing1.append(drinks[i])
            if count == 2:
                missing2.append(drinks[i])
            if count == 3:
                missing3.append(drinks[i])
            if count > 3:
                missingmore.append(drinks[i])

        if len(available_drinks) == 0:
            available_drinks = ["None"]
        if len(missing1) == 0:
            missing1 = ["None"]
        if len(missing2) == 0:
            missing2 = ["None"]
        if len(missing3) == 0:
            missing3 = ["None"]
        if len(missingmore) == 0:
            missingmore = ["None"]

        return render_template("available.html", bar_name=bar_name, availables=available_drinks, miss1s=missing1, miss2s=missing2, miss3s=missing3, missings=missingmore)

@app.route("/drinks")
def drinks():
    DRINKS = db.execute("SELECT drink FROM recipes GROUP BY drink")
    FAVORITES = db.execute("SELECT * FROM favorites WHERE user_id=?", session["user_id"])
    return render_template("drinks.html", drinks=DRINKS, favorites=FAVORITES)

@app.route("/ingredients", methods=["GET", "POST"])
def ingredients():
    INGREDIENTS = db.execute("SELECT ingredient FROM ingredients ORDER BY ingredient")
    if request.method == "POST":
        ingredient1 = request.form.get("ingredient1")
        ingredient2 = request.form.get("ingredient2")
        if not ingredient1:
            ingredient = ingredient2
        if not ingredient2:
            ingredient = ingredient1

        DRINKS = db.execute("SELECT drink FROM recipes WHERE ingredient=?", ingredient)
        return render_template("drinks2.html", ingredient=ingredient, drinks=DRINKS)

    else:
        SPIRITS = db.execute("SELECT ingredient FROM ingredients WHERE type='Spirit' ORDER BY ingredient")
        SYRUPS = db.execute("SELECT ingredient FROM ingredients WHERE type='Syrup' ORDER BY ingredient")
        JUICES = db.execute("SELECT ingredient FROM ingredients WHERE type='Juice' ORDER BY ingredient")
        ALCS = db.execute("SELECT ingredient FROM ingredients WHERE type='Other Alcoholic' ORDER BY ingredient")
        BITTERS = db.execute("SELECT ingredient FROM ingredients WHERE type='Bitters' ORDER BY ingredient")
        NON_ALCS = db.execute("SELECT ingredient FROM ingredients WHERE type='Non-Alcoholic' ORDER BY ingredient")
        MISCS = db.execute("SELECT ingredient FROM ingredients WHERE type='Misc.' ORDER BY ingredient")

        ingredients = []
        for i in range(len(INGREDIENTS)):
            ingredient = INGREDIENTS[i]["ingredient"]
            ingredients.append(ingredient)

        return render_template("ingredients.html", spirits=SPIRITS, syrups=SYRUPS, juices=JUICES, alcs=ALCS, bitters=BITTERS, non_alcs=NON_ALCS, miscs=MISCS, ingredients=ingredients)


@app.route("/recipe", methods=["GET", "POST"])
def recipe():
    # info to display for the recipe
    drink0 = request.form.get("drink0")
    drink1 = request.form.get("drink1")
    drink2 = request.form.get("drink2")

    if not drink0 and not drink1:
            drink = drink2
    if not drink1 and not drink2:
        drink = drink0
    if not drink2 and not drink0:
        drink = drink1

    DRINKS = db.execute("SELECT drink FROM recipes GROUP BY drink")

    # make a LIST of all drink names
    recipes = []
    for i in range(len(DRINKS)):
        recipe = DRINKS[i]["drink"]
        recipes.append(recipe)

    # if the user types a drink that doesn't exist, take them to the page to add a recipe
    if drink not in recipes:
        INGREDIENTS =  db.execute("SELECT ingredient FROM ingredients ORDER BY ingredient")
        return render_template("add.html", ingredients=INGREDIENTS)

    if drink in recipes:
        RECIPES = db.execute("SELECT * FROM recipes WHERE drink=?", drink)
        INSTRUCTIONS = db.execute("SELECT instructions FROM recipes WHERE drink=? GROUP BY instructions", drink)
        instruction = INSTRUCTIONS[0]["instructions"]
        # get a dict of all the ingredients the user has
        rows = db.execute("SELECT ingredients FROM bars WHERE user_id=?", session["user_id"])
        # create a list of the user's ingredients
        on_hand = []
        for i in range(len(rows)):
            ingredient = (rows[i]["ingredients"])
            on_hand.append(ingredient)

        # check for each ingredient in a drink if the user has it on hand
        missing_ing = []
        needed = []

        # go throught the length of the recipe to the ingredient column, label that ingredient=ingredient, add that ingredient to the ingredients list
        for i in range(len(RECIPES)):
            ingredient = (RECIPES[i]["ingredient"])
            needed.append(ingredient)
        # for the length of the ingredients list, add 1 to the count each time the ingredient is missing from user's ingredients
        for j in range(len(needed)):
            if needed[j] not in on_hand:
                missing_ing.append(needed[j])

        if len(missing_ing) == 0:
            missing_ing = ["None"];

        FAVORITES = db.execute("SELECT * FROM favorites WHERE user_id=?", session["user_id"])
        favorites = []
        for i in range(len(FAVORITES)):
            favorite = FAVORITES[i]["drink"]
            favorites.append(favorite)

        if drink not in favorites:
            message = "+ Add to Favorites"
        if drink in favorites:
            message = "Favorited. View your Favorites."

        return render_template("recipe.html", recipes=RECIPES, drink=drink, favorites=favorites, instruction=instruction, missing_ings=missing_ing, message=message)

@app.route("/add1", methods=["GET", "POST"])
def add1():
    # add a recipe to the database
    if request.method == "POST":
        drink = request.form.get("drink")
        quantities = request.form.getlist("quantity")
        ingredients = request.form.getlist("ingredient")
        instructions = request.form.get("instructions")
        INGREDIENTS =  db.execute("SELECT ingredient FROM ingredients")

        all_ing = []
        for i in range(len(INGREDIENTS)):
            ingredient = INGREDIENTS[i]["ingredient"]
            ingredient = ingredient.upper().strip()
            all_ing.append(ingredient)

        new_ingredients = []
        TYPES = [
            "Bitters",
            "Juice",
            "Misc.",
            "Non-Alcoholic",
            "Other Alcoholic",
            "Spirit",
            "Syrup"
        ]

        if not drink or not quantities or not ingredients:
            return render_template("add.html", error="Must include drink name and at least 1 quantity and ingredient.")

        for i in range(len(ingredients)):
            if ingredients[i] != "":
                db.execute("INSERT INTO recipes (drink, ingredient, quantity, instructions) VALUES (?, ?, ?, ?)", drink, ingredients[i], quantities[i], instructions)
                if ingredients[i].upper().strip() not in all_ing:
                    new_ingredients.append(ingredients[i])

        if len(new_ingredients) == 0:
            DRINKS = db.execute("SELECT drink FROM recipes GROUP BY drink")
            return render_template("drinks.html", drinks=DRINKS)
        if len(new_ingredients) != 0:
            return render_template("addredirect.html", ingredients=new_ingredients, types=TYPES)

    else:
        INGREDIENTS =  db.execute("SELECT ingredient FROM ingredients ORDER BY ingredient")
        return render_template("add.html", ingredients=INGREDIENTS)

@app.route("/add2", methods=["GET", "POST"])
def add2():
    TYPES = [
            "Bitters",
            "Juice",
            "Misc.",
            "Non-Alcoholic",
            "Other Alcoholic",
            "Spirit",
            "Syrup"
        ]

    if request.method == "POST":
        ingredients = request.form.getlist("ingredient")
        types = request.form.getlist("type")

        INGREDIENTS = db.execute("SELECT ingredient FROM ingredients ORDER BY ingredient")

        all_ing = []
        for i in range(len(INGREDIENTS)):
            ingredient = INGREDIENTS[i]["ingredient"]
            all_ing.append(ingredient)

        for i in range(len(ingredients)):
            if ingredients[i] not in all_ing:
                db.execute("INSERT INTO ingredients (ingredient, type) VALUES (?, ?)", ingredients[i], types[i])

        DRINKS = db.execute("SELECT drink FROM recipes GROUP BY drink")
        return render_template("drinks.html", drinks=DRINKS)
    else:
        return render_template("addingredients.html", types=TYPES)