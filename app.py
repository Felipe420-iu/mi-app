from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import traceback
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inmigracion_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('inicio.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/consulta')
def consulta():
    return render_template('consulta.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            pasaporte = request.form['pasaporte']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            pais = request.form['pais']
            fecha_solicitud = request.form['fecha_solicitud']
            tipo_visa = request.form['tipo_visa']  # Nuevo campo
            comentarios = request.form.get('comentarios', '')
            correo = request.form.get('correo', '')
            
            # Crear cursor para la base de datos
            cursor = mysql.connection.cursor()
            
            # Ejecutar consulta para insertar datos
            cursor.execute("""
                INSERT INTO solicitantes 
                (pasaporte, nombre, apellido, pais, fecha_solicitud, tipo_visa, comentarios, correo) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [pasaporte, nombre, apellido, pais, fecha_solicitud, tipo_visa, comentarios, correo])
            
            # Confirmar la inserción
            mysql.connection.commit()
            
            # Cerrar cursor
            cursor.close()
            
            # Mensaje de éxito
            return render_template('registro.html', mensaje="¡Registro exitoso! Tus datos han sido guardados.")
            
        except Exception as e:
            # En caso de error, mostrar el mensaje
            error_message = f"Error al registrar: {str(e)}"
            print(error_message)
            print(traceback.format_exc())
            return render_template('registro.html', error=error_message)

@app.route('/consultar', methods=['POST'])
def consultar():
    if request.method == 'POST':
        try:
            # Obtener el número de pasaporte del formulario
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
                
        except Exception as e:
            # En caso de error, mostrar el mensaje
            error_message = f"Error al consultar: {str(e)}"
            print(error_message)
            print(traceback.format_exc())
            return render_template('consulta.html', resultado=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

