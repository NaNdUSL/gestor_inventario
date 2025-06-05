from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, EqualTo

class LoginForm(FlaskForm):

	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submeter = SubmitField('Entrar')


class RegistoForm(FlaskForm):

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
	categoria = SelectField('ID da Categoria', coerce=int, validators=[DataRequired()])
	submeter = SubmitField('Gravar')


class CategoriaForm(FlaskForm):

	nome = StringField('Nome da Categoria', validators=[DataRequired()])
	submeter = SubmitField('Gravar')


class LogForm(FlaskForm):

	utilizador_id = IntegerField('ID do Utilizador', validators=[DataRequired()])
	produto_id = IntegerField('ID do Produto', validators=[DataRequired()])
	descricao = StringField('Descrição', validators=[DataRequired()])
	submeter = SubmitField('Registar Log')


class FuncionarioEditarForm(FlaskForm):
	nome = StringField('Nome', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	nif = StringField('NIF', validators=[DataRequired()])
	telemovel = StringField('Telemóvel', validators=[DataRequired()])
	password = PasswordField('Nova Password (opcional)')
	submeter = SubmitField('Gravar')