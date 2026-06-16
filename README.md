<<<<<<< HEAD
# PeopleFlow


## Tecnologias

- Python 3.12
- Flask com templates Jinja2
- HTML5, CSS3 e JavaScript puro
- SQLAlchemy e Flask-Migrate
- MySQL 8 com PyMySQL
- MongoDB com Flask-PyMongo
- ReportLab para PDF
- Chart.js via CDN
- Docker Compose

## Arquitetura

O projeto segue MVC com Service Layer, Router e Middleware:

- `app/models`: modelos SQLAlchemy
- `app/daos`: acesso aos dados MySQL
- `app/services`: regras de negocio
- `app/controllers`: controllers da aplicacao
- `app/routers`: blueprints e rotas
- `app/middlewares`: autenticacao, log, erro e validacao
- `app/interfaces`: contratos `IDAO`, `IService` e `IController`

## Como rodar

Suba os containers:

```bash
docker compose up --build
```

Em outro terminal, execute as migrations:

```bash
docker compose exec app flask db init
docker compose exec app flask db migrate -m "initial tables"
docker compose exec app flask db upgrade
```

Crie os dados iniciais:

```bash
docker compose exec app flask seed
```

## Acessos

- Aplicacao: <http://localhost:5000>
- phpMyAdmin: <http://localhost:8081>
- mongo-express: <http://localhost:8082>

Usuario inicial:

- E-mail: `admin@peopleflow.com`
- Senha: `admin123`

## Endpoints principais

- `GET /login`
- `GET /register`
- `GET /dashboard`
- `GET /employees`
- `GET /employees/create`
- `POST /employees`
- `GET /employees/<id>`
- `GET /employees/<id>/edit`
- `PUT /employees/<id>`
- `DELETE /employees/<id>`
- `POST /employees/<id>/update`
- `POST /employees/<id>/delete`
- `GET /api/charts/employees-by-department`

## JSON

Tela:

- `GET /imports`

Exportacao:

- `GET /exports/employees.json`
- `GET /exports/departments.json`
- `GET /exports/positions.json`
- `GET /exports/skills.json`

Importacao:

- `POST /imports/employees`
- `POST /imports/departments`
- `POST /imports/positions`
- `POST /imports/skills`

Para colaboradores, o JSON precisa informar pelo menos `position_id`, `name`, `email`, `document`, `admission_date` e `status`.

## Logs XML

- `GET /logs`
- `GET /logs/export.xml`

Filtros opcionais:

- `usuario`
- `acao`
- `data_inicial`
- `data_final`

## Relatorio PDF

- `GET /reports/employees`
- `GET /reports/employees/pdf`

Filtros opcionais:

- `department_id`
- `position_id`
- `status`
- `admission_start`
- `admission_end`

## Observacoes para apresentacao

- O MySQL armazena os dados principais do sistema.
- O MongoDB armazena logs de acesso, login, CRUD, importacao, exportacao, erros e geracao de PDF.
- O middleware de autenticacao protege as rotas privadas usando `session`.
- As senhas sao armazenadas com `generate_password_hash` do Werkzeug.
- O CRUD principal do trabalho e o de colaboradores.
=======
# Trabalho-PythonFlask-RH
Sistema web de gestão de colaboradores e auditoria com Flask, arquitetura MVC, MySQL e MongoDB. Possui autenticação, CRUD completo, logs de auditoria, exportação XML/PDF, dashboard com Chart.js e ambiente Docker para execução.
>>>>>>> d97fb3bbb9005f866eed2b939fba78edcce20ed7
