
from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os


app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='Sistema'
mysql.init_app(app)
CARPETA = os.path.join('uploads')
app.config['CARPETA']=CARPETA


@app.route('/')
def index():
    sql="SELECT * FROM empleados; "
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    print(empleados)
    conn.commit()
    return render_template('empleados/index.html', empleados = empleados)

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():

    _nombre = request.form['txtNombre']    
    _correo = request.form['txtCorreo']    
    _foto=request.files['txtFoto']    

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != "":
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql="INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);" 
    datos = (_nombre,_correo,nuevoNombreFoto)

    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

@app.route('/destroy/<int:id>')
def destroy(id):
    sql =  f"DELETE FROM `empleados` WHERE `empleados`.`id` = {id}"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return redirect("/")


@app.route('/edit/<int:id>')
def edit(id):
    sql = f"SELECT * FROM `empleados` WHERE `empleados`.`id` = {id}"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleado = cursor.fetchall()
    print(empleado)
    conn.commit()
    return render_template("/empleados/edit.html", empleados = empleado)


@app.route('/update/<int:id>',methods=['POST'])
def update(id):
    _nombre = request.form['txtNombre']    
    _correo = request.form['txtCorreo']    
    _foto=request.files['txtFoto'] 
    

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    

    if _foto.filename != "":
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql = "UPDATE empleados SET `nombre` = %s, `correo` = %s, `foto` = %s WHERE `empleados`.`id` = %s;"
    datos = (_nombre, _correo, nuevoNombreFoto, id)
    
    conn = mysql.connect()
    cursor=conn.cursor()
    
    cursor.execute("SELECT foto FROM empleados WHERE id = %s", id)
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    

    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')
    

@app.route('/uploads/<nombreDeLaFoto>')
def uploads(nombreDeLaFoto):
    return send_from_directory(app.config['CARPETA'], nombreDeLaFoto)

if __name__ == "__main__":
    app.run(debug=True)
