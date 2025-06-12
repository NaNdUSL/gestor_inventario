from flask import Flask, flash, render_template, redirect, url_for, request
from models import db, Produto, Utilizador, Categoria, Log
from forms import ProdutoForm, LoginForm, RegistoForm, CategoriaForm, FuncionarioEditarForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import or_
from datetime import datetime
import pytz

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
	return Utilizador.query.get(int(user_id))


@app.before_request
def criar_bd():
	db.create_all()


@app.route('/')
def index():
	return redirect(url_for('painel'))


@app.route('/painel', methods=['GET', 'POST'])
@login_required
def painel():
	pesquisa = request.args.get('pesquisa', '', type=str)

	if request.method == 'POST':
		opt = request.form.get('opt', 'produtos')
	else:
		opt = request.args.get('opt', 'produtos')

	if opt == 'produtos':
		if pesquisa:
			produtos = Produto.query.filter(or_(Produto.nome.contains(pesquisa), Produto.descricao.contains(pesquisa))).all()
		else:
			produtos = Produto.query.all()

		categorias = []
	else:
		if pesquisa:
			categorias = Categoria.query.filter(Categoria.nome.contains(pesquisa)).all()
		else:
			categorias = Categoria.query.all()
		produtos = []

	return render_template('painel.html', opt=opt, produtos=produtos, categorias=categorias, pesquisa=pesquisa)



@app.route('/produtos/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar():

	form = ProdutoForm()
	form.categoria.choices = [(c.id, c.nome) for c in Categoria.query.order_by(Categoria.nome).all()]

	if form.validate_on_submit():
		produto = Produto(nome=form.nome.data, preco=form.preco.data, descricao=form.descricao.data, categoria_id=form.categoria.data, quantidade=form.quantidade.data)
		db.session.add(produto)
		db.session.commit()

		log = Log(utilizador_id=current_user.id, descricao=f"Adicionado o produto '{produto.nome}'" )
		db.session.add(log)
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

		log = Log(utilizador_id=current_user.id, descricao=f"Adicionada a categoria '{nova_categoria.nome}'")
		db.session.add(log)
		db.session.commit()

		return redirect(url_for('painel') + '?opt=categorias')

	return render_template('adicionar_categoria.html', form=form)


@app.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):

	categoria = Categoria.query.get_or_404(id)
	form = CategoriaForm(obj=categoria)

	if form.validate_on_submit():
		form.populate_obj(categoria)
		db.session.commit()

		log = Log(utilizador_id=current_user.id, descricao=f"Editada a categoria '{categoria.nome}'")
		db.session.add(log)
		db.session.commit()

		return redirect(url_for('painel') + '?opt=categorias')

	return render_template('editar_categoria.html', form=form)


@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):

	produto = Produto.query.get_or_404(id)
	form = ProdutoForm(obj=produto)
	form.categoria.choices = [(c.id, c.nome) for c in Categoria.query.order_by(Categoria.nome).all()]

	if form.validate_on_submit():

		produto.nome = form.nome.data
		produto.preco = form.preco.data
		produto.descricao = form.descricao.data
		produto.categoria_id = form.categoria.data
		db.session.commit()

		log = Log(utilizador_id=current_user.id, descricao=f"Editado o produto '{produto.nome}'")
		db.session.add(log)
		db.session.commit()

		return redirect(url_for('painel'))

	return render_template('editar.html', form=form)


@app.route('/apagar_categoria/<int:id>', methods=['GET', 'POST'])
@login_required
def apagar_categoria(id):
	categoria = Categoria.query.get_or_404(id)
	produtos_com_categoria = Produto.query.filter_by(categoria_id=id).all()
	
	if request.method == 'POST':
		if request.form.get('confirmar') == 'sim':
			for p in produtos_com_categoria:
				p.categoria_id = None
			db.session.delete(categoria)
			db.session.commit()

			log = Log(utilizador_id=current_user.id, descricao=f"Apagada a categoria '{categoria.nome}'")
			db.session.add(log)
			db.session.commit()

			flash(f"Categoria '{categoria.nome}' apagada com sucesso.", 'success')
			return redirect(url_for('painel', opt='categorias'))
		else:
			return redirect(url_for('painel', opt='categorias'))

	if produtos_com_categoria:
		return render_template('confirmar_apagar_categoria.html', categoria=categoria, produtos=produtos_com_categoria)
	else:
		db.session.delete(categoria)
		db.session.commit()
		flash(f"Categoria '{categoria.nome}' apagada com sucesso.", 'success')
		return redirect(url_for('painel', opt='categorias'))


