from sql_alchemy import banco
import bcrypt


class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    id = banco.Column(banco.Integer, primary_key=True)
    username = banco.Column(banco.String(80), unique=True, nullable=False)
    password = banco.Column(banco.String(128), nullable=False)
    email = banco.Column(banco.String(120), unique=True, nullable=False)
    telefone = banco.Column(banco.String(15), nullable=True)

    def __init__(self, username, email, telefone, password):
        self.username = username
        self.email = email
        self.telefone = telefone
        # Gera um hash seguro da senha usando bcrypt
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # Verifica se a senha fornecida corresponde ao hash armazenado
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }
    
    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
    