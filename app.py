from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inmigracion_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('inicio.html')  # Asegúrate de que 'inicio.html' esté en la carpeta 'templates'

@app.route('/registro')
def registro():
    return render_template('registro.html')  # Archivo de registro si lo necesitas

@app.route('/consulta')
def consulta():
    return render_template('consulta.html')  # Archivo de consulta si lo necesitas

@app.route('/consultar', methods=['POST'])
def consultar():
    if request.method == 'POST':
        pasaporte = request.form['documento']
        
        # Crear cursor para la base de datos
        cursor = mysql.connection.cursor()
        
        # Ejecutar consulta
        cursor.execute("SELECT * FROM solicitantes WHERE pasaporte = %s", [pasaporte])
        
        # Obtener resultados
        solicitante = cursor.fetchone()
        
        # Cerrar cursor
        cursor.close()
        
        if solicitante:
            # Si encuentra el solicitante, mostrar sus datos
            return render_template('resultado.html', solicitante=solicitante)
        else:
            # Si no encuentra el solicitante
            return render_template('consulta.html', resultado="No se encontró ningún registro con ese número de pasaporte.")

if __name__ == '__main__':
    app.run(debug=True)

