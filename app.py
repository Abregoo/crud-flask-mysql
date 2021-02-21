from flask import Flask
from flask import render_template, request
from flaskext.mysql import MySQL

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
    sql = "INSERT INTO `empleados_flask`.`empleados`(`name`, `lastName`, `email`) VALUES('Doanald', 'López', 'pepe@gmail.com');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    return render_template('empleados/index.html')


@app.route('/create')
def create():
    return render_template('empleados/create.html')


@app.route('/store', methods=['POST'])
def storage():

    _name = request.form['txtName']
    _lastName = request.form['txtLastName']
    _email = request.form['txtEmail']

    _image = request.files['txtImage']

    sql = "INSERT INTO `empleados_flask`.`empleados`(`name`, `lastName`, `email`, `image`) VALUES(%s, %s, %s, %s);"

    datos = (_name, _lastName, _email, _image.filename)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return render_template('empleados/index.html')


if __name__ == '__main__':
    app.run(debug=True)
