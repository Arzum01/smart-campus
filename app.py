import flask
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3

app = Flask(__name__)
connection = sqlite3.connect("campus.db")
cursor = connection.cursor()
upload_img_folder = os.path.join('static', 'covers')
upload_pdf_folder = os.path.join('secure_storage', 'pdfs')

os.makedirs(upload_img_folder, exist_ok=True)
os.makedirs(upload_pdf_folder, exist_ok=True)

cursor.execute("""CREATE TABLE IF NOT EXISTS menu(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               image_filename TEXT NOT NULL,
               category TEXT NOT NULL,
               price TEXT NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS books(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               image_filename TEXT NOT NULL,
               pdf_filename TEXT NOT NULL)""")

cursor.execute("SELECT COUNT(*) FROM books")
book_count = cursor.fetchone()[0]
if book_count == 0:
    initial_books = [
        {"title": "1984 George Orwell", "img": "georgeOrwell.png", "pdf": "1984-nineteen-eighty-four-george-orwell-obooko.pdf"},
        {"title": "Algorithms Notes", "img": "algorithmNotes.png", "pdf": "AlgorithmsNotesForProfessionals.pdf"},
        {"title": "Anna Karenina", "img": "annaKarenina.png", "pdf": "anna-karenina-obooko.pdf"},
        {"title": "Begin EthicalHacking with Python", "img": "ethicalHacking.png", "pdf": "Begin_Ethical_Hacking_with_Python.pdf"},
        {"title": "CompTIA Security Certification Guide", "img": "comptia.png", "pdf": "CompTIA_Security__Certification_Guide.pdf"},
        {"title": "C++ Notes", "img": "c++Notes.png", "pdf": "CPlusPlusNotesForProfessionals.pdf"},
        {"title": "CSS Notes", "img": "cssNotes.png", "pdf": "CSSNotesForProfessionals.pdf"},
        {"title": "HTML5 Notes", "img": "htmlNotes.png", "pdf": "HTML5NotesForProfessionals.pdf"},
        {"title": "Industrial Engineering and Management", "img": "ieManage.png", "pdf": "Industrial Engineering And Management.pdf"},
        {"title": "Introduction to Machine Learning", "img": "IntroMachLearn.png", "pdf": "Introduction to Machine Learning with Python.pdf"},
        {"title": "IOS Notes", "img": "iosDev.png", "pdf": "iOSNotesForProfessionals.pdf"},
        {"title": "Introduction to Statistical Learning", "img": "introStatisLearning.png", "pdf": "ISLRv2_corrected_June_2023.pdf"},
        {"title": "Jane Eyre", "img": "janeEyre.png", "pdf": "jane-eyre-charlotte-bronte-obooko.pdf"},
        {"title": "Linear Algebra", "img": "linearAlgebra.png", "pdf": "linearAlgebra.pdf"},
        {"title": "Linux Basics for Hackers", "img": "linuxBasics.png", "pdf": "Linux_Basics_for_Hackers_2nd_Edition.pdf"},
        {"title": "Little Women", "img": "littleWomen.png", "pdf": "little-women-or-meg-jo-beth-and-amy-obooko.pdf"},
        {"title": "Real World Bug Hunting", "img": "bugHunting.png", "pdf": "Real-World_Bug_Hunting.pdf"},
        {"title": "Social Engineering", "img": "socialEng.png", "pdf": "Social_Engineering.pdf"},
        {"title": "Sun Also Rises", "img": "obokoSun.png", "pdf": "sun-also-rises-by-ernest-hemingway-free-edition-obooko.pdf"},
        {"title": "The Adventures of Huckleberry", "img": "adventureHucklBe.png", "pdf": "the-adventures-of-huckleberry-finn.pdf"}
    ]

    cursor.executemany(
        "INSERT INTO books (title, image_filename, pdf_filename) VALUES (?, ?, ?)",
        [(b["title"], b["img"], b["pdf"]) for b in initial_books]
    )

cursor.execute("SELECT count(*) FROM menu")
if cursor.fetchone()[0] == 0:
    menu_items = [
        ('Club Sandwich', 'sandwich.jpg', 'student', '6.70azn'),
        ('Caesar Salad', 'salad.jpg', 'student', '5.90azn'),
        ('French Fries', 'fries.jpg', 'student', '3.70azn'),
        ('Doner Kebab', 'doner.jpg', 'student', '6.20azn'),
        ('Coca-cola', 'cola.jpg', 'student', '1.20azn'),
        ("Fanta", "fanta.jpg", "student", '1.20azn'),
        ("Sirab", "sirab.jpg", "student", '0.80azn'),
        ("Tea", "tea.jpg", "student", '0.50azn'),
        ("Plov", "plov.jpg", "teacher", '9.80azn'),
        ("Dolma", "dolma.jpg", "teacher", '8.60azn'),
        ("Paytaxt Salatı", "psalad.jpg", "teacher", '4.90azn'),
        ("Kiyev Kotleti", "kotlet.jpg", "teacher", '12.70azn'),
        ("Fresh Orange Juice", "fresh.jpg", "teacher", '1.90azn'),
        ("Capuccino", "coffee.jpg", "teacher", '1.40azn'),
        ("Sirab", "sirab.jpg", "teacher", '0.80azn'),
        ("Tea", "tea.jpg", "teacher", '0.50azn'),
    ]
    cursor.executemany("INSERT INTO menu(name, image_filename, category, price) VALUES (?,?,?,?)", menu_items)

