# Academia API 🏋️‍♂️

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-00a393.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-orange.svg)

## 📌 Sobre o Projeto

Este é um **projeto autoral** desenvolvido do zero com o objetivo de consolidar conhecimentos avançados em desenvolvimento back-end utilizando **FastAPI**, **SQLAlchemy 2.0**, **Pydantic V2** e os princípios da **Clean Architecture (N-Tier / Domain-Driven Design)**.

A **Academia API** atua como o núcleo operacional de uma academia de ginástica, desenhada para ser consumida por múltiplos clientes simultâneos (Painel Administrativo Web, Tablet do Professor e App Mobile do Aluno). 

Ao longo deste projeto, estou aplicando na prática conceitos como:
* Modelagem de Banco de Dados Relacional complexa (Relacionamentos 1:1, 1:N, N:N).
* Controle de Acesso Baseado em Papéis (RBAC - Admin, Teacher, Receptionist, Student).
* Validação profunda de schemas e sanitização de payloads.
* Segurança de APIs e separação estrita de responsabilidades entre as camadas (Routers, Services, Repositories).

---

## 🚀 Tecnologias Utilizadas

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Assíncrono)
* **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) + `aiosqlite`
* **Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
* **Validação de Dados:** [Pydantic V2](https://docs.pydantic.dev/)
* **Gerenciamento de Pacotes:** [Poetry](https://python-poetry.org/)
* **Segurança:** Hashing de senhas utilizando o moderno algoritmo **Argon2** via `pwdlib`.

---

## 🏗️ Arquitetura

O projeto foi desenhado de forma modular (Domain-Driven), o que permite alta escalabilidade e manutenção simples. As pastas são espelhadas por domínio de negócio:

```text
app/
 ├── models/           # Mapeamento das tabelas do banco de dados (Ex: accounts.py)
 ├── schemas/          # Validações de Entrada/Saída do Pydantic (Segurança e Filtros)
 ├── routers/          # Controladores HTTP puros (Endpoints RESTful)
 ├── core/             # Configurações do banco, segurança e variáveis globais
 ...
```

---

## ⚙️ Funcionalidades (Roadmap)

- [x] Modelagem da Base de Dados (Entity-Relationship)
- [x] Estruturação Base (FastAPI + Alembic)
- [x] Módulo de Contas (Accounts): User, Student e Teacher (Models e Schemas)
- [ ] Autenticação e Autorização (JWT / Hashing)
- [ ] Módulo Financeiro: Planos (Plans) e Matrículas (Enrollments)
- [ ] Módulo Operacional: Fichas de Treino (Workouts) e Exercícios
- [ ] Integração com Catraca: Check-ins baseados em status financeiro

---

## 🛠️ Como rodar o projeto localmente

**1. Clone o repositório**
```bash
git clone https://github.com/SEU-USUARIO/academia-api.git
cd academia-api
```

**2. Instale as dependências com o Poetry**
```bash
poetry install
```

**3. Rode as migrations para criar o banco de dados**
```bash
poetry run alembic upgrade head
```

**4. Inicie o servidor em ambiente de desenvolvimento**
```bash
poetry run fastapi dev app/app.py
```
A API estará disponível em `http://localhost:8000` e a documentação interativa completa do Swagger em `http://localhost:8000/docs`.

---
*Este projeto está sendo construído como prova de conceito e portfólio de Engenharia de Software Back-end.*
