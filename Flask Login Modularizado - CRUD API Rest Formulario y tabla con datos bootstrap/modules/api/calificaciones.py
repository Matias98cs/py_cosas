from flask_restful import Resource, reqparse
from flask import jsonify
from flask_login import login_required
from modules import helpers

calificaciones = [
    {"id": 1,"Nombre": 'Jose', "Clase": "Matemáticas", "Materia": "Álgebra", "Calificacion": 85},
    {"id": 2,"Nombre": 'Jose', "Clase": "Tecnología", "Materia": "Biología", "Calificacion": 92},
    {"id": 3,"Nombre": 'Jose', "Clase": "Historia", "Materia": "Geografía", "Calificacion": 78},
    {"id": 4,"Nombre": 'Jose', "Clase": "Arte", "Materia": "Pintura", "Calificacion": 95},
    {"id": 5,"Nombre": 'Jose', "Clase": "Música", "Materia": "Piano", "Calificacion": 88},
    {"id": 6,"Nombre": 'Jose', "Clase": "Deportes", "Materia": "Fútbol", "Calificacion": 70},
    {"id": 7,"Nombre": 'Jose', "Clase": "Idiomas", "Materia": "Inglés", "Calificacion": 90},
    {"id": 8,"Nombre": 'Jose', "Clase": "Ciencias", "Materia": "Física", "Calificacion": 82},
    {"id": 9,"Nombre": 'Pedro', "Clase": "Matemáticas", "Materia": "Álgebra", "Calificacion": 78},
    {"id": 10,"Nombre": 'Pedro', "Clase": "Tecnología", "Materia": "Biología", "Calificacion": 73},
    {"id": 11,"Nombre": 'Pedro', "Clase": "Historia", "Materia": "Geografía", "Calificacion": 68},
    {"id": 12,"Nombre": 'Pedro', "Clase": "Arte", "Materia": "Pintura", "Calificacion": 91},
    {"id": 13,"Nombre": 'Pedro', "Clase": "Música", "Materia": "Piano", "Calificacion": 73},
    {"id": 14,"Nombre": 'Pedro', "Clase": "Deportes", "Materia": "Fútbol", "Calificacion": 79},
    {"id": 15,"Nombre": 'Pedro', "Clase": "Idiomas", "Materia": "Inglés", "Calificacion": 91},
    {"id": 16,"Nombre": 'Pedro', "Clase": "Ciencias", "Materia": "Física", "Calificacion": 59}
]

# Definir el analizador de argumentos para las solicitudes POST
post_parser = reqparse.RequestParser()
post_parser.add_argument("Nombre", type=str, required=True, help="Nombre es requerido.")
post_parser.add_argument("Clase", type=str, required=True, help="Clase es requerida.")
post_parser.add_argument("Materia", type=str, required=True, help="Materia es requerida.")
post_parser.add_argument("Calificacion", type=int, required=True, help="Calificación es requerida.")

class CalificacionesResource(Resource):
    method_decorators= [login_required]
    
    def get(self):
        return calificaciones, 200

    def post(self):
        args = post_parser.parse_args()
        calificacion_id=0
        if calificaciones:
             calificacion_id=calificaciones[-1]['id'] + 1

        calificacion = {
                "id": calificacion_id,
                "Nombre": args['Nombre'],
                "Clase": args['Clase'],
                "Materia": args['Materia'],
                "Calificacion": args['Calificacion']
        }
        calificaciones.append(calificacion)
        return calificaciones, 201

    def delete(self, calificacion_id):
        global calificaciones

        calificacion = next((c for c in calificaciones if c['id'] == calificacion_id), None)
        if calificacion:
            calificaciones = [c for c in calificaciones if c['id'] != calificacion_id]
            return calificaciones, 201
        else:
            return calificaciones, 404
        

