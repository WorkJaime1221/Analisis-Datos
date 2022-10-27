#Seunfo video
#Minuto 10
from flask import (Flask, render_template, url_for, request, redirect, jsonify)
from flask import flash
from flask_mysqldb import MySQL
import os as os
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key ="mineriadedatos"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'
mysql = MySQL(app)

@app.route('/')
def main():
    link = mysql.connection.cursor()
    link.execute("SELECT * FROM employes")
    data = link.fetchall()
    return render_template('index.html',empleados=data)

@app.route('/login')
def login():
    return "En construcción!!!"

@app.route('/viewemployes', methods=['POST', 'GET'])
def viewemployes():
    if request.method == 'POST':
        id = request.form['Documento']
        link = mysql.connection.cursor()
        link.execute("SELECT * FROM employes WHERE Documento = %s", [id])
        data = link.fetchall()
    return jsonify({'htmlresponse': render_template('viewemployes.html', empleados=data)})

@app.route('/addemployes', methods=['POST', 'GET'])
def addemployes():
    if request.method == 'POST':
        Documento = request.form["Documento"]
        Nombres = request.form["Nombres"]
        Apellidos = request.form["Apellidos"]
        link = mysql.connection.cursor()
        link.execute("INSERT INTO `employes` (`Documento`, `Nombres`, `Apellidos`) VALUES(%s,%s,%s)",(Documento, Nombres, Apellidos))
        mysql.connection.commit()
        link.close()
        flash("Empleado registrado correctamente")
        return redirect(url_for('main'))

@app.route('/updateemployes', methods=['POST', 'GET'])
def updateemployes():
    if request.method == 'POST':
        Documento = request.form["Documento"]
        Nombres = request.form["Nombres"]
        Apellidos = request.form["Apellidos"]
        link = mysql.connection.cursor()
        link.execute("UPDATE employes SET Nombres= %s, Apellidos=%s WHERE Documento=%s",(Nombres, Apellidos, Documento))
        mysql.connection.commit()
        link.close()
        flash("Empleado actualizado correctamente")
        return redirect(url_for('main'))

@app.route('/deleteemployes/<string:Documento>', methods=['POST', 'GET'])
def deleteemployes(Documento):
    if request.method == 'GET':
        link = mysql.connection.cursor()
        link.execute("DELETE FROM `employes` WHERE Documento=%s",[Documento])
        mysql.connection.commit()
        link.close()
        flash("Empleado eliminado correctamente")
        return redirect(url_for('main'))

@app.route('/cargarcsv')
def cargarcsv():
    return render_template('cargarcsv.html')

@app.route('/uploadcsv', methods=['POST','GET'])
def uploadcsv():
    if request.method == 'POST':
        upload_file = request.files['csvfile']
        if upload_file.filename != '':

            file_path = os.path.join(app.config['UPLOAD_FOLDER'],
             upload_file.filename)
            upload_file.save(file_path)
            grabarCSV(file_path)
        flash("DataSet Cargado correctamente")
        return redirect(url_for('cargarcsv'))

def grabarCSV(filepath):
    columnas = ['Doumento','Nombres','Apellidos']
    csvData = pd.read_csv(filepath)
    link = mysql.connection.cursor()
    for i, row in csvData.iterrows():
        sql = "INSERT INTO employes (Documento, Nombres, Apellidos) VALUES(%s,%s,%s)"
        valores = (row['Documento'],row['Nombres'],row['Apellidos'])
        link.execute(sql,valores)
        mysql.connection.commit()

    

if __name__=='__main__':
    app.run(port=5000, debug=True)