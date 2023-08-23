from flask_restful import Resource, reqparse
from flask import jsonify
from flask_login import login_required
from modules.models.entities import Persona, Genero, Lugar
import datetime

# Definir el analizador de argumentos para las solicitudes POST y PUT
persona_parser = reqparse.RequestParser()
persona_parser.add_argument(
    "nombre", type=str, required=True, help="Nombre es requerido.")
persona_parser.add_argument(
    "apellido", type=str, required=True, help="Apellido es requerido.")
persona_parser.add_argument(
    "email", type=str, required=True, help="Email es requerido.")
# persona_parser.add_argument("birthdate", type=str, required=True, help="Fecha de nacimiento es requerida.")
persona_parser.add_argument("personal_id", type=str,
                            required=True, help="ID personal es requerido.")
persona_parser.add_argument("genero_id", type=int,
                            required=True, help="ID de género es requerido.")
# persona_parser.add_argument("lugar_id", type=int, required=True, help="ID de lugar es requerido.")


class PersonasResource(Resource):
    method_decorators = [login_required]

    def get(self, persona_id=None):
        if persona_id is None:
            datos = []
            personas = Persona.query.all()
            for persona in personas:
                persona_data = persona.serialize()
                persona_data['birthdate'] = persona_data['birthdate'].isoformat()
                persona_data['genero'] = persona.genero.nombre
                datos.append(persona_data)
            return datos, 200
        else:
            persona = Persona.query.get(persona_id)
            if persona:
                return persona.serialize(), 200
            else:
                return {"message": "Persona no encontrada"}, 404

    def post(self):
        args = persona_parser.parse_args()
        print(args)
        try:
            nueva_persona = Persona(
                nombre=args["nombre"],
                apellido=args["apellido"],
                email=args["email"],
                birthdate="2000-01-01",
                personal_id=args["personal_id"],
                genero=Genero.query.get(args["genero_id"]),
                lugar=Lugar.query.get(1)
            )
            resultado = nueva_persona.guardar()
            print(resultado)
            if resultado["Exito"]:
                return {"message": "Persona agregada exitosamente"}, 201
            else:
                return {"message": resultado["MensajePorFallo"]}, 400
        except Exception as e:
            return {"message": str(e)}, 500

    def put(self, persona_id):
        args = persona_parser.parse_args()
        persona = Persona.query.get(persona_id)
        if not persona:
            return {"message": "Persona no encontrada"}, 404
        try:
            persona.nombre = args["nombre"]
            persona.apellido = args["apellido"]
            persona.email = args["email"]
            persona.birthdate = "2000-01-01",
            persona.personal_id = args["personal_id"]
            persona.genero = Genero.query.get(args["genero_id"]),
            persona.lugar = Lugar.query.get(1)
            resultado = persona.guardar()
            if resultado["Exito"]:
                return {"message": "Persona modificada exitosamente"}, 200
            else:
                return {"message": resultado["MensajePorFallo"]}, 400
        except Exception as e:
            return {"message": str(e)}, 500

    def delete(self, persona_id):
        persona = Persona.query.get(persona_id)
        if not persona:
            return {"message": "Persona no encontrada"}, 404
        try:
            resultado = persona.borrar()
            if resultado["Exito"]:
                return {"message": "Persona eliminada exitosamente"}, 200
            else:
                return {"message": resultado["MensajePorFallo"]}, 400
        except Exception as e:
            return {"message": str(e)}, 500
