# Documentação Técnica: Academia API

## Versão: 1.0.1
## Data: Julho 2026
## Status: Aprovado

---

## Descrição
A **Academia API** é um sistema de back-end robusto focado no gerenciamento completo das operações de uma academia de ginástica, estúdios de musculação ou centros de treinamento cruzado (cross-training). Este documento visa detalhar de forma técnica, porém puramente arquitetural e lógica, todos os requisitos e regras de negócio que deverão ser traduzidos em código durante a fase de implementação.

## Objetivos
- Centralizar a gestão de alunos e suas respectivas assinaturas (planos).
- Controlar acessos físicos (check-in) vinculando o status financeiro e de matrícula à liberação.
- Organizar a montagem, distribuição e acompanhamento de treinos e exercícios pelos professores.
- Manter histórico preciso de avaliações físicas e evolução dos alunos.
- Garantir segurança, consistência e rastreabilidade nas operações financeiras e administrativas.

## Escopo
O escopo engloba desde a modelagem dos dados até a definição de fluxos de caixa básicos (pagamentos de mensalidades), passando por controle de acesso (login, permissões), gestão de recursos humanos (professores e administradores) e controle de frequência.

## Público Alvo
- **Desenvolvedores e Engenheiros de Software:** Encarregados de implementar a API.
- **Gerentes de Projeto/Produto:** Para acompanhamento do cronograma.
- **Stakeholders (Donos da Academia):** Validação das regras de negócio mapeadas.

---

# Índice

