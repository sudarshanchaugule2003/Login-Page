
# Imports 
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from docx import Document
import io
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
# app instance creation
app = Flask(__name__)
# Secret key for session management
app.secret_key = 'your_secret_key'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User model (adjust it to your needs)
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# User loader callback function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # In a real app, fetch the user from the database using user_id
    return User(user_id, "test_username")  # Replace with actual user retrieval logic

# Simulate a database query to get answers for the logged-in user
def get_answers_from_database():
    # Fetch answers based on the current user (you need to adjust this to your database logic)
    if current_user.is_authenticated:
        answers = mongo.db.answers.find({"user_id": current_user.id})  # Replace with your actual DB query
        return answers
    else:
        return None

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

        # Check if username already exists
        existing_user = mongo.db.accounts.find_one({"username": username})
        if existing_user:
            flash("Account already exists")
            return redirect(url_for('signup'))

        # Check if email already exists
        existing_mail = mongo.db.accounts.find_one({"email": email})
        if existing_mail:
            flash("Email already exists")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)

        # Create a new user
        mongo.db.accounts.insert_one({
            "username": username,
            "password": hashed_password,
            "email": email})
        flash("Account created successfully")
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch the user from the database
        user = mongo.db.accounts.find_one({"username": username})
        
        if user:
            # Verify the password
            if check_password_hash(user['password'], password):
                # Create a User object and log in
                user_obj = User(str(user['_id']), username)
                login_user(user_obj)
                return redirect(url_for('display_sub_form', username=username))
            else:
                flash('Invalid password')  # Incorrect password
        else:
            flash('User not found')  # Username doesn't exist

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()  # Flask-Login handles the logout
    return redirect(url_for('login'))

@app.route("/display_sub_form/<username>")
def display_sub_form(username):
    return render_template("display_sub_form.html", username=username)

@app.route("/submit", methods=["POST"])
@login_required
def subject():
    selected_sub = request.form.get("subject")
    answers = {
        "Question 1": request.form.get("q1"),
        "Question 2": request.form.get("q2"),
        "Question 3": request.form.get("q3"),
        "Question 4": request.form.get("q4"),
    }

    if selected_sub: 
        existing_submission = mongo.db.answers.find_one({"user_id": current_user.id, "subject": selected_sub})

        if existing_submission:
            # Update existing record
            mongo.db.answers.update_one(
                {"user_id": current_user.id, "subject": selected_sub},
                {"$set": {"answers": answers}}
            )
            flash("Your answers have been updated successfully!")
        else:
            # Insert new answers
            mongo.db.answers.insert_one({
                "user_id": current_user.id,
                "answers": answers,
                "subject": selected_sub,
            })
            flash("Answers submitted successfully!")

    # Redirect to the appropriate form based on subject
    if selected_sub == "subject-1":
        return render_template("subject1.html")
    elif selected_sub == "subject-2":
        return render_template("subject2.html")
    elif selected_sub == "subject-3":
        return render_template("subject3.html")

    return redirect(url_for('display_sub_form', username=current_user.username))



@app.route('/subject1_form', methods=['POST'])
@login_required
def subject1_form():
    # Fetch the submitted form data
    answers = {
        "Question 1": request.form.get("q1"),
        "Question 2": request.form.get("q2"),
        "Question 3": request.form.get("q3"),
        "Question 4": request.form.get("q4"),
    }
    selected_sub = "subject-1"  # Static identifier for this form

    existing_submission = mongo.db.answers.find_one({"user_id": current_user.id, "subject": selected_sub})

    if existing_submission:
        # Update existing answers
        mongo.db.answers.update_one(
            {"user_id": current_user.id, "subject": selected_sub},
            {"$set": {"answers": answers}}
        )
        flash("Your answers have been updated successfully!")
    else:
        # Insert new answers
        mongo.db.answers.insert_one({
            "user_id": current_user.id,
            "subject": selected_sub,
            "answers": answers,
        })
        flash("Answers submitted successfully!")

    # Redirect to the next subject page
    return render_template('subject1_next.html')

