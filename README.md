# Sistema de Gestão de Inventário

Este projeto é uma aplicação web desenvolvida com Flask para a gestão de produtos, categorias e utilizadores, com funcionalidades específicas para perfis de funcionário e administrador.

## Funcionalidades

- Autenticação de utilizadores (admin e funcionário)
- Gestão de produtos
- Gestão de categorias
- Registo automático de logs de atividades
- Interface de pesquisa e filtragem
- Permissões por cargo (admin pode gerir utilizadores)
- Interface em navegadores web
- Base de dados local (SQLite)

## Tecnologias Utilizadas

- Python 3.10.11
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Login
- SQLite

## Instalação

1. Clonar o repositório:
   ```bash
   git clone https://github.com/o_teu_utilizador/gestor-inventario.git
   cd gestor-inventario
   ```

2. Criar e ativar um ambiente virtual (opcional mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```

3. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Correr a aplicação:
   ```bash
   python app.py
   ```

## Estrutura de Ficheiros

- `app.py` — aplicação principal Flask
- `models.py` — definição das tabelas e relações da base de dados
- `forms.py` — definição dos formulários WTForms
- `templates/` — HTMLs com Jinja2
- `static/` — ficheiros CSS
- `requirements.txt` — dependências