1. [Visão Geral](#visão-geral)
2. [Requisitos Funcionais](#requisitos-funcionais)
3. [Requisitos Não Funcionais](#requisitos-não-funcionais)
4. [Modelagem do Banco](#modelagem-do-banco)
5. [Relacionamentos](#relacionamentos)
6. [Regras de Negócio](#regras-de-negócio)
7. [Casos de Uso](#casos-de-uso)
8. [Fluxos](#fluxos)
9. [Endpoints Esperados](#endpoints-esperados)
10. [Códigos HTTP](#códigos-http)
11. [Estrutura Sugerida do Projeto](#estrutura-sugerida-do-projeto)
12. [Roadmap de Desenvolvimento](#roadmap-de-desenvolvimento)
13. [Desafios Extras](#desafios-extras)
14. [Melhorias Futuras](#melhorias-futuras)

---

# Visão Geral

A Academia API atua como o núcleo operacional da academia. Ela processa as requisições enviadas por diferentes clientes (painel web administrativo, aplicativo móvel do aluno, terminal de catraca física) e coordena as regras de negócio antes de persistir as informações no banco de dados.

### Quem utiliza o sistema
1. **Administradores / Recepcionistas:** Gerenciam matrículas, pagamentos, cadastros gerais (planos, professores) e prestam suporte no balcão.
2. **Professores / Personal Trainers:** Avaliam os alunos, montam fichas de treinamento, ajustam exercícios e monitoram o progresso.
3. **Alunos:** Visualizam seus treinos, histórico de avaliações, status financeiro da matrícula e realizam check-in (via app ou biometria integrada à catraca).

### Quais problemas o sistema resolve
- **Inadimplência Oculta:** O sistema bloqueia automaticamente catracas para alunos com pendências ou plano vencido.
- **Fichas de Papel Perdidas:** Digitalização completa do ciclo de treinos, facilitando o acesso ao aluno e atualizações imediatas pelo professor.
- **Falta de Dados Gerenciais:** Consolida informações que podem gerar relatórios de faturamento, horários de pico (via check-ins) e taxa de evasão de alunos.

---

# Requisitos Funcionais

Abaixo estão listados os requisitos funcionais mapeados, ordenados de forma lógica por módulo.

**Módulo: Usuários e Autenticação**
- RF001 - Autenticar usuário no sistema via credenciais de login.
- RF002 - Cadastrar usuários administrativos.
- RF003 - Gerenciar permissões de acesso baseadas em papéis (Admin, Professor, Recepcionista).
- RF004 - Realizar recuperação de senha.

**Módulo: Gestão de Alunos**
- RF005 - Cadastrar um novo aluno.
- RF006 - Atualizar dados cadastrais do aluno.
- RF007 - Consultar perfil do aluno por identificador único.
- RF008 - Listar alunos com paginação e filtros (nome, CPF, status).
- RF009 - Inativar cadastro de aluno.

**Módulo: Gestão de Professores**
- RF010 - Cadastrar novo professor.
- RF011 - Atualizar informações do professor.
- RF012 - Vincular professor a turnos e especialidades.
- RF013 - Listar professores ativos no sistema.

**Módulo: Gestão de Planos e Matrículas**
- RF014 - Criar pacotes/planos de assinatura (ex: Mensal, Trimestral, Anual).
- RF015 - Atualizar valor e regras de um plano (sem afetar matrículas antigas vigentes).
- RF016 - Efetivar matrícula de um aluno vinculando-o a um plano específico.
- RF017 - Renovar matrícula expirada ou prestes a expirar.
- RF018 - Cancelar matrícula antes do prazo (gerenciando status).
- RF019 - Listar histórico de matrículas de um aluno.

**Módulo: Treinos e Exercícios**
- RF020 - Cadastrar catálogo base de exercícios (nome, grupo muscular, descrição).
- RF021 - Criar nova ficha de treino para um aluno.
- RF022 - Atualizar ficha de treino existente.
- RF023 - Adicionar múltiplos exercícios a uma ficha de treino, definindo séries, repetições, carga sugerida e tempo de descanso.
- RF024 - Listar fichas de treino ativas de um aluno.

**Módulo: Check-in**
- RF025 - Registrar check-in de aluno no estabelecimento.
- RF026 - Validar regras de acesso antes de confirmar check-in (pagamento e validade da matrícula).
- RF027 - Consultar histórico de check-ins de um aluno.

**Módulo: Financeiro**
- RF028 - Registrar transação de pagamento referente a uma matrícula.
- RF029 - Listar pagamentos pendentes por período.
- RF030 - Estornar um pagamento.

**Módulo: Avaliação Física**
- RF031 - Registrar nova avaliação física do aluno (peso, altura, % gordura, medidas corporais).
- RF032 - Visualizar histórico evolutivo de avaliações de um aluno específico.

---

# Requisitos Não Funcionais

- **RNF001 - Segurança:** A comunicação deve ocorrer obrigatoriamente sob protocolo HTTPS.
- **RNF002 - Autenticação:** A API utilizará tokens JWT (JSON Web Tokens) contendo claims de identificação e perfil de acesso, com curto tempo de expiração e mecanismo de Refresh Token.
- **RNF003 - Performance:** A API deve responder em menos de 200ms para 95% das requisições de consulta em horário de pico (ex: endpoints de check-in).
- **RNF004 - Banco de Dados:** O sistema deve utilizar um banco de dados relacional robusto para garantir propriedades ACID nas transações financeiras e de matrícula.
- **RNF005 - Escalabilidade:** O design da API deve ser stateless, permitindo balanceamento de carga horizontal através de múltiplos contêineres/servidores.
- **RNF006 - Logs e Auditoria:** Toda operação de exclusão, alteração cadastral ou estorno financeiro deve gerar um log de auditoria associado ao usuário que realizou a ação, incluindo timestamp e IP.
- **RNF007 - Disponibilidade:** A API deve projetar um uptime de 99.9%, visto que a catraca física depende da API para funcionar.

---

# Modelagem do Banco

As tabelas a seguir refletem as entidades que compõem o banco de dados. Os nomes das entidades e suas intenções estão em português para fácil comunicação com stakeholders, **porém os campos estão padronizados em inglês** visando a implementação no código e banco de dados.

### 1. Entidade: Usuário (User)
**Objetivo:** Centralizar o acesso de administradores, recepcionistas, e professores ao painel.
**Descrição:** Armazena credenciais e vincula ao nível de permissão.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| email | String(100) | Sim | N/A | Único, formato de e-mail |
| password_hash | String(255) | Sim | N/A | Senha criptografada |
| role | Enum | Sim | 'STUDENT' | ADMIN, TEACHER, RECEPTIONIST, STUDENT |
| is_active | Boolean | Sim | True | Indica se pode logar |
| created_at | DateTime | Sim | Timestamp | |

### 2. Entidade: Aluno (Student)
**Objetivo:** Dados cadastrais do cliente principal da academia.
**Descrição:** Contém informações pessoais de contato e identificação.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| user_id | UUID | Não | Null | FK (User) Único (1:1) - Login do app |
| full_name | String(150) | Sim | N/A | Min 3 caracteres |
| cpf | String(11) | Sim | N/A | Único, apenas números |
| birth_date | Date | Sim | N/A | Deve ter mais de 14 anos |
| phone | String(15) | Sim | N/A | |
| email | String(100) | Sim | N/A | Único |
| emergency_contact_name | String(150) | Sim | N/A | Nome do contato |
| emergency_contact_phone| String(15) | Sim | N/A | Telefone do contato |
| is_active | Boolean | Sim | True | Para soft delete / inativação |

### 4. Entidade: Professor (Teacher)
**Objetivo:** Dados dos profissionais de educação física.
**Descrição:** Vincula o usuário autenticado aos dados profissionais.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| user_id | UUID | Sim | N/A | FK (User) Único (1:1) |
| full_name | String(150) | Sim | N/A | |
| cref | String(20) | Sim | N/A | Único (Conselho Regional) |
| specialty | String(100) | Não | Null | Ex: Musculação, Pilates |
| is_active | Boolean | Sim | True | Para soft delete / inativação |

### 5. Entidade: Plano (Plan)
**Objetivo:** Modelos de assinaturas vendidos.
**Descrição:** Define preço e duração em meses de cada pacote comercializado.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| name | String(100) | Sim | N/A | Ex: "Plano Anual Premium" |
| description | Text | Não | Null | |
| price | Decimal(10,2) | Sim | N/A | Maior que 0 |
| duration_months | Integer | Sim | N/A | Maior que 0 |
| is_active | Boolean | Sim | True | Planos antigos viram False |

### 6. Entidade: Matrícula (Enrollment)
**Objetivo:** Vínculo de um aluno a um plano num período de tempo.
**Descrição:** Controla a vigência de acesso do aluno.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| student_id | UUID | Sim | N/A | FK (Student) |
| plan_id | UUID | Sim | N/A | FK (Plan) |
| start_date | Date | Sim | N/A | |
| end_date | Date | Sim | N/A | Calculada via duration_months |
| status | String(20) | Sim | 'ACTIVE' | ACTIVE, CANCELED, EXPIRED |

### 7. Entidade: Pagamento (Payment)
**Objetivo:** Histórico de pagamentos das matrículas.
**Descrição:** Essencial para liberar acesso e balanço financeiro.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| enrollment_id | UUID | Sim | N/A | FK (Enrollment) |
| amount | Decimal(10,2) | Sim | N/A | Deve ser >= 0 |
| payment_date | DateTime | Sim | N/A | |
| payment_method | String(50) | Sim | N/A | PIX, CREDIT_CARD, CASH |
| status | String(20) | Sim | 'PENDING' | PENDING, PAID, REFUNDED |

### 8. Entidade: Checkin (Checkin)
**Objetivo:** Registro de frequência física na academia.
**Descrição:** Criado sempre que o aluno passa na catraca.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| student_id | UUID | Sim | N/A | FK (Student) |
| checkin_time | DateTime | Sim | Timestamp | |
| entry_method | String(50) | Sim | 'BIOMETRICS'| BIOMETRICS, APP, MANUAL |

### 9. Entidade: Avaliação Física (PhysicalEvaluation)
**Objetivo:** Histórico de saúde e medidas do aluno.
**Descrição:** Registrado pelos professores esporadicamente.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| student_id | UUID | Sim | N/A | FK (Student) |
| teacher_id | UUID | Sim | N/A | FK (Teacher) |
| evaluation_date| Date | Sim | Data atual | |
| weight_kg | Decimal(5,2) | Sim | N/A | Maior que 0 |
| height_cm | Integer | Sim | N/A | Maior que 0 |
| body_fat_pct | Decimal(5,2) | Não | Null | |
| notes | Text | Não | Null | |

### 10. Entidade: Treino (Workout)
**Objetivo:** A ficha que agrupa os exercícios diários de um aluno.
**Descrição:** Pode ser Treino A, Treino B, etc.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| student_id | UUID | Sim | N/A | FK (Student) |
| teacher_id | UUID | Sim | N/A | FK (Teacher) |
| name | String(50) | Sim | N/A | Ex: "Treino A - Peito" |
| objective | String(100) | Não | Null | Hipertrofia, Emagrecimento |
| created_at | Date | Sim | Data atual | |
| is_active | Boolean | Sim | True | Apenas um conjunto de treinos ativo por aluno |

### 11. Entidade: Exercício (Exercise)
**Objetivo:** Catálogo base de exercícios que existem na academia.
**Descrição:** Cadastrado pelos administradores/professores.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| name | String(100) | Sim | N/A | Ex: "Supino Reto" |
| muscle_group | String(50) | Sim | N/A | Peito, Costas, Pernas, etc |
| description | Text | Não | Null | Como executar |

### 12. Entidade: Treino_Exercicio (WorkoutExercise)
**Objetivo:** Tabela pivô que une o Treino aos seus respectivos Exercícios, adicionando carga e repetição.
**Descrição:** N:N entre Treino e Exercício com atributos extras.

| Campo | Tipo Sugerido | Obrigatório | Valor Padrão | Regras / Restrições |
|---|---|---|---|---|
| id | UUID | Sim | Gerado aut. | PK |
| workout_id | UUID | Sim | N/A | FK (Workout) |
| exercise_id | UUID | Sim | N/A | FK (Exercise) |
| sets | Integer | Sim | N/A | Ex: 3 |
| reps | String(20) | Sim | N/A | Ex: "10 a 12" ou "Falha" |
| suggested_weight| String(20) | Não | Null | Ex: "20kg" |
| rest_seconds | Integer | Não | 60 | Tempo em segundos |
| order_index | Integer | Sim | N/A | Ordem de execução na ficha |

---

# Relacionamentos

A modelagem reflete a realidade operacional de uma academia, garantindo que os dados não fiquem órfãos e mantendo integridade referencial.

**Diagrama de Fluxo e Relacionamentos do Aluno:**

```text
       Plan
         | (1:N) - Um plano serve várias matrículas.
         |
    Enrollment --- (1:N) --- Payment
         |
         | (N:1) - Muitas matrículas pertencem a um aluno (histórico).
         |
       Student
         |
         ├── (1:N) ── Checkin (Um aluno faz muitos check-ins)
         |
         ├── (1:N) ── PhysicalEvaluation (Aluno possui várias ao longo do tempo)
         |                 |
         |                 | (N:1) - Avaliada por um Professor
         |               Teacher
         |                 |
         ├── (1:N) ── Workout (Aluno possui várias fichas como A, B, C)
                           |
                           | (N:1) - Montado por um Professor
```

**Detalhando Relacionamentos:**

- **User (1) : (1) Teacher**
  - **Por quê?** Nem todo usuário é professor (pode ser admin), mas o professor precisa de uma conta de acesso. A tabela teacher complementa a tabela user com dados de CREF e especialidade.

- **Student (1) : (N) Enrollment**
  - **Por quê?** Ao longo dos anos, o aluno pode ter plano semestral, depois cancelar, depois voltar e fazer plano anual. É necessário manter o histórico e nunca sobrescrever a matrícula anterior.

- **Enrollment (1) : (N) Payment**
  - **Por quê?** Um plano anual pode ser parcelado em 12 vezes, gerando 12 registros de pagamento atrelados a uma única matrícula.

- **Workout (1) : (N) WorkoutExercise (N) : (1) Exercise**
  - **Por quê?** Um Treino possui muitos exercícios. Um exercício (ex: Supino) pode estar presente em vários treinos diferentes. O relacionamento N:N exige a tabela associativa `WorkoutExercise`, que guarda os atributos de contexto: "Quantas séries e peso DESTE exercício NESTE treino específico?".

---

# Regras de Negócio

As regras a seguir determinam o comportamento sistêmico da aplicação. Qualquer violação destas regras deverá resultar em exceção de regra de negócio, devolvendo status HTTP 422 (Unprocessable Entity) ou 409 (Conflict).

**Validações Cadastrais**
- **RN01:** Não é permitido o cadastro de dois alunos com o mesmo CPF.
- **RN02:** Não é permitido o cadastro de dois alunos, professores ou usuários com o mesmo e-mail.
- **RN03:** A idade do aluno, calculada a partir da `birth_date`, deve ser no mínimo de 14 anos na data de cadastro.

**Regras de Matrícula**
- **RN04:** Um aluno **não pode** possuir duas matrículas com status `ACTIVE` simultaneamente.
- **RN05:** Ao cancelar uma matrícula antes do vencimento, o status passa a ser `CANCELED` e o acesso será imediatamente revogado.
- **RN06:** Planos marcados como `is_active = False` (inativos) não podem ser utilizados em NOVAS matrículas, porém as matrículas antigas vigentes não sofrem alteração.
- **RN07:** A data de fim (`end_date`) da matrícula deve ser obrigatoriamente calculada pelo sistema somando a quantidade de meses do plano à `start_date`. O usuário não pode enviar essa data manualmente.

**Regras de Acesso e Check-in**
- **RN08:** Check-in só é permitido se houver uma matrícula com status `ACTIVE`.
- **RN09:** Check-in **será negado** se a data atual for maior que a `end_date` da matrícula (Matrícula Vencida).
- **RN10:** Check-in **será negado** se houver algum pagamento associado à matrícula atual com status `PENDING` e com data de vencimento ultrapassada.
- **RN11:** Para evitar fraudes na catraca, um aluno não pode realizar um novo check-in em um intervalo menor que 30 minutos desde seu último check-in bem-sucedido.

**Regras de Treino**
- **RN12:** Apenas professores autenticados (ou admins) podem criar fichas de treino.
- **RN13:** Ao criar uma nova ficha de treino (A, B, C) e marcá-la como `is_active = True`, todas as fichas de treino passadas deste aluno deverão, por questões lógicas de visualização no app, ser agrupadas, e a interface deve priorizar os treinos ativos no momento.
- **RN14:** Um aluno cujo cadastro está inativado (`is_active = False`) não pode receber novas fichas de treino.

**Regras Financeiras**
- **RN15:** O estorno de um pagamento só é possível se o pagamento estava com status `PAID`.
- **RN16:** Quando um pagamento pendente atinge mais de 5 dias de atraso, o sistema (via verificação programada ou de forma lazy na requisição de login/check-in) deve suspender o acesso do aluno temporariamente.

---

# Casos de Uso

### Caso de Uso: Cadastrar Aluno e Criar Matrícula

1. O Administrador acessa a tela de cadastro e envia dados pessoais do aluno.
2. A API valida formatações, CPF e email (verificando unicidade).
3. A API cria o Aluno (Student) e retorna o ID.
4. O Administrador seleciona um Plano disponível.
5. O Administrador define a data de início (`start_date`).
6. A API calcula a `end_date` com base no plano.
7. A API cria a Matrícula (`status` = `ACTIVE`).
8. A API gera os registros na tabela de Pagamento (Payment) (se for pago mensalmente em plano anual, gera 12 registros de pagamento futuro; se for à vista, gera 1 registro).

### Caso de Uso: Registrar Check-in (Catraca)

1. A catraca física (ou aplicativo) lê o cartão/digital do aluno e envia o `student_id` via POST para a API.
2. A API busca a matrícula ativa vinculada ao aluno.
3. Se não houver matrícula ativa, a API devolve erro.
4. Se houver, a API verifica a `end_date`. Se expirada, devolve erro.
5. A API verifica a tabela de Pagamentos para a matrícula. Se houver pagamento vencido, devolve erro.
6. A API verifica se houve um check-in nos últimos 30 minutos. Se sim, devolve erro (Double entry).
7. Estando tudo correto, a API persiste um registro em `Checkin` com a hora atual.
8. A API devolve status de Sucesso para a catraca abrir.

### Caso de Uso: Montar Ficha de Treino

1. O Professor lista os alunos e seleciona um.
2. O Professor cria o escopo do Treino ("Treino A - Peito e Tríceps").
3. O Professor busca exercícios no catálogo.
4. Para cada exercício selecionado, o Professor define Séries (ex: 4), Repetições (ex: 12) e descanso.
5. A API salva o Treino (Workout).
6. A API salva múltiplos registros associativos na tabela `WorkoutExercise` numa única transação.
7. O aluno pode visualizar no seu app em tempo real.

---

# Fluxos

### Fluxo de Renovação de Matrícula

```text
[Início]
   |
   V
[Aluno procura recepção com matrícula vencida]
   |
   V
[Admin seleciona Aluno no sistema] --> (API GET /students/{id})
   |
   V
[Admin escolhe novo Plano (ou mantém anterior)] --> (API GET /plans)
   |
   V
[Admin cria nova Matrícula com data de hoje]
   |
   V
[API processa POST /enrollments]
   |--> Marca antiga como 'EXPIRED' (se não estava).
   |--> Cria nova matrícula como 'ACTIVE'.
   |--> Calcula nova data de fim.
   |--> Gera novos registros em 'Payment'.
   |
   V
[Fim - Aluno apto para Check-in]
```

### Fluxo de Pagamento Atrasado

```text
[Aluno tenta passar na catraca]
   |
   V
[API /checkins recebe a requisição]
   |
   V
[API detecta Pagamento Vencido]
   |--> (status = PENDING e payment_date < data_atual)
   |
   V
[API bloqueia acesso (Erro 403 Forbidden - Mensagem: "Pagamento Pendente")]
   |
   V
[Catraca não abre]
   |
   V
[Aluno vai à recepção, realiza pagamento do título atrasado]
   |
   V
[Admin atualiza pagamento no sistema] --> (API PATCH /payments/{id} para 'PAID')
   |
   V
[Aluno tenta passar novamente]
   |
   V
[API valida, não encontra pendências, insere Checkin e permite acesso (200 OK)]
```

---

# Endpoints Esperados

Esta seção documenta a interface da API. O design obedece às boas práticas RESTful, utilizando os verbos adequados e padrões de URI baseados em recursos.

### Módulo: Autenticação
- **POST `/auth/login`**
  - **Descrição:** Autentica o usuário e devolve o JWT.
  - **Parâmetros Body:** `email`, `password`
  - **Resposta 200:** `{ "access_token": "...", "token_type": "bearer", "expires_in": 3600 }`
  - **Erros:** 401 Unauthorized (Credenciais inválidas).

### Módulo: Alunos (Students)
- **GET `/students`**
  - **Descrição:** Lista alunos paginados.
  - **Parâmetros Query:** `page`, `limit`, `name`, `cpf`, `status`
  - **Resposta 200:** Lista de objetos student.

- **GET `/students/{id}`**
  - **Descrição:** Dados completos de um aluno específico.
  - **Resposta 200:** Objeto Student.
  - **Erros:** 404 Not Found.

- **POST `/students`**
  - **Descrição:** Cria novo aluno.
  - **Body:** `full_name`, `cpf`, `birth_date`, `phone`, `email`, `emergency_contact`
  - **Resposta 201:** Aluno criado.
  - **Erros:** 400 Bad Request, 409 Conflict (CPF/Email já existe), 422 Unprocessable Entity (Idade inválida).

- **PUT `/students/{id}`**
  - **Descrição:** Atualiza dados do aluno.
  - **Resposta 200:** Aluno atualizado.

- **DELETE `/students/{id}`**
  - **Descrição:** Inativa o aluno (Soft Delete - atualiza `is_active` para `false`).
  - **Resposta 204:** No Content.

### Módulo: Planos (Plans)
- **GET `/plans`**
  - **Descrição:** Lista todos os planos disponíveis (ativos por padrão).
- **POST `/plans`**
  - **Descrição:** Cria um novo plano de assinatura.
  - **Body:** `name`, `description`, `price`, `duration_months`

### Módulo: Matrículas (Enrollments)
- **POST `/enrollments`**
  - **Descrição:** Efetiva a matrícula de um aluno.
  - **Body:** `student_id`, `plan_id`, `start_date`
  - **Resposta 201:** Matrícula criada com data de fim calculada e cronograma financeiro (pagamentos) retornados no objeto.
  - **Erros:** 422 (Aluno já possui matrícula ativa).

- **GET `/students/{id}/enrollments`**
  - **Descrição:** Busca o histórico de matrículas do aluno.

- **PATCH `/enrollments/{id}/cancel`**
  - **Descrição:** Cancela uma matrícula antes do prazo (muda o `status` para `CANCELED`).

### Módulo: Financeiro (Payments)
- **GET `/payments`**
  - **Descrição:** Lista pagamentos.
  - **Query:** `status`, `start_date`, `end_date`

- **PATCH `/payments/{id}/pay`**
  - **Descrição:** Marca uma pendência financeira como paga.
  - **Body:** `payment_method` (PIX, CASH, etc)

### Módulo: Treinos (Workouts & Exercises)
- **GET `/exercises`**
  - **Descrição:** Retorna catálogo base de exercícios.

- **POST `/students/{id}/workouts`**
  - **Descrição:** Cria uma ficha de treino para o aluno, incluindo todos os exercícios num único payload.
  - **Body:** `name`, `objective`, `exercises`: [ `{ exercise_id, sets, reps, suggested_weight, rest_seconds, app_index }` ]
  - **Resposta 201:** Ficha montada.

- **GET `/students/{id}/workouts`**
  - **Descrição:** Lista as fichas ativas do aluno para ele acompanhar no aplicativo.

### Módulo: Check-in
- **POST `/checkins`**
  - **Descrição:** Bate o ponto do aluno na catraca.
  - **Body:** `student_id`, `entry_method`
  - **Resposta 200:** Sucesso, catraca liberada.
  - **Erros:**
    - 403 Forbidden: "Matrícula inativa/vencida".
    - 403 Forbidden: "Pagamento pendente".
    - 429 Too Many Requests: "Check-in já realizado nos últimos 30 minutos."

### Módulo: Avaliação Física (Physical Evaluations)
- **POST `/students/{id}/evaluations`**
  - **Descrição:** Grava novas medidas corporais.
  - **Body:** `weight_kg`, `height_cm`, `body_fat_pct`, `notes`

---

# Códigos HTTP

O sistema deve padronizar o retorno dos verbos e códigos de status HTTP conforme a especificação REST:

- **200 OK:** Requisição bem sucedida. Usado em GETs, atualizações (PUT/PATCH) ou em check-in validado.
- **201 Created:** Recurso gerado com sucesso. Usado sempre que um novo registro entra no banco (POST de aluno, treino, matrícula).
- **204 No Content:** Sucesso na requisição, mas sem conteúdo para retornar no body. Ideal para DELETE (soft delete).
- **400 Bad Request:** A requisição foi malformada sintaticamente (falta campo obrigatório no JSON) ou não atende a alguma formatação básica.
- **401 Unauthorized:** O usuário não enviou o Token JWT no header de Authorization, ou o Token expirou/é inválido.
- **403 Forbidden:** O usuário até possui Token válido, mas não tem *permissão* para aquela ação (ex: Um aluno tentando acessar a rota de criação de planos). Também usado no check-in caso a regra de negócio impeça a entrada financeira.
- **404 Not Found:** O recurso solicitado na URL não existe. (ex: buscar um `/alunos/{id_inexistente}`).
- **409 Conflict:** Violação de unicidade no sistema. Exemplo: Tentar criar um aluno com um CPF ou E-mail que já está no banco de dados.
- **422 Unprocessable Entity:** O JSON está bem formado, mas houve falha nas regras de negócio (semântica). Exemplo: `birth_date` indicando que a pessoa tem 10 anos (quando o mínimo é 14) ou tentar cadastrar um treino com um `exercise_id` inválido.
- **500 Internal Server Error:** Ocorreu uma exceção não tratada no backend, erro de conexão com banco de dados. Nunca deve expor stack trace para o cliente, apenas uma mensagem genérica de erro.

---

# Estrutura sugerida do projeto

Esta arquitetura reflete os princípios do Clean Architecture / Padrão de Camadas (N-Tier), isolando regras de negócio da camada de transporte (HTTP) e persistência.

```text
app/
 ├── main/             # Ponto de entrada, configuração do servidor e middlewares.
 ├── core/             # Configurações gerais (variáveis de ambiente, JWT, segurança).
 ├── routers/          # (Controllers) Define os endpoints, recebe requisições, chama serviços.
 ├── schemas/          # Contratos de DTO (Data Transfer Object). Validação de input/output.
 ├── models/           # Definição das entidades do Banco de Dados (mapeamento ORM).
 ├── repositories/     # Abstrai operações diretas com o banco de dados (CRUDs).
 ├── services/         # Coração do sistema: Onde residem todas as Regras de Negócio.
 └── database/         # Configurações de conexão, sessões e inicialização.
```

**Responsabilidades:**
- **routers:** Não possui lógica de negócio nem query de banco. Apenas faz parse do request, injeta dependências e devolve respostas.
- **schemas:** Garante que o JSON que chegou tem as chaves corretas e devolve exatamente o que foi documentado (escondendo a senha hash, por exemplo).
- **services:** Recebe dados limpos, aplica validações complexas (RN01, RN04), orquestra as dependências e manda salvar.
- **repositories:** Os únicos arquivos que conhecem SQL/ORM. Executam `insert`, `select`, `update` no banco.
- **models:** Espelho literal das tabelas do banco.

---

# Roadmap de Desenvolvimento: Por onde começar?

O desenvolvimento da API deve seguir uma abordagem iterativa e orientada a **fatias verticais (Vertical Slices)**. Em vez de criar todo o banco de dados de uma vez (o que pode gerar confusão e retrabalho), você deve implementar entidade por entidade, de ponta a ponta (Model, Schema, Repository, Service e Router), seguindo a ordem estrita de dependências. Se você é o desenvolvedor encarregado, **comece exatamente por aqui**.

### Passo 0: Preparação e Setup Inicial
1. **Configuração de Ambiente:** Inicialize o projeto (FastAPI, pip/poetry), configure o arquivo `.env` para as credenciais do banco.
2. **Conexão com Banco de Dados:** Configure o SQLAlchemy e a ferramenta Alembic. Teste se a aplicação consegue se conectar ao banco de dados relacional.

### Passo 1: Módulo de Usuários, Autenticação e Permissões (User & Role)
*Dependências: Nenhuma.*
1. Crie o Enum de Roles e o Model `User` (contendo o campo `role`).
2. Gere a migration via Alembic e aplique no banco (`alembic revision --autogenerate`).
3. Desenvolva o CRUD completo de `User`, incluindo hash de senhas (com `passlib`).
4. Desenvolva a rota de Login (`POST /auth/login`) gerando o token JWT.
5. Crie a dependência de segurança (ex: `Depends(get_current_user)`) para proteger as próximas rotas validando o Role do usuário.

### Passo 2: Cadastros Base - Alunos (Student) e Professores (Teacher)
*Dependências: User.*
1. Crie os Models `Student` e `Teacher`.
2. Gere as migrations e aplique.
3. Desenvolva o CRUD completo de Alunos e Professores. (Lembre-se que Teacher tem relação 1:1 com User).
4. Proteja as rotas exigindo o JWT criado no Passo 2.

### Passo 4: Catálogos Independentes - Planos (Plan) e Exercícios (Exercise)
*Dependências: Nenhuma.*
1. Crie os Models `Plan` e `Exercise`.
2. Gere as migrations e aplique.
3. Construa o CRUD de ponta a ponta para ambos.

### Passo 5: O Coração Financeiro - Matrículas (Enrollment) e Pagamentos (Payment)
*Dependências: Student e Plan.*
1. Crie os Models `Enrollment` e `Payment`. Gere e aplique as migrations.
2. **Matrículas:** Implemente a criação de matrícula, garantindo as validações de regra de negócio (RN04 a RN07).
3. **Motor Financeiro:** Dentro do Service de criação de Matrícula, insira a lógica que cria os registros na tabela `Payment` (Pagamentos). *Esta etapa deve rodar em uma única transação no banco (ACID).*
4. Desenvolva os endpoints de atualização de Pagamento (ex: Baixa de PIX ou Cartão).

### Passo 6: Operação Diária - Treinos (Workout)
*Dependências: Student, Teacher e Exercise.*
1. Crie os Models `Workout` e `WorkoutExercise` (tabela associativa).
2. Gere as migrations e aplique.
3. Desenvolva a rota que cria a ficha de treino recebendo um payload JSON aninhado (salvando tudo na mesma transação).

### Passo 7: Validação Final - Check-in
*Dependências: Student, Enrollment e Payment.*
1. Crie o Model `Checkin`. Gere a migration e aplique.
2. Construa o endpoint `POST /checkins`.
3. Programe TODAS as condições de bloqueio (RN08 a RN11): verificar pagamento vencido, matrícula expirada e bloqueio de intervalo de tempo.

### Passo 8: Lapidação e Testes
- Adicione as paginações (`limit` / `offset`) nas listagens de GET.
- Escreva testes unitários focados nas regras dos Services.
- Finalize com as rotas e lógicas de Soft Delete.

---

# Desafios Extras

Ao implementar, o time técnico de desenvolvimento deverá se preocupar com os seguintes aspectos complexos:

1. **JWT e Refresh Token:** Como tokens expiram rápido (ex: 1 hora) por segurança, a implementação precisa fornecer rota para trocar um token expirado sem que o usuário faça login novamente com senha.
2. **Rate Limit:** Impedir ataques de força bruta no endpoint de `/auth/login` e requisições massivas no `/checkins`.
3. **Filtros Dinâmicos e Paginação:** Criar endpoints capazes de filtrar `?name=João&status=ACTIVE` com paginação nativa (Limit/Offset).
4. **Soft Delete:** Nunca usar comando DELETE puro. Alunos inativados não devem sumir para não quebrarem o histórico de relatórios financeiros e acesso passado.
5. **Transações (ACID):** Criar uma Matrícula e seus N Pagamentos deve ocorrer dentro da mesma transaction do banco. Se os pagamentos falharem, a matrícula deve ser revertida por rollback.
6. **Docker:** Todo o ambiente deve estar contêinerizado (API e Banco de dados) facilitando testes e padronização entre desenvolvedores.
7. **Pytest (Testes Automatizados):** Regras críticas de validação de datas, cálculo de vencimento e dupla matrícula DEVEM estar cobertas por testes de unidade nos Services.
8. **Permissões Refinadas:** Uma rota de DELETE /plans não pode, em nenhuma hipótese, ser acessada por um papel Professor, apenas Admin.

---

# Melhorias Futuras

As funcionalidades abaixo estão fora do escopo da versão 1.0.0, mas a arquitetura de dados concebida acima já prepara o terreno para suportar essas adições no futuro:

- **Aplicativo Mobile do Aluno:** Onde o próprio aluno lê o Treino e insere a carga real que ele fez naquele dia (histórico de progressão de carga).
- **Pagamento Integrado:** Substituir a baixa manual do pagamento na recepção por Webhooks de provedores (ex: Stripe, Pagar.me, Asaas) informando que o PIX foi pago e a API baixando automático.
- **Catraca Física via TCP/IP:** Criar serviço em background rodando localmente na academia que espelha os dados dessa API na nuvem e destrava catracas físicas por hardware.
- **Reconhecimento Facial:** Alterar o endpoint de checkin para não ser mais envio de ID bruto, mas aceitar validação via integração de API biométrica.
- **Notificações Push / Email:** Disparo automático (Cron Job): "Sua mensalidade vence em 3 dias", ou "Sua matrícula expirou".
- **Agenda de Aulas (CrossFit / Spinning):** Criar reserva de horários limitados nas salas, onde o check-in passa a abater créditos de aula ao invés de livre acesso.

---

# Restrições IMPORTANTES de Engenharia

Para os desenvolvedores encarregados do projeto, atentar-se estritamente às normas abaixo ao transformar este documento em sistema:

1. **Absolutamente todo o retorno de erro deve possuir uma mensagem clara** para o front-end, através de um schema padrão de erro (ex: `{"detail": "Idade inferior ao permitido."}`).
2. **Datas e Timezones devem ser padronizados** para UTC no banco de dados e convertidos apenas nas camadas de apresentação ou mediante necessidade estrita.
3. Não criar regras de negócio na camada de Router.
4. Qualquer script de carga inicial (seed) deverá conter um usuário Admin padrão para acesso inicial ao sistema.
5. Manter os repositórios focados estritamente na interface de acesso ao dado, sem tomadas de decisão lógicas complexas de domínio.

---
**FIM DO DOCUMENTO**