@app.route('/subject1_next', methods=['POST'])
@login_required
def subject1_next():
    answers = {
        "Question 1": request.form.get("q1"),
        "Question 2": request.form.get("q2"),
    }
    selected_sub = "subject-1-next"

    existing_submission = mongo.db.answers.find_one({"user_id": current_user.id, "subject": selected_sub})
    if existing_submission:
        mongo.db.answers.update_one(
            {"user_id": current_user.id, "subject": selected_sub},
            {"$set": {"answers": answers}}
        )
        flash("Your answers have been updated successfully!")
    else:
        mongo.db.answers.insert_one({
            "user_id": current_user.id,
            "subject": selected_sub,
            "answers": answers,
        })
        flash("Answers submitted successfully!")

    return redirect(url_for('review'))  # Redirect to Subject 2 Next form


@app.route('/subject2_form', methods=['POST'])
@login_required
def subject2_form():
    answers = {
        "Question 1": request.form.get("q1"),
        "Question 2": request.form.get("q2"),
        "Question 3": request.form.get("q3"),
        "Question 4": request.form.get("q4"),
    }
    selected_sub = "subject-2"

    # if not all(answers.values()):
    #     flash("Please answer all questions before submitting.")
    #     return redirect(url_for('subject2_form'))

    existing_submission = mongo.db.answers.find_one({"user_id": current_user.id, "subject": selected_sub})

    if existing_submission:
        mongo.db.answers.update_one(
            {"user_id": current_user.id, "subject": selected_sub},
            {"$set": {"answers": answers}}
        )
        flash("Your answers have been updated successfully!")
    else:
        mongo.db.answers.insert_one({
            "user_id": current_user.id,
            "subject": selected_sub,
            "answers": answers,
        })
        flash("Answers submitted successfully!")

    return render_template('subject2_next.html')

@app.route('/subject2_next', methods=['POST'])
@login_required
def subject2_next():
    answers = {
        "Question 1": request.form.get("q1"),
        "Question 2": request.form.get("q2"),
    }
    selected_sub = "subject-2-next"

    # if not all(answers.values()):
    #     flash("Please answer all questions before submitting.")
    #     return redirect(url_for('subject2_next'))

    # Check if the user already submitted answers
    existing_submission = mongo.db.answers.find_one({"user_id": current_user.id, "subject": selected_sub})
    if existing_submission:
        mongo.db.answers.update_one(
            {"user_id": current_user.id, "subject": selected_sub},
            {"$set": {"answers": answers}}
        )
        flash("Your answers have been updated successfully!")
    else:
        mongo.db.answers.insert_one({
            "user_id": current_user.id,
            "subject": selected_sub,
            "answers": answers,
        })
        flash("Answers submitted successfully!")

    return redirect(url_for('review'))  # Redirect to Subject 3 Next form


@app.route('/subject3_form', methods=['POST'])
@login_required
def subject3_form():
    answers = {
        "Question 1": request.form.get("q1"),
        "Question 2": request.form.get("q2"),
        "Question 3": request.form.get("q3"),
        "Question 4": request.form.get("q4"),
    }
    selected_sub = "subject-3"

    # if not all(answers.values()):
    #     flash("Please answer all questions before submitting.")
    #     return redirect(url_for('subject3_form'))

    existing_submission = mongo.db.answers.find_one({"user_id": current_user.id, "subject": selected_sub})

    if existing_submission:
        mongo.db.answers.update_one(
            {"user_id": current_user.id, "subject": selected_sub},
            {"$set": {"answers": answers}}
        )
        flash("Your answers have been updated successfully!")
    else:
        mongo.db.answers.insert_one({
            "user_id": current_user.id,
            "subject": selected_sub,
            "answers": answers,
        })
        flash("Answers submitted successfully!")

    return render_template('subject3_next.html')  # Redirect to Review page

@app.route('/subject3_next', methods=['POST'])
@login_required
def subject3_next():
    answers = {
        "Question 1": request.form.get("q1"),
        "Question 2": request.form.get("q2"),
    }
    selected_sub = "subject-3-next"

    # if not all(answers.values()):
    #     flash("Please answer all questions before submitting.")
    #     return redirect(url_for('subject3_next'))

    # Check if the user already submitted answers
    existing_submission = mongo.db.answers.find_one({"user_id": current_user.id, "subject": selected_sub})
    if existing_submission:
        mongo.db.answers.update_one(
            {"user_id": current_user.id, "subject": selected_sub},
            {"$set": {"answers": answers}}
        )
        flash("Your answers have been updated successfully!")
    else:
        mongo.db.answers.insert_one({
            "user_id": current_user.id,
            "subject": selected_sub,
            "answers": answers,
        })
        flash("Answers submitted successfully!")

    return redirect(url_for('review'))  # Redirect to Review page

