from flask import Flask, jsonify, request
from flask_restful import Api
from models.hotel import UserModel
from resources.hotel import Hoteis, Hotel
from flask_cors import CORS  # Importe o CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sql_alchemy import banco




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta'
jwt = JWTManager(app)
api = Api(app)
bcrypt = Bcrypt(app)
CORS(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = UserModel.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
    else:
        return {'message': 'Usuário ou senha incorretos'}, 401
      
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    telefone = data.get('telefone')
    email = data.get('email')

    # Verifique se as senhas coincidem
    if password != confirm_password:
        return jsonify({'message': 'As senhas não coincidem'}), 400

    # Verifique se o usuário já existe
    if UserModel.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Crie um novo usuário com a senha seguramente armazenada
    novo_usuario = UserModel(username=username, password=password, telefone=telefone, email=email)
    banco.session.add(novo_usuario)
    banco.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/usuarios/<int:user_id>', methods=['DELETE'])
def deletar_usuario(user_id):
    # Tente encontrar o usuário no banco de dados
    user = UserModel.query.filter_by(id=user_id).first()

    # Se o usuário não for encontrado, retorne uma mensagem de erro
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    # Caso contrário, delete o usuário do banco de dados
    banco.session.delete(user)
    banco.session.commit()

    return jsonify({'message': 'Usuário deletado com sucesso'}), 200


    

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(host='0.0.0.0', port=5000)