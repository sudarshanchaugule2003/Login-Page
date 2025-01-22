# Imports 
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from docx import Document
import io
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
    return render_template("login.html")

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
            return redirect(url_for("display_sub_form", username=username))
        else:
            flash("Wrong credentials","danger")
            return redirect(url_for('login'))
    
    return render_template("login.html")

@app.route("/display_sub_form/<username>")
def display_sub_form(username):
    return render_template("display_sub_form.html", username=username)

#form submit route
@app.route("/submit", methods=["POST"])
def subject():
    selected_sub = request.form.get("subject")

    answers = {
        "Question 1": request.form.get("q1"),
        "Question 2": request.form.get("q2"),
        "Question 3": request.form.get("q3"),
        "Question 4": request.form.get("q4"),
    }
    answers["subject"] = selected_sub

    mongo.db.answers.insert_one({
        "answers": answers,
        "subject": selected_sub,
    })

    if selected_sub == "subject-1": #checking comparing with value of radio btn
        return render_template("subject1.html")
    elif selected_sub == "subject-2":
        return render_template("subject2.html")
    elif selected_sub == "subject-3":
        return render_template("subject3.html")

    return render_template("display_sub_form.html", selected_sub=selected_sub)

# # next page after submitting form
# @app.route('/next', methods=['GET','POST'])
# def next_page(subject):
#     if subject == "subject-1": #checking comparing with value of radio btn
#         return render_template("subject1_next_page.html")
#     elif subject == "subject-2":
#         return render_template("subject2_next_page.html")
#     elif subject == "subject-3":
#         return render_template("subject3_next_page.html")

#     return render_template("display_sub_form.html")


@app.route('/next/subject1', methods=['POST'])
def subject1_next():
    # Render the next page for Subject 1
    return render_template('subject1_next.html')

@app.route('/next/subject2', methods=['POST'])
def subject2_next():
    # Render the next page for Subject 1
    return render_template('subject2_next.html')

@app.route('/next/subject3', methods=['POST'])
def subject3_next():
    # Render the next page for Subject 1
    return render_template('subject3_next.html')


# @app.route('/review', methods=['POST'])
# def review():
#     # Handle form data here
#     return render_template('review.html')

# @app.route('/review', methods=['GET', 'POST'])
# def review():
#     # Fetch all answers from the database
#     answers = list(mongo.db.answers.find())

#     # Pass the answers to the template
#     return render_template('review.html', answers=answers)

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        # Handle form submission
        selected_sub = request.form.get("subject")
        answers = {
            "Question 1": request.form.get("q1"),
            "Question 2": request.form.get("q2"),
            "Question 3": request.form.get("q3"),
            "Question 4": request.form.get("q4"),
        }
        answers["subject"] = selected_sub

        # Save the answers to the database
        mongo.db.answers.insert_one({
            "answers": answers,
            "subject": selected_sub,
        })

        flash("Form submitted successfully!")
        return redirect(url_for('review'))  # This will redirect to a GET request to avoid resubmission

    elif request.method == 'GET':
        # Fetch all answers from the database for review
        answers = list(mongo.db.answers.find())
        return render_template('review.html', answers=answers)



# @app.route('/update_answers', methods=['POST'])
# def update_answers():
#     selected_sub = request.form.get("subject")
#     updated_answers = request.form.getlist('answers')  # Get the updated answers from
#     updated_answers_dict = {
#         "Question 1": updated_answers[0],
#         "Question 2": updated_answers[1],
#         "Question 3": updated_answers[2],
#         "Question 4": updated_answers[3],
#     }

#     # Update the record in the database
#     mongo.db.answers.update_one(
#         {"subject": selected_sub},  # Match the document with the same subject
#         {"$set": {"answers": updated_answers_dict}}  # Update the answers
#     )

#     flash("Answers updated successfully!")  # Flash success message
#     return redirect(url_for('review'))  # Redirect to the review page to show updated answers

# @app.route('/update_answers', methods=['POST'])
# def update_answers():
#     # Get the subject from the form
#     selected_sub = request.form.get("subject")

#     # Initialize an empty dictionary to store updated answers
#     updated_answers_dict = {}