@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    if request.method == 'POST':
        # Logic to update answers (if needed)
        pass

    # Fetch all answers for the current logged-in user
    answers = list(mongo.db.answers.find({"user_id": current_user.id}))

    # Group answers by their logical flow
    grouped_answers = {}
    for answer_set in answers:
        if "subject" in answer_set and answer_set["subject"]:
            base_subject = answer_set["subject"].split("-")[0]  # Get the base subject (e.g., "subject1")
            if base_subject not in grouped_answers:
                grouped_answers[base_subject] = []
            grouped_answers[base_subject].append(answer_set)


    return render_template('review.html', grouped_answers=grouped_answers)


@app.route('/update_answers', methods=['POST'])
@login_required
def update_answers():
    # Parse the form data
    form_data = request.form.to_dict(flat=False)

    for key, value in form_data.items():
        # Process each subject
        if key.startswith("subject["):  
            subject_index = key[8:-1]  
            subject_name = value[0]  

            # Collect answers for this subject
            updated_answers = {
                k.split("][", 1)[-1][:-1]: v[0]
                for k, v in form_data.items()
                if k.startswith(f"answers[{subject_index}]")
            }

            # Update the database for the current subject
            mongo.db.answers.update_one(
                {"user_id": current_user.id, "subject": subject_name},
                {"$set": {"answers": updated_answers}}
            )

    flash("Answers updated successfully!")
    return redirect(url_for('review'))



@app.route('/generate_docx', methods=['GET'])
@login_required
def generate_docx():
    # Fetch answers for the current logged-in user
    answers = list(mongo.db.answers.find({"user_id": current_user.id}))

    # Create a new Document
    doc = Document()
    doc.add_heading('Your Copy of Submitted Answers', 0)

    if answers:
        # Iterate through each answer set and write to the document
        for answer_set in answers:
            subject = answer_set.get("subject", "Unknown Subject")
            doc.add_heading(f"Subject: {subject}", level=1)
            
            # Loop through the answers and add them to the document
            for question, answer in answer_set.get("answers", {}).items():
                doc.add_paragraph(f"{question}: {answer}")
    else:
        doc.add_paragraph("No answers available for review.")

    # Save the document to an in-memory file
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    # Send the file to the user for download
    return send_file(
        file_stream,
        as_attachment=True,
        download_name="review_answers.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )



# Forgot-password route
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        account = mongo.db.accounts.find_one({"email": email})

        if account:
            reset_link = url_for('reset_password', _external=True)
            
            # Create Message object
            msg = Message("Password Reset Request", sender="your-email@example.com", recipients=[email])
            msg.body = f'Hi, {account["username"]}!\n\nClick on the link to reset your password: \n{reset_link}'

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



@app.route('/generate_pdf', methods=['GET'])
@login_required
def generate_pdf():
    # Fetch answers for the current logged-in user
    answers = list(mongo.db.answers.find({"user_id": current_user.id}))

    # Create an in-memory PDF file
    pdf_stream = BytesIO()
    c = canvas.Canvas(pdf_stream, pagesize=letter)

    c.setFont("Helvetica", 12)
    y_position = 750  # starting Y position on the PDF

    c.drawString(100, y_position, 'Your Copy of Submitted Answers')
    y_position -= 30

    if answers:
        # Iterate through each answer set and write to the PDF
        for answer_set in answers:
            subject = answer_set.get("subject", "Unknown Subject")
            c.drawString(100, y_position, f"Subject: {subject}")
            y_position -= 20

            for question, answer in answer_set.get("answers", {}).items():
                c.drawString(100, y_position, f"{question}: {answer}")
                y_position -= 20

            # Add space between subjects
            y_position -= 10
    else:
        c.drawString(100, y_position, "No answers available for review.")
        y_position -= 20

    # Save the PDF to the in-memory stream
    c.showPage()
    c.save()

    # Move back to the beginning of the BytesIO stream
    pdf_stream.seek(0)

    # Send the PDF to the user for download
    return send_file(
        pdf_stream,
        as_attachment=True,
        download_name="review_answers.pdf",
        mimetype="application/pdf"
    )
# Reset password route
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        new_password = request.form.get("new_password")
        username = request.form.get("username")

        # Check if password field is empty
        if not new_password:
            flash("Password cannot be empty")
            return redirect(url_for("reset_password"))

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


    