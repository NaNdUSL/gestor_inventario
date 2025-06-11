from app import app, db
from models import Utilizador

with app.app_context():
	db.create_all()

	if not Utilizador.query.first():
		admin = Utilizador(
			nome='Administrador',
			email='admin@example.com',
			nif='123456789',
			telemovel='911111111',
			cargo='admin'
		)
		admin.set_password('admin123')

		funcionario = Utilizador(
			nome='Funcionário',
			email='user@example.com',
			nif='987654321',
			telemovel='922222222',
			cargo='funcionario'
		)
		funcionario.set_password('user123')

		db.session.add(admin)
		db.session.add(funcionario)
		db.session.commit()

		print("Utilizadores criados com sucesso.")
	else:
		print("Utilizadores já existem. Nada foi feito.")