#     # Get the answers from the form (it's a dictionary where keys are the question names)
#     for key in request.form:
#         if key.startswith("answers["):  # Check if the key starts with 'answers['
#             question = key[8:-1]  # Extract the question key, e.g., "Question 1"
#             updated_answers_dict[question] = request.form.get(key)

#     # Now, you have updated_answers_dict with the correct question-answer pairs
#     # Update the record in the database
#     mongo.db.answers.update_one(
#         {"subject": selected_sub},  # Match the document with the same subject
#         {"$set": {"answers": updated_answers_dict}}  # Update the answers
#     )

#     flash("Answers updated successfully!")  # Flash success message
#     return redirect(url_for('review'))  # Redirect to the review page to show updated answers

@app.route('/update_answers', methods=['POST'])
def update_answers():
    # Retrieve and process the updated answers
    selected_sub = request.form.get("subject")
    updated_answers_dict = {}

    # Populate the updated answers dictionary
    for key in request.form:
        if key.startswith("answers["):
            question = key[8:-1]
            updated_answers_dict[question] = request.form.get(key)

    # Update the database
    mongo.db.answers.update_one(
        {"subject": selected_sub},
        {"$set": {"answers": updated_answers_dict}}
    )

    flash("Answers updated successfully!")
    return redirect(url_for('review'))


# @app.route('/generate_docx', methods=['GET', 'POST'])
# def generate_docx():
#     if request.method == 'POST':
#         doc = Document()
        
#         doc.add_heading('your copy of Submitted Answers', 0)

#         if answers:
#             for answer in answers[0].answers.items():
#                 question, answer_value = answer
#                 doc.add_paragraph(f"{question}: {answer_value}")
#         else:
#             doc.add_paragraph("No answers available for review.")

#         # Saves document to an in-memory file (using io.BytesIO)
#         file_stream = io.BytesIO()
#         doc.save(file_stream)
#         file_stream.seek(0)

#         # Sends the file to the user for download
#         return send_file(file_stream, as_attachment=True, download_name="review_answers.docx", mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
#     # If GET request, just render the review page
#     return render_template('review.html', answers=answers)



# @app.route('/generate_docx', methods=['GET', 'POST'])
# def generate_docx():
#     # Fetch answers for the current user (you need to define how to get them from your database or context)
#     # Assuming you're passing `answers` when rendering the page or have access to them
#     answers = get_answers_from_database()  # Replace with your logic to get answers

#     if request.method == 'POST':
#         # Create a new Document
#         doc = Document()
        
#         doc.add_heading('Your Copy of Submitted Answers', 0)

#         if answers:
#             for answer in answers[0].answers.items():
#                 question, answer_value = answer
#                 doc.add_paragraph(f"{question}: {answer_value}")
#         else:
#             doc.add_paragraph("No answers available for review.")

#         # Save the document to an in-memory file (using io.BytesIO)
#         file_stream = io.BytesIO()
#         doc.save(file_stream)
#         file_stream.seek(0)

#         # Send the file to the user for download
#         return send_file(file_stream, as_attachment=True, download_name="review_answers.docx", mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

#     # If GET request, just render the review page
#     return render_template('review.html', answers=answers)


@app.route('/generate_docx', methods=['POST'])
def generate_docx():
    # Fetch answers
    answers = get_answers_from_database()  # Replace this with the actual way to get the answers

    # Create a new document
    doc = Document()
    doc.add_heading('Your Copy of Submitted Answers', 0)

    if answers:
        for answer in answers[0].answers.items():
            question, answer_value = answer
            doc.add_paragraph(f"{question}: {answer_value}")
    else:
        doc.add_paragraph("No answers available for review.")

    # Save document to in-memory file
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    # Send the file to the user for download
    return send_file(file_stream, as_attachment=True, download_name="review_answers.docx", mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


def get_answers_from_database():
    # This is where you should define how to fetch the answers.
    # For example, if you're fetching it from MongoDB, you'd do something like this:
    answers = mongo.db.answers.find({"user": current_user})  # Adjust as needed
    return answers



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
    app.run(debug=True, use_reloader=True, port=5000)