@app.route('/produtos/apagar/<int:id>')
@login_required
def apagar(id):

	produto = Produto.query.get_or_404(id)
	db.session.delete(produto)
	db.session.commit()

	log = Log(utilizador_id=current_user.id, descricao=f"Apagado o produto '{produto.nome}'")
	db.session.add(log)
	db.session.commit()

	return redirect(url_for('painel'))


@app.route('/ajustar_quantidade/<int:id>', methods=['POST'])
def ajustar_quantidade(id):
	produto = Produto.query.get_or_404(id)
	try:
		ajuste = int(request.form['quantidade'])
	except ValueError:
		flash('Quantidade inválida.', 'danger')
		return redirect(url_for('painel', opt='produtos'))

	nova_quantidade = produto.quantidade + ajuste
	if nova_quantidade < 0:
		flash('Não pode reduzir a quantidade para um valor negativo.', 'danger')
		return redirect(url_for('painel', opt='produtos'))

	produto.quantidade = nova_quantidade
	db.session.commit()
	flash('Quantidade ajustada com sucesso.', 'success')

	log = Log(utilizador_id=current_user.id, descricao=f"Ajustada a quantidade de '{produto.nome}' para {nova_quantidade}")
	db.session.add(log)
	db.session.commit()

	return redirect(url_for('painel', opt='produtos'))


@app.route('/logs')
@login_required
def listar_logs():
	cargo_filter = request.args.get('cargo', '').strip()
	nome_filter = request.args.get('nome', '').strip()
	descricao_filter = request.args.get('descricao', '').strip()
	data_inicio_str = request.args.get('data_inicio', '').strip()
	data_fim_str = request.args.get('data_fim', '').strip()

	data_inicio = None
	data_fim = None
	fmt = "%Y-%m-%d %H:%M"
	fmt_date_only = "%Y-%m-%d"

	try:
		if data_inicio_str:
			try:
				data_inicio = datetime.strptime(data_inicio_str, fmt)
			except ValueError:
				data_inicio = datetime.strptime(data_inicio_str, fmt_date_only)
		if data_fim_str:
			try:
				data_fim = datetime.strptime(data_fim_str, fmt)
			except ValueError:
				data_fim = datetime.strptime(data_fim_str, fmt_date_only)
				data_fim = data_fim.replace(hour=23, minute=59, second=59)
	except Exception:
		pass

	if current_user.cargo == 'admin':
		query = Log.query.join(Log.utilizador)

		if cargo_filter:
			query = query.filter(Utilizador.cargo == cargo_filter)

		if nome_filter:
			query = query.filter(Utilizador.nome.ilike(f'%{nome_filter}%'))

		if data_inicio:
			query = query.filter(Log.data >= data_inicio)
		if data_fim:
			query = query.filter(Log.data <= data_fim)

		logs = query.order_by(Log.data.desc()).all()

	else:
		query = Log.query.filter_by(utilizador_id=current_user.id)

		if descricao_filter:
			query = query.filter(Log.descricao.ilike(f'%{descricao_filter}%'))

		if data_inicio:
			query = query.filter(Log.data >= data_inicio)
		if data_fim:
			query = query.filter(Log.data <= data_fim)

		logs = query.order_by(Log.data.desc()).all()

	return render_template('logs.html', logs=logs, cargo_filter=cargo_filter, nome_filter=nome_filter, descricao_filter=descricao_filter, data_inicio=data_inicio_str, data_fim=data_fim_str)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = Utilizador.query.filter_by(email=form.email.data).first()

		if user and user.check_password(form.password.data):
			login_user(user)

			if user.cargo == 'admin':
				return redirect(url_for('lista_funcionarios'))
			else:
				return redirect(url_for('painel'))

		flash("Credenciais erradas. Tente novamente.", "danger")

	return render_template('login.html', form=form)


