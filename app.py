from flask import Flask
from flask import render_template
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


if __name__ == '__main__':
    app.run(debug=True)