cursor.execute("""CREATE TABLE IF NOT EXISTS courses(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               course_name TEXT NOT NULL,
               class_number INTEGER NOT NULL,
               professor TEXT NOT NULL,
               date TEXT NOT NULL)""")

cursor.execute("SELECT COUNT(*) FROM courses")
if cursor.fetchone()[0] == 0:
    cursor.execute("""INSERT INTO courses(course_name, class_number, professor, date) VALUES ('Calculus', '127', 'Prof. Aliyev', '2026-09-12' )""")



connection.commit()
connection.close()

@app.route("/")
def home():
    connection = sqlite3.connect('campus.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    
    teacher_menu = cursor.execute("SELECT * FROM menu").fetchall()
    all_courses = cursor.execute("SELECT * FROM courses").fetchall()
    connection.close()

    return render_template('home.html', teacher_menu=teacher_menu, courses=all_courses)

@app.route("/cafeteria")
def cafeteria():
    connection = sqlite3.connect('campus.db')
    connection.row_factory=sqlite3.Row
    cursor = connection.cursor()

    student_menu = cursor.execute("SELECT * FROM menu WHERE category = 'student'").fetchall()
    teacher_menu = cursor.execute("SELECT * FROM menu WHERE category = 'teacher'").fetchall()
    all_courses = cursor.execute("SELECT * FROM courses").fetchall()
    connection.close()

    return render_template('cafeteria.html', student_menu=student_menu, teacher_menu=teacher_menu)

@app.route("/registration", methods = ["GET", "POST"])
def registration():
    connection = sqlite3.connect('campus.db')
    connection.row_factory=sqlite3.Row
    cursor = connection.cursor()
    error_message = None

    if request.method == "POST":
        course_name = request.form["course_name"]
        class_number = request.form["class_number"]
        professor = request.form["professor"]
        date = request.form["date"]

        cursor.execute("SELECT * FROM courses WHERE professor=? AND date=?", (professor, date))
        conflict = cursor.fetchone()

        if conflict:
            error_message = "This professor is already booked for this date. Please choose another date."
        else:
            cursor.execute("""INSERT INTO courses (course_name, class_number, professor, date) VALUES (?,?,?,?)""", 
                       (course_name, class_number, professor, date))
        connection.commit()
        connection.close()

        return redirect(url_for("registration"))
    all_courses = cursor.execute("SELECT * FROM courses").fetchall()
    connection.close()

    return render_template('registration.html', courses=all_courses, error = error_message)

@app.route("/library", methods=['GET', 'POST'])
def library_system():
    connection = sqlite3.connect('campus.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        cover_file = request.files['cover_image']
        pdf_file = request.files['pdf_file']

        if cover_file and pdf_file:
            cover_path = os.path.join(upload_img_folder, cover_file.filename)
            cover_file.save(cover_path)

            pdf_path = os.path.join(upload_pdf_folder, pdf_file.filename)
            pdf_file.save(pdf_path)

            cursor.execute("INSERT INTO books (title, image_filename, pdf_filename) VALUES (?,?,?)",
                           (title, cover_file.filename, pdf_file.filename))
            connection.commit()
            connection.close()
            return redirect(url_for("library_system"))
        
    search_query = request.args.get('search', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page-1)*per_page

    if search_query:
        # Fetch filtered count and books matching the search string
        total_books = cursor.execute("SELECT COUNT(*) FROM books WHERE title LIKE ?", ('%' + search_query + '%',)).fetchone()[0]
        books = cursor.execute("SELECT * FROM books WHERE title LIKE ? LIMIT ? OFFSET ?", ('%' + search_query + '%', per_page, offset)).fetchall()
    else:
        # Fetch everything normally if there is no search query
        total_books = cursor.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        books = cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?", (per_page, offset)).fetchall()
    
    total_pages = max(1, (total_books+per_page-1)//per_page)
    connection.close()

    return render_template("library.html", books=books, page=page, total_pages=total_pages, search_query=search_query)

@app.route("/view_pdf/<filename>")
def view_pdf(filename):
    return send_from_directory(upload_pdf_folder, filename)

app.run(debug=True)