
# Task Management API

API para gerenciamento de tarefas com autenticação, criação, atualização e visualização de tarefas.

---

## Tecnologias

- Python 3.11
- Django REST Framework
- PostgreSQL
- Docker e Docker Compose
- drf-yasg (Swagger)

---

## Estrutura do Projeto

```
backend/
├── backend/          # Configurações Django
├── core/             # App principal
├── tasks/            # App para tarefas
├── users/            # App para usuários
├── manage.py
requirements.txt
Dockerfile
docker-compose.yaml
.env                 # Variáveis de ambiente (não versionar)
```

---

## Configuração

1. Copie o arquivo `.env.example` para `.env` e configure as variáveis:
```env
SECRET_KEY="django-insecure-7v8g&*o1gl3w+4c9b9x$v(j9=$d$1s%sl7m#m4!@+j)"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

DB_NAME=taskdb
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=task_db
DB_PORT=5432

JWT_SECRET_KEY=supersecretjwtkey
JWT_ACCESS_TOKEN_LIFETIME=60
```

2. Construa e suba os containers:
```bash
docker-compose up --build
```

3. Execute as migrações dentro do container da API:
```bash
docker-compose exec task_api python manage.py migrate
```

---

## Uso

- API rodando em: `http://localhost:8000/`
- Documentação Swagger: `http://localhost:8000/swagger/`

---

## Endpoints principais

- `POST /api/register/` — Registrar novo usuário
- `POST /api/login/` — Login e obtenção de token JWT
- CRUD de tarefas:
  - `GET /api/tasks/`
  - `POST /api/tasks/`
  - `GET /api/tasks/{id}/`
  - `PUT /api/tasks/{id}/`
  - `DELETE /api/tasks/{id}/`

---

## Testes

Para rodar os testes automatizados dentro do container:

```bash
docker-compose exec task_api python manage.py test users
docker-compose exec task_api python manage.py test tasks
```

---

## Dependências principais

- Django REST Framework
- djangorestframework-simplejwt
- drf-yasg
- psycopg2-binary

---

## Swagger

Documentação automática da API em `/swagger/`, gerada pelo drf-yasg.

## Deployment na AWS Elastic Beanstalk

- Conta na AWS
- AWS CLI instalada e configurada (`aws configure`)
- Elastic Beanstalk CLI instalada (`eb cli`)

1. Instale o EB CLI:
```bash
pip3 install awsebcli
```

2. Inicialize seu projeto para o Elastic Beanstalk::
```bash
pip3 install awsebcli
```

3. Criar ambiente para a aplicação::
```bash
eb create nome-do-ambiente
```
3. Configurar env::
```bash
eb setenv SECRET_KEY=seu_secret_key DB_NAME=taskdb DB_USER=postgres DB_PASSWORD=senha DB_HOST=host_db DB_PORT=5432 DEBUG=False
```

4. Fazer o deploy::
```bash
eb deploy
```
5. Depois do deploy o terminal vai fornecer a url para fazer as requisições
