from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Funcionario(db.Model, UserMixin):
	__tablename__ = 'funcionarios'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	nome = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password_hash = db.Column(db.String(200), nullable=False)
	nif = db.Column(db.String(50), unique=True, nullable=False)
	telemovel = db.Column(db.String(16), unique=True, nullable=False)

	logs = db.relationship('Log', backref='funcionario', lazy=True)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

	def check_password(self, password):
		print(f"Checking password for {check_password_hash(self.password_hash, password)}")
		return check_password_hash(self.password_hash, password)


class Categoria(db.Model):
	__tablename__ = 'categorias'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	nome = db.Column(db.String(50), unique=True, nullable=False)

	produtos = db.relationship('Produto', backref='categoria', lazy=True)


class Produto(db.Model):
	__tablename__ = 'produtos'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	nome = db.Column(db.String(50), nullable=False)
	preco = db.Column(db.Float, nullable=False)
	descricao = db.Column(db.String(50))
	categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)


class Log(db.Model):
	__tablename__ = 'logs'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
	descricao = db.Column(db.String(100), nullable=False)
	data = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)