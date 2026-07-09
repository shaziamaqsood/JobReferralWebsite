from flask import Flask, render_template, request, redirect, session
from database import get_connection
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "jobportal123"
app.permanent_session_lifetime = timedelta(days=7)


# Home page
@app.route("/")
def home():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
    jobs = cursor.fetchall()

    conn.close()

    return render_template("index.html", jobs=jobs)



# All jobs page
@app.route("/jobs")
def jobs():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
    jobs = cursor.fetchall()

    conn.close()

    return render_template("jobs.html", jobs=jobs)



# Job details
@app.route("/job/<int:id>")
def job_detail(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM jobs WHERE id=%s",
        (id,)
    )

    job = cursor.fetchone()

    conn.close()

    return render_template(
        "job_detail.html",
        job=job
    )



# Admin login
@app.route("/admin/login", methods=["GET","POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "Shazia Maqsood" and password == "12082003":

            session["admin"] = True

            return redirect("/admin")

    return render_template("admin_login.html")



# Admin dashboard
@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/admin/login")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        jobs=jobs
    )



# Add job
@app.route("/add_job", methods=["GET","POST"])
def add_job():

    if "admin" not in session:
        return redirect("/admin/login")


    if request.method == "POST":

        data = (
            request.form["title"],
            request.form["company"],
            request.form["skills"],
            request.form["pay"],
            request.form["openings"],
            request.form["description"],
            request.form["referral_link"],
            request.form["category"],
            request.form["posted_date"]
        )


        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute(
        """
        INSERT INTO jobs
        (title,company,skills,pay,openings,description,referral_link,category,posted_date)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        data
        )


        conn.commit()
        conn.close()

        return redirect("/admin")


    return render_template("add_job.html")



# Logout
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)