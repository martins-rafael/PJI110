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
- [Neon](https://neon.tech/)
- [Vercel](https://vercel.com/dashboard)
- [Figma](https://www.figma.com/)
- [Bootstrap](https://getbootstrap.com/)
- [VS Code](https://code.visualstudio.com/)

<br>

## Estrutura da aplicação

```
PJI110
    ├── app
    │   ├── static
    │   │   ├── css
    │   │   ├── icons
    │   │   └── js
    │   │
    │   ├── templates
    │   │   ├── announcements
    │   │   ├── auth
    │   │   ├── main
    │   │   └── partials
    │   │
    │   ├── __init__.py
    │   ├── announcements.py
    │   ├── auth.py
    │   ├── db.py
    │   ├── main.py
    │   ├── models.py
    │   └── schema.sql
    │
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    └── vercel.json
```


## Requisitos

Para rodar a aplicação, você precisa ter o [Python](https://www.python.org/) instalado em sua máquina.

<br>


## Contribuindo com o projeto

Dê um fork neste repositório e em seguida clone o mesmo para sua máquina

1 - Entre na pasta web com
```
cd PJI110
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

5 - Crie uma tabela com o nome `igrejaconectada`

6 - Defina a variável de ambiente com os dados para conectar o banco de dados
```
export DATABASE_URL=postgresql://postgres:suasenha@localhost:5432/igrejaconectada
```

7 - Rode as migrations
```
flask db init
flask db migrate
flask db upgrade
```

8 - Rode as aplicação
```
flask run --debug
```

9 - Acesse http://localhost:5000 no seu navegador.

10 - Realize as alterações e crie um pull request.

<br>


## Licença

<a href="https://opensource.org/licenses/MIT">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-0D6EFD?style=flat-square">
</a>

<br>

Esse projeto está sob a licença MIT. Veja o arquivo [License](/License) para mais detalhes.
