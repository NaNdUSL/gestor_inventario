import pytest
from flask import Flask
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_painel_default(client):
    """Deve carregar o painel com produtos por padrão"""
    response = client.get('/painel')
    assert response.status_code == 200
    assert b"Lista de Produtos" in response.data

def test_painel_categorias(client):
    """Deve mostrar categorias quando opt=categorias"""
    response = client.post('/painel', data={'opt': 'categorias'})
    assert response.status_code == 200
    assert b"Lista de Categorias" in response.data

def test_pesquisa_produtos(client):
    """Deve aceitar pesquisa e mostrar resultados"""
    response = client.get('/painel?opt=produtos&pesquisa=banana')
    assert response.status_code == 200
    assert b"Produtos" in response.data

def test_botao_trocar_opt(client):
    """Deve manter estado ao mudar de produtos para categorias"""
    response = client.post('/painel', data={'opt': 'produtos'})
    assert response.status_code == 200
    assert b"Lista de Produtos" in response.data

    response = client.post('/painel', data={'opt': 'categorias'})
    assert response.status_code == 200
    assert b"Lista de Categorias" in response.data
