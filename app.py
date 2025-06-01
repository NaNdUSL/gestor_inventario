from flask import Flask, flash, render_template, redirect, url_for, request
from models import db, Produto, Funcionario, Categoria
from forms import ProdutoForm, FuncionarioLoginForm, FuncionarioRegistoForm, CategoriaForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import or_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'segredomuitobemguardado'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
	return Funcionario.query.get(int(user_id))


@app.before_request
def criar_bd():
	db.create_all()


@app.route('/')
def index():
	return redirect(url_for('painel'))


# @app.route('/produtos')
# @login_required
# def listar():
# 	pesquisa = request.args.get('pesquisa', '', type=str)
# 	if pesquisa:
# 		produtos = Produto.query.filter(or_(Produto.nome.contains(pesquisa), Produto.descricao.contains(pesquisa))).all()
# 	else:
# 		produtos = Produto.query.all()
# 	return render_template('lista.html', produtos=produtos, pesquisa=pesquisa)



@app.route('/painel', methods=['GET', 'POST'])
@login_required
def painel():
	pesquisa = request.args.get('pesquisa', '', type=str)

	if request.method == 'POST':
		ver = request.form.get('ver', 'produtos')
	else:
		ver = request.args.get('ver', 'produtos')

	if ver == 'produtos':
		if pesquisa:
			produtos = Produto.query.filter(
				or_(
					Produto.nome.contains(pesquisa),
					Produto.descricao.contains(pesquisa)
				)
			).all()
		else:
			produtos = Produto.query.all()
		categorias = []
	else:
		if pesquisa:
			categorias = Categoria.query.filter(
				Categoria.nome.contains(pesquisa)
			).all()
		else:
			categorias = Categoria.query.all()
		produtos = []

	return render_template(
		'painel.html',
		ver=ver,
		produtos=produtos,
		categorias=categorias,
		pesquisa=pesquisa,
	)



@app.route('/produtos/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar():

	form = ProdutoForm()

	if form.validate_on_submit():
		produto = Produto(nome=form.nome.data, preco=form.preco.data, descricao=form.descricao.data, categoria_id=form.categoria.data)
		db.session.add(produto)
		db.session.commit()

		return redirect(url_for('painel'))

	return render_template('adicionar.html', form=form)


@app.route('/categorias/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_categoria():

	form = CategoriaForm()

	if form.validate_on_submit():

		nova_categoria = Categoria(nome=form.nome.data)
		db.session.add(nova_categoria)
		db.session.commit()
		flash("Categoria adicionada com sucesso!", "sucesso")

		return redirect(url_for('painel') + '?ver=categorias')

	return render_template('adicionar_categoria.html', form=form)


@app.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):

	categoria = Categoria.query.get_or_404(id)
	form = CategoriaForm(obj=categoria)

	if form.validate_on_submit():
		form.populate_obj(categoria)
		db.session.commit()

		return redirect(url_for('painel') + '?ver=categorias')

	return render_template('editar_categoria.html', form=form)


@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):

	produto = Produto.query.get_or_404(id)
	form = ProdutoForm(obj=produto)

	if form.validate_on_submit():
		form.populate_obj(produto)
		db.session.commit()

		return redirect(url_for('painel'))

	return render_template('editar.html', form=form)


@app.route('/categorias/apagar/<int:id>')
@login_required
def apagar_categoria(id):

	categoria = Categoria.query.get_or_404(id)
	db.session.delete(categoria)
	db.session.commit()

	return redirect(url_for('painel') + '?ver=categorias')


@app.route('/produtos/apagar/<int:id>')
@login_required
def apagar(id):

	produto = Produto.query.get_or_404(id)
	db.session.delete(produto)
	db.session.commit()

	return redirect(url_for('painel'))


@app.route('/login', methods=['GET', 'POST'])
def login():

	form = FuncionarioLoginForm()

	if form.validate_on_submit():
		user = Funcionario.query.filter_by(email=form.email.data).first()

		if user and user.check_password(form.password.data):
			login_user(user)
			return redirect(url_for('index'))

		return "Login inválido. Tente novamente!"

	return render_template('login.html', form=form)


@app.route('/registo', methods=['GET', 'POST'])
def registo():

	form = FuncionarioRegistoForm()

	if form.validate_on_submit():
		nome = form.nome.data.strip()
		email = form.email.data.strip()
		nif = form.nif.data.strip()
		telemovel = form.telemovel.data.strip()
		password = form.password.data.strip()

		if not nome or not password:
			flash("Preencha todos os campos corretamente.", "erro")
			return render_template('registo.html', form=form)

		if Funcionario.query.filter_by(email=email).first():
			flash("O utilizador já existe, escolha outro email.", "erro")
			return render_template('registo.html', form=form)

		novo_utilizador = Funcionario(nome=nome, email=email, nif=nif, telemovel=telemovel)
		novo_utilizador.set_password(password)
		db.session.add(novo_utilizador)
		db.session.commit()
		flash("Registo efetuado com sucesso!", "sucesso")

		return redirect(url_for('login'))

	return render_template('registo.html', form=form)


@app.route('/logout')
@login_required
def logout():

	logout_user()
	return redirect(url_for('login'))


@app.template_filter('highlight')
def highlight(texto, termo):
	if not texto or not termo:
		return texto or ''

	termo_lower = termo.lower()
	texto_lower = texto.lower()
	start = texto_lower.find(termo_lower)

	if start == -1:
		return texto

	end = start + len(termo)
	highlighted = texto[:start] + '<mark>' + texto[start:end] + '</mark>' + texto[end:]
	return highlighted


if __name__ == "__main__":
	app.run(debug=True)