@app.route('/registo', methods=['GET', 'POST'])
def registo():

	form = RegistoForm()

	if form.validate_on_submit():
		nome = form.nome.data.strip()
		email = form.email.data.strip()
		nif = form.nif.data.strip()
		telemovel = form.telemovel.data.strip()
		password = form.password.data.strip()

		if not nome or not password:
			flash("Preencha todos os campos corretamente.", "erro")
			return render_template('registo.html', form=form)

		if Utilizador.query.filter_by(email=email).first():
			flash("O utilizador já existe, escolha outro email.", "erro")
			return render_template('registo.html', form=form)

		novo_utilizador = Utilizador(nome=nome, email=email, nif=nif, telemovel=telemovel, cargo='funcionario')
		novo_utilizador.set_password(password)
		db.session.add(novo_utilizador)
		db.session.commit()
		flash("Registo efetuado com sucesso!", "sucesso")

		log = Log(utilizador_id=current_user.id, descricao=f"Registado o novo funcionário '{novo_utilizador.nome}'")
		db.session.add(log)
		db.session.commit()

		return redirect(url_for('lista_funcionarios'))

	return render_template('registo.html', form=form)


@app.route('/lista_funcionarios')
@login_required
def lista_funcionarios():
	if current_user.cargo != 'admin':
		return "Acesso negado", 403

	filtro_texto = request.args.get('nome', '').strip()
	cargo_filtro = request.args.get('cargo', '').strip()

	query = Utilizador.query

	if filtro_texto:
		like_pattern = f"%{filtro_texto}%"
		query = query.filter(or_(Utilizador.nome.ilike(like_pattern), Utilizador.email.ilike(like_pattern)))

	if cargo_filtro:
		query = query.filter_by(cargo=cargo_filtro)
	else:
		query = query.filter(Utilizador.cargo.in_(['funcionario', 'admin']))

	funcionarios = query.order_by(Utilizador.nome).all()

	return render_template('lista_funcionarios.html', funcionarios=funcionarios)


@app.route('/funcionarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_funcionario(id):
	if current_user.cargo != 'admin' and current_user.id != id:
		flash("Acesso não autorizado.", "erro")
		return redirect(url_for('painel'))

	funcionario = Utilizador.query.get_or_404(id)
	form = FuncionarioEditarForm(obj=funcionario)

	if form.validate_on_submit():
		funcionario.nome = form.nome.data
		funcionario.email = form.email.data
		funcionario.nif = form.nif.data
		funcionario.telemovel = form.telemovel.data

		if form.password.data:
			funcionario.set_password(form.password.data)

		db.session.commit()
		flash("Funcionário atualizado com sucesso!", "sucesso")

		log = Log(utilizador_id=current_user.id, descricao=f"Editado o funcionário '{funcionario.nome}'")
		db.session.add(log)
		db.session.commit()

		if current_user.cargo == 'admin':
			return redirect(url_for('lista_funcionarios'))
		else:
			return redirect(url_for('painel'))

	return render_template('editar_funcionario.html', form=form)


@app.route('/funcionarios/apagar/<int:id>')
@login_required
def apagar_funcionario(id):
	if current_user.cargo != 'admin':
		flash("Acesso não autorizado.", "erro")
		return redirect(url_for('painel'))

	funcionario = Utilizador.query.get_or_404(id)

	if funcionario.id == current_user.id:
		flash("Não podes apagar a tua própria conta.", "erro")
		return redirect(url_for('lista_funcionarios'))

	log = Log(utilizador_id=current_user.id, descricao=f"Apagado o funcionário '{funcionario.nome}'")
	db.session.add(log)
	db.session.commit()

	db.session.delete(funcionario)
	db.session.commit()
	flash("Funcionário eliminado com sucesso!", "sucesso")

	return redirect(url_for('lista_funcionarios'))


@app.route('/logout')
@login_required
def logout():

	logout_user()
	return redirect(url_for('login'))

@app.template_filter('to_portugal_time')
def to_portugal_time(value):
	if not value:
		return ''
	portugal_tz = pytz.timezone('Europe/Lisbon')
	if value.tzinfo is None:
		value = pytz.utc.localize(value)
	portugal_time = value.astimezone(portugal_tz)
	return portugal_time.strftime('%d-%m-%Y %H:%M:%S')


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