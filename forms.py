from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, EqualTo

class FuncionarioLoginForm(FlaskForm):

	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submeter = SubmitField('Entrar')


class FuncionarioRegistoForm(FlaskForm):

	nome = StringField('Nome', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirmar = PasswordField('Confirmar Password', validators=[EqualTo('password')])
	nif = StringField('NIF', validators=[DataRequired()])
	telemovel = StringField('Telemóvel', validators=[DataRequired()])
	submeter = SubmitField('Registar')


class ProdutoForm(FlaskForm):

	nome = StringField('Nome', validators=[DataRequired()])
	preco = FloatField('Preço', validators=[DataRequired()])
	descricao = StringField('Descrição')
	categoria = IntegerField('ID da Categoria', validators=[DataRequired()])
	submeter = SubmitField('Gravar')


class CategoriaForm(FlaskForm):

	nome = StringField('Nome da Categoria', validators=[DataRequired()])
	submeter = SubmitField('Gravar')


class LogForm(FlaskForm):

	funcionario_id = IntegerField('ID do Funcionário', validators=[DataRequired()])
	produto_id = IntegerField('ID do Produto', validators=[DataRequired()])
	descricao = StringField('Descrição', validators=[DataRequired()])
	submeter = SubmitField('Registar Log')
