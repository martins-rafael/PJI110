# Projeto Integrador I - Univesp

## PJI110 (Projeto Integrador em Computação I)

**Tema escolhido pelo grupo com base no tema norteador da Univesp:** Desenvolvimento de software com framework web que utilize noções de banco de dados, praticando controle de versão.

**Título provisório do trabalho:** Sistema web de controle de membros para igrejas

<br>


## Tecnologias e Ferramentas

Tecnologias utilizadas no desenvolvimento do projeto:

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLite](https://sqlite.org/index.html)
- [PostgreSQL](https://www.postgresql.org/)
- [Figma](https://www.figma.com/)
- [Bootstrap](https://getbootstrap.com/)
- [VS Code](https://code.visualstudio.com/)

<br>

## Estrutura da aplicação

```
SJBV-PI1
    ├── app
    │   ├── static
    │   │   └── style.css
    │   │
    │   ├── templates
    │   │   ├── auth
    │   │   │   └── login.html
    │   │   │
    │   │   ├── main
    │   │   │   ├── create.html
    │   │   │   ├── edit.html
    │   │   │   ├── index.html
    │   │   │   ├── member.html
    │   │   │   ├── members.html
    │   │   │   └── password.html
    │   │   │
    │   │   ├── partials
    │   │   │   └── header.html
    │   │   │
    │   │   └── base.html
    │   │
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── db.py
    │   ├── main.py
    │   └── schema.sql
    │
    ├── .gitignore
    ├── README.md
    └── requirements.txt
```


## Requisitos

Para rodar a aplicação, você precisa ter o [Python](https://www.python.org/) instalado em sua máquina.

<br>


## Contribuindo com o projeto

Dê um fork neste repositório e em seguida clone o mesmo para sua máquina

1 - Entre na pasta web com
```
cd SJBV-PI1
```

2 - Crie um ambiente virtual com o comando
```
python -m venv venv
```

3 - Ative o ambiente virtual
```
source venv/Scripts/activate
```

4 - Instale as dependências com
```
pip install -r requirements.txt
```

5 - Inicie o banco de dados de desenvolvimento
```
flask init-db
```

6 - Rode a aplicação
```
flask run --debug
```

7 - Acesse http://localhost:5000 no seu navegador.

<br>


## Licença

<a href="https://opensource.org/licenses/MIT">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-ff375f?style=flat-square">
</a>

<br>
Esse projeto está sob a licença MIT. Veja o arquivo [LICENSE](/LICENSE) para mais detalhes.