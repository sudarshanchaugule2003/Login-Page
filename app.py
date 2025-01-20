# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mail import Mail, Message
# # from flask_sqlalchemy import SQLAlchemy
# # from flask_migrate import Migrate
# from flask_pymongo import PyMongo

# app = Flask(__name__)

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = "vedant.22220153@viit.ac.in"
# app.config['MAIL_PASSWORD'] = "9822156586Pappa"
# app.config['MAIL_DEFAULT_SENDER'] = 'vedant.22220153@viit.ac.in'
# mail = Mail(app)


# # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# # app.config['TEMPLATES_AUTO_RELOAD'] = True
# # app.secret_key = 'abcdefgh'
# # db = SQLAlchemy(app)
# # migrate = Migrate(app, db)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/Login"

# mongo = PyMongo(app)

# class accounts(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique = True)
#     password = db.Column(db.String(15), nullable = False)
#     email = db.Column(db.String(100), unique = True, nullable=False)

# with app.app_context():
#         db.create_all()

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/signup", methods=["GET","POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         email = request.form.get("email")

#         # checking for existed user
#         exixt_user = accounts.query.filter_by(username=username).first()
#         if exixt_user:
#             flash("Account already exists")
#             return redirect(url_for('signup'))
        
#         # new user account with email
#         new_account = accounts(username = username, password=password, email=email)
#         db.session.add(new_account)
#         db.session.commit()

#         flash("Account created")
#         return redirect(url_for('login'))
#     return render_template("signup.html")

# @app.route("/login", methods = ["GET", "POST"])
# def login():
#      if(request.method == "POST"):
#           username = request.form.get("username")
#           password = request.form.get("password")        
          
#           #exist account
#           usr_account = accounts.query.filter_by(username=username).first()
#           if usr_account and usr_account.password == password:
#                print({username})
#                return redirect(url_for("display", username = username))
#           else:
#                print({username})
#                flash("wrong credentials")
#                return redirect(url_for('login'))
#      return render_template("login.html")

# @app.route("/display/<username>")
# def display(username):
#      return f"welcome {username}"

# @app.route("/forgot-password", methods=["GET", "POST"])
# def forgot_password():
#      if request.method == "POST":
#           email = request.form.get("email")
#           username = request.form.get("username")
          
#           account = accounts.query.filter_by(username=username).first()

#           if account:
#             # send reset link
#             reset_link = url_for('reset_password', _external = True)
#             msg = Message(
#                 recipients = [email]
#             )
#             msg.body = f'Hi, {account.username}!\n\nClick on link to reset password : \n{reset_link}'

#             try:
#                 mail.send(msg)
#                 flash("password reset instruction on your flash")
#                 return redirect(url_for("forgot_password"))
#             except Exception as e:
#                 flash(f"Error in sending email: {str(e)}")
#                 return redirect(url_for('forgot_password'))
#           else:
#             flash("user not found")
#             return redirect(url_for('forgot_password'))
#      return render_template("forgot_password.html")

# @app.route("/reset-password", methods = ["GET", "POST"])
# def reset_password():
#     if request.method == "POST":
#         new_password = request.form.get("new_password")
#         usernme = request.form.get("username")
# # look for this
#         from werkzeug.security import generate_password_hash
#         hashed_password = generate_password_hash(new_password)

#         account = accounts.query.filter_by(username=username).first()
#         if account:
#             account.password = hashed_password
#             db.session.commit()
#             flash("your Password has been chnanged")
#             return redirect(url_for('login'))
#         else:
#             flash("user not found")
#             return redirect(url_for('reset_password'))
#     return render_template("reset_password.html")



# if __name__ == '__main__':
#     app.run(debug=True)


# Imports 
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

# app instance creation
app = Flask(__name__)

# Gmail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "vedant.22220153@viit.ac.in"
app.config['MAIL_PASSWORD'] = "bogt bjmz zayb xpyi"
app.config['MAIL_DEFAULT_SENDER'] = 'vedant.22220153@viit.ac.in'
mail = Mail(app)

# Mongo-DB compass setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/Login"
app.secret_key = 'abcdefgh'
mongo = PyMongo(app)

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# SignUp route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        #exited userid
        existing_user = mongo.db.accounts.find_one({"username": username})
        if existing_user:
            flash("Account already exists")
            return redirect(url_for('signup'))
        #existed email id

        existing_mail = mongo.db.accounts.find_one({"email":email})
        if existing_mail:
            flash("Email already exixts")
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)

        #new user
        mongo.db.accounts.insert_one({
            "username": username,
            "password": hashed_password,
            "email": email})
        flash("Account created successfully")
        return redirect(url_for('login'))
    return render_template("signup.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #finduser by username
        usr_account = mongo.db.accounts.find_one({"username": username})  #filter_by in sqlaalchemy
        if usr_account and check_password_hash(usr_account["password"], password):
            return redirect(url_for("display", username=username))
        else:
            flash("Wrong credentials")
            return redirect(url_for('login'))
    
    return render_template("login.html")

# final page after login 
@app.route("/display/<username>")
def display(username):
    return render_template("Display.html", username = username)

# forgot-password route
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        #username = request.form.get("username")

        account = mongo.db.accounts.find_one({"email":email})

        if account:
            #reset link share
            reset_link = url_for('reset_password', _external=True)
            msg = Message(
                recipients=[email]
            )
            msg.body = f'Hi, {account["username"]}!\n\nClick on link to reset password: \n{reset_link}'

            try:
                mail.send(msg)
                flash("Password reset instructions sent to your email")
                return redirect(url_for("forgot_password"))
            except Exception as e:
                flash(f"Error in sending email: {str(e)}")
                return redirect(url_for('forgot_password'))
        else:
            flash("User not found")
            return redirect(url_for('forgot_password'))
    
    return render_template("forgot_password.html")

# Reset password route
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        new_password = request.form.get("new_password")
        username = request.form.get("username")

        hashed_password = generate_password_hash(new_password)

        account = mongo.db.accounts.find_one({"username": username})
        if account:
            mongo.db.accounts.update_one({"username": username}, {"$set": {"password": hashed_password}})
            flash("Your password has been changed")
            return redirect(url_for('login'))
        else:
            flash("User not found")
            return redirect(url_for('reset_password'))

    return render_template("reset_password.html")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=4000)
