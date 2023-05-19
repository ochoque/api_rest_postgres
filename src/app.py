from flask import Flask, jsonify, request
import psycopg2
#from decouple import config
from flask_cors import CORS, cross_origin

from config import config
from connecion import conneccion
##from validaciones import *

app = Flask(__name__)

# CORS(app)
CORS(app, resources={r"/usuarios/*": {"origins": "http://localhost"}})

##conexion = MySQL(app)
# @cross_origin
@app.route('/usuarios',methods=['GET'])
def listar_cursos():
    try:
        ##return(app.config())
        ##conn = psycopg2.connect(database="db_api_flask", host="localhost", user="postgres", password="postgres", port=5432)
        conn = conneccion()
        cur = conn.cursor()
        cur.execute("select * from usuarios")
        datos=cur.fetchall()
        usuarios = []
        for fila in datos:
            usuario = {'cedula_identidad': fila[0], 
                     'nombre': fila[1],
                     'primer_apellido': fila[2],
                     'segundo_apellido': fila[3],
                     'fecha_nacimiento': fila[4]}
            usuarios.append(usuario)
        return jsonify({'usuarios': usuarios, 'mensaje': "Usuarios listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def leer_usuario(codigo):
    try:
        ##conn = psycopg2.connect(database="db_api_flask", host="localhost", user="postgres", password="postgres", port=5432)
        conn = conneccion()
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuarios WHERE cedula_identidad = %s',(codigo,))
        datos=cur.fetchone()
        if datos != None:
            usuario = {'cedula_identidad': datos[0],'nombre': datos[1],
                       'primer_apellido': datos[2],'segundo_apellido': datos[3],
                       'fecha_nacimiento': datos[4]}
            return usuario
        else:
            return None
    except Exception as ex:
        raise ex

@app.route('/usuarios/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        usuario = leer_usuario(codigo)
        if usuario != None:
            return jsonify({'usuarios': usuario, 'mensaje': "usuario encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/usuarios', methods=['POST'])
def registrar_curso():
    # print(request.json)
    try:
        print(request.json)
        usuario = leer_usuario(request.json['cedula_identidad'])
        if usuario != None:
            return jsonify({'mensaje': "Cedula de identidad  ya existe, no se puede duplicar.", 'exito': False})
        else:
            ##conn = psycopg2.connect(database="db_api_flask", host="localhost", user="postgres", password="postgres", port=5432)
            conn = conneccion()
            cur = conn.cursor()
            cur.execute('INSERT INTO usuarios values(%s,%s,%s,%s,%s)',(request.json['cedula_identidad'],request.json['nombre'], request.json['primer_apellido'],
                                                           request.json['segundo_apellido'],request.json['fecha_nacimiento']))
            
            conn.commit()
            return jsonify({'mensaje': "Usuario registrado.", 'exito': True})
    except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    
@app.route('/usuarios/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    try:
        usuario = leer_usuario(codigo)
        if usuario != None:
            conn = conneccion()
            cur = conn.cursor()
            cur.execute("""UPDATE usuarios SET nombre=%s, primer_apellido=%s, segundo_apellido=%s,
            fecha_nacimiento=%s WHERE cedula_identidad=%s""",
                        (request.json['nombre'], request.json['primer_apellido'],request.json['segundo_apellido'],request.json['fecha_nacimiento'],codigo))
            conn.commit()
                     
            return jsonify({'mensaje': "Curso actualizado.", 'exito': True})
        else:
                return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    


@app.route('/usuarios/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        usuario = leer_usuario(codigo)
        if usuario != None:
            ##conn = psycopg2.connect(database="db_api_flask", host="localhost", user="postgres", password="postgres", port=5432)
            conn = conneccion()
            cur = conn.cursor()
            cur.execute('DELETE FROM usuarios WHERE cedula_identidad = %s',(codigo,))
            conn.commit()
            return jsonify({'mensaje': "Usuario eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

### PROMEDIO DE EDADES
@app.route('/usuarios/promedio-edad',methods=['GET'])
def promedio_ed():
    try:
        conn = conneccion()
        cur = conn.cursor()
        cur.execute("""select avg(extract(year from age(now(),fecha_nacimiento))) 
        as promedio_edades from usuarios""")
        datos=cur.fetchone()
        if datos != None:
            print('verdad')
            return jsonify({'promedio_edad': datos[0], 'exito': True})
        else:
            return jsonify({'mensaje': "No existe promedio.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})



def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0')
