from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)

# Conexion a la base de datos
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'empleados_flask'
mysql.init_app(app)


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

    cursor.execute("DELETE FROM empleados WHERE  id = %s", (id))
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

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _image.filename != '':
        newNameImage = tiempo + _image.filename
        _image.save("uploads/"+newNameImage)

    sql = "INSERT INTO `empleados_flask`.`empleados`(`name`, `lastName`, `email`, `image`) VALUES(%s, %s, %s, %s);"

    datos = (_name, _lastName, _email, newNameImage)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return render_template('empleados/index.html')


if __name__ == '__main__':
    app.run(debug=True)
