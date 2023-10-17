from flask import Flask, jsonify, request
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from flask_cors import CORS  # Importe o CORS
from flask_jwt_extended import JWTManager, create_access_token



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta'
jwt = JWTManager(app)
api = Api(app)
CORS(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

   

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Implemente a lógica para verificar as credenciais no banco de dados
    # Se as credenciais estiverem corretas, crie um token JWT
    if username == 'luiz2' and password == 'suasenha':
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200
    else:
        return {'message': 'Usuário ou senha incorretos'}, 401
    
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


hoteis = []
@app.route('/hoteis', methods=['GET', 'POST'])
def gerenciar_hoteis():
    if request.method == 'POST':
        # Lidar com a solicitação POST para criar um novo hotel
        novo_hotel = request.json  # Os dados do novo hotel são enviados como JSON

        # Adicione o novo hotel à lista de hotéis
        hoteis.append(novo_hotel)

        # Você pode retornar uma resposta de sucesso, se desejar
        return jsonify({"message": "Hotel adicionado com sucesso"}), 201

    elif request.method == 'GET':
        # Lidar com a solicitação GET para obter a lista de hotéis
        return jsonify({"hoteis": hoteis}), 200

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)