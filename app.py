from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from flask import send_from_directory

from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "manuelduarte077"

# Conexion a la base de datos
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'empleados_flask'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA


@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)


@app.route('/')
def index():
    sql = "SELECT * FROM `empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    empleados = cursor.fetchall()
    print(empleados)

    conn.commit()
    return render_template('empleados/index.html', empleados=empleados)


@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT image FROM empleados WHERE id=%s", id)
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM empleados WHERE  id = %s", (id))
    conn.commit()

    return redirect("/")


@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id = %s", (id))

    empleados = cursor.fetchall()
    conn.commit()

    return render_template('empleados/edit.html', empleados=empleados)


@app.route('/update', methods=['POST'])
def update():
    _name = request.form['txtName']
    _lastName = request.form['txtLastName']
    _email = request.form['txtEmail']

    _image = request.files['txtImage']
    id = request.form['id']

    sql = "UPDATE empleados SET name=%s, lastName=%s, email=%s WHERE id=%s;"

    datos = (_name, _lastName, _email, id)

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _image.filename != '':
        newNameImage = tiempo + _image.filename
        _image.save("uploads/" + newNameImage)

        cursor.execute("SELECT image FROM empleados WHERE id=%s", id)
        fila = cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE empleados SET image=%s WHERE id=%s", (newNameImage, id))
        conn.commit()

    cursor.execute(sql, datos)
    conn.commit()

    return redirect("/")


@app.route('/create')
def create():
    return render_template('empleados/create.html')


@app.route('/store', methods=['POST'])
def storage():
    _name = request.form['txtName']
    _lastName = request.form['txtLastName']
    _email = request.form['txtEmail']

    _image = request.files['txtImage']

    if _name == '' or _lastName == '' or _email == '' or _image == '0':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('create'))

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _image.filename != '':
        newNameImage = tiempo + _image.filename
        _image.save("uploads/" + newNameImage)

    sql = "INSERT INTO `empleados_flask`.`empleados`(`name`, `lastName`, `email`, `image`) VALUES(%s, %s, %s, %s);"

    datos = (_name, _lastName, _email, newNameImage)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
