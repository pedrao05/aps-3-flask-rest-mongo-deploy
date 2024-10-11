from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
import os
from dotenv import load_dotenv

load_dotenv('.cred')

mongo_uri = os.getenv('MONGO_URI')

app = Flask(__name__)
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app, tlsAllowInvalidCertificates=True, tls=True)


# Inserir uma bicicleta
@app.route('/bikes', methods=['POST'])
def cadastrar_bike():
    try:
        data = request.json
        if not all(key in data for key in ("marca", "modelo", "cidade", "status")):
            return jsonify({"erro": "Dados incompletos. Os campos 'marca', 'modelo', 'cidade' e 'status' são obrigatórios."}), 400

        bike_id = mongo.db.bikes.insert_one(data)
        data['_id'] = str(bike_id.inserted_id)

        return jsonify({"mensagem": "Bicicleta inserida com sucesso!", "bicicleta": data}), 201
    
    except Exception as e:
        return {"erro":str(e)}, 500


# Ler todas as bicicletas
@app.route('/bikes', methods=['GET'])
def get_bikes():
    try:
        bikes = list(mongo.db.bikes.find())
        for bike in bikes:
            bike['_id'] = str(bike['_id'])
        return jsonify(bikes), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# Ler apenas uma bicicleta dado um id
@app.route('/bikes/<id>', methods=['GET'])
def get_bike(id):
    try:
        bike = mongo.db.bikes.find_one({"_id": ObjectId(id)})
        if not bike:
            return jsonify({"erro": "Bicicleta não encontrada"}), 404
        else:
            bike['_id'] = str(bike['_id'])
            return jsonify(bike), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# Atualizar uma bicicleta dado um id
@app.route('/bikes/<id>', methods=['PUT'])
def atualizar_bike(id):
    try:
        data = request.json

        if not data:
            return jsonify({"erro": "Dados para atualização não fornecidos"}), 400

        bike = mongo.db.bikes.find_one({"_id": ObjectId(id)})
        if bike:

            mongo.db.bikes.update_one({"_id": ObjectId(id)}, {"$set": data})
            return jsonify({"mensagem": "Bicicleta atualizada com sucesso!"}), 200
        else:
            return jsonify({"erro": "Bicicleta não encontrada"}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# Deletar uma bicicleta dado um id
@app.route('/bikes/<id>', methods=['DELETE'])
def deletar_bike(id):
    try:
        bike = mongo.db.bikes.find_one({"_id": ObjectId(id)})
        if bike:
            mongo.db.bikes.delete_one({"_id": ObjectId(id)})
            return jsonify({"mensagem": "Bicicleta deletada com sucesso!"}), 200
        else:
            return jsonify({"erro": "Bicicleta não encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# Inserir uma usuario
@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    try:
        data = request.json
        if not all(key in data for key in ("nome", "cpf", "data de nascimento")):
            return jsonify({"erro": "Dados incompletos. Os campos 'marca', 'modelo' e 'cidade' são obrigatórios."}), 400

        usuario_id = mongo.db.usuarios.insert_one(data)
        data['_id'] = str(usuario_id.inserted_id)

        return jsonify({"mensagem": "Usuario inserido com sucesso!", "usuario": data}), 201
    
    except Exception as e:
        return {"erro":str(e)}, 500


# Ler todas as usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = list(mongo.db.usuarios.find())
        for usuario in usuarios:
            usuario['_id'] = str(usuario['_id'])
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# Ler apenas uma usuario dado um id
@app.route('/usuarios/<id>', methods=['GET'])
def get_usuario(id):
    try:
        usuario = mongo.db.usuarios.find_one({"_id": ObjectId(id)})
        if not usuario:
            return jsonify({"erro": "Usuario não encontrada"}), 404
        else:
            usuario['_id'] = str(usuario['_id'])
            return jsonify(usuario), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# Atualizar uma usuario dado um id
@app.route('/usuarios/<id>', methods=['PUT'])
def atualizar_usuario(id):
    try:
        data = request.json

        if not data:
            return jsonify({"erro": "Dados para atualização não fornecidos"}), 400

        usuario = mongo.db.usuarios.find_one({"_id": ObjectId(id)})
        if usuario:

            mongo.db.usuarios.update_one({"_id": ObjectId(id)}, {"$set": data})
            return jsonify({"mensagem": "Usuario atualizada com sucesso!"}), 200
        else:
            return jsonify({"erro": "Usuario não encontrada"}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# Deletar uma usuario dado um id
@app.route('/usuarios/<id>', methods=['DELETE'])
def deletar_usuario(id):
    try:
        usuario = mongo.db.usuarios.find_one({"_id": ObjectId(id)})
        if usuario:
            mongo.db.usuarios.delete_one({"_id": ObjectId(id)})
            return jsonify({"mensagem": "usuario deletada com sucesso!"}), 200
        else:
            return jsonify({"erro": "usuario não encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)