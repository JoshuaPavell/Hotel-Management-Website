from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from flask_mysqldb import MySQL
import pdfkit
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, template_folder='template')
app.secret_key = 'tes123'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel'
mysql = MySQL(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jose07pavell@gmail.com'
app.config['MAIL_PASSWORD'] = 'qspmtthgjeocxltv'

mail = Mail(app)

# Set the path to your PDF generation tool (wkhtmltopdf)
pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

@app.route("/")
def home():
    if 'loggedin' in session:
        return render_template('index.html')
    flash('Harap Login dulu','danger')
    return redirect(url_for('login'))

#registrasi
@app.route('/registrasi', methods=('GET','POST'))
def registrasi():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        level = request.form['level']

        #cek username atau email
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_users WHERE username=%s OR email=%s',(username, email, ))
        akun = cursor.fetchone()
        if akun is None:
            cursor.execute('INSERT INTO tb_users VALUES (NULL, %s, %s, %s, %s)', (username, email, generate_password_hash(password), level))
            mysql.connection.commit()
            flash('Registrasi Berhasil','success')
        else :
            flash('Username atau email sudah ada','danger')
    return render_template('registrasi.html')

#login
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        #cek data username
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_users WHERE email=%s',(email, ))
        akun = cursor.fetchone()
        if akun is None:
            flash('Login Gagal, Cek Username Anda','danger')
        elif not check_password_hash(akun[3], password):
            flash('Login gagal, Cek Password Anda', 'danger')
        else:
            session['loggedin'] = True
            session['username'] = akun[1]
            session['level'] = akun[4]
            if session['level'] == 'Admin':
                return redirect(url_for('read'))
            else:
                return redirect(url_for('home'))
    return render_template('login.html')

#logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('level', None)
    return redirect(url_for('login'))

@app.route("/admin")
def read():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customer ORDER BY id DESC")
    datatampil = cur.fetchall()
    cur.close()
    return render_template('admin.html', datapemesan=datatampil)

@app.route('/', methods=['POST'])
def insert():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        phone = request.form['tlp']
        tipe = request.form['tipe']
        checkin = request.form['checkin']
        checkout = request.form['checkout']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer (nama, email, phone, tipe, checkin, checkout) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nama, email, phone, tipe, checkin, checkout))
        mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        email = request.form['email']
        phone = request.form['tlp']
        tipe = request.form['tipe']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        status = request.form['status']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE customer SET nama=%s, email=%s, phone=%s, tipe=%s, checkin=%s, checkout=%s, status=%s WHERE id=%s",
                    (nama, email, phone, tipe, checkin, checkout, status, id))
        mysql.connection.commit()
        flash("Data Berhasil di Update")
    return redirect(url_for('read'))

@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customer WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('read'))

@app.route("/generate_pdf/<int:id>", methods=["GET", "POST"])
def generate_pdf(id):
    if request.method == "POST":
        # Generate the PDF and return the response
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customer WHERE id=%s", (id,))
        customer_data = cur.fetchone()
        cur.close()

        pdf_data = render_template('pdf_template.html', customer_data=customer_data)
        pdf = pdfkit.from_string(pdf_data, False, configuration=pdfkit_config)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=booking_report.pdf'

        return response
    else:
        # Render the template with instructions and form
        return render_template('pdf_instructions.html', id=id)
    
@app.route("/email")
def email():
    return render_template('emailing.html')  

@app.route('/send_email', methods=['POST'])
def send_email():
    sender = request.form['sender']
    recipient = request.form['recipient']
    subject = request.form['subject']
    message = request.form['message']

    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = message

    mail.send(msg)
    flash('Email sent!', 'success')
    return redirect(url_for('email'))

if __name__ == '__main__':
    app.run(debug=True)
