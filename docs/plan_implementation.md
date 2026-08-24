# Plano de Implementacao - Gym API

Baseado em: `docs/gym_api_documentation.md`  
Ultima revisao manual: 2026-08-05

## Como usar este arquivo

Use os checkboxes para marcar o progresso real da implementacao. A ideia e manter este plano como um mapa simples: primeiro estabilizar a base, depois completar os modulos centrais e, por fim, tratar regras mais avancadas como auditoria, performance e operacao.

Legenda:
- `[x]` Ja existe no projeto, mesmo que possa precisar de ajuste.
- `[ ]` Ainda precisa ser implementado.
- `[~]` Existe parcialmente ou precisa de revisao antes de considerar pronto.

## Estado atual observado

- [x] Projeto FastAPI criado com `app/app.py`.
- [x] Configuracao basica em `app/core/settings.py`.
- [x] Sessao assincrona SQLAlchemy em `app/core/database.py`.
- [x] Alembic configurado.
- [x] Models iniciais de `User`, `Student` e `Teacher`.
- [x] Schemas iniciais de `User`, `Student`, `Teacher` e autentificacao.
- [x] CRUD HTTP inicial para usuarios, alunos e professores.
- [x] Hash de senha com `pwdlib`.
- [x] Login JWT e refresh simples.
- [x] `.env.example` criado com as variaveis obrigatorias atuais.
- [~] Protecao por token existe em rotas, mas RBAC por papel ainda nao.
- [~] Regras de negocio estao implementadas direto nos routers; a documentacao pede separar em services/repositories.
- [~] Autenticacao existe, mas o contrato nao retorna `expires_in` e o refresh token real ainda nao foi modelado.
- [ ] Recuperacao de senha.
- [ ] Planos, matriculas, pagamentos, check-ins, treinos, exercicios e avaliacoes fisicas.
- [ ] Testes automatizados relevantes.
- [ ] Auditoria/logs das operacoes sensiveis.

## Fase 0 - Decisoes base

- [x] Definir padrao de rotas: usar `/api/v1/...`.
- [x] Definir campo de senha: `password` no model armazena hash, nunca senha pura.
- [x] Manter `.env.example` com as variaveis obrigatorias atuais.
- [x] Manter erros com `HTTPException(detail="mensagem clara")`.
- [x] Definir timestamps gerados pela aplicacao em UTC com `utc_now`.
- [ ] Deixar comandos oficiais no README quando estabilizar o fluxo local.
- [ ] Criar testes por modulo conforme cada modulo for fechado.

## Fase 1 - Arquitetura em camadas

Objetivo: alinhar o projeto com a propria documentacao, que pede routers sem regra de negocio e sem query direta.

- [x] Criar pacote `app/repositories/`.
- [x] Criar pacote `app/services/`.
- [x] Extrair queries de usuario para `accounts_repository`.
- [x] Extrair regras de usuario para `accounts_service`.
- [ ] Extrair queries de aluno para `accounts_repository`.
- [ ] Extrair regras de aluno para `accounts_service`.
- [ ] Extrair queries de professor para `accounts_repository`.
- [ ] Extrair regras de professor para `accounts_service`.
- [ ] Manter routers apenas recebendo request, chamando service e retornando response.
- [ ] Cobrir essa refatoracao com testes para evitar regressao no CRUD existente.

## Fase 2 - Usuarios, autenticacao e autorizacao

Requisitos relacionados: RF001, RF002, RF003, RF004, RNF002.

- [x] Criar usuario.
- [x] Listar usuarios autenticado.
- [x] Buscar usuario por ID autenticado.
- [x] Atualizar usuario autenticado.
- [x] Inativar usuario por soft delete.
- [x] Hash de senha.
- [x] Login com JWT.
- [x] Dependencia `get_current_user`.
- [ ] Impedir login de usuario `is_active = False`.
- [ ] Incluir `role` nas claims ou garantir lookup eficiente para autorizacao.
- [ ] Criar dependencia de permissao por papel: Admin, Teacher, Receptionist, Student.
- [ ] Aplicar RBAC nas rotas administrativas.
- [ ] Ajustar response do login para incluir `expires_in`, se mantiver contrato da doc.
- [ ] Decidir se `/refresh_token` atual e suficiente ou se havera refresh token persistido/rotacionado.
- [ ] Implementar recuperacao de senha ou marcar formalmente como fora do MVP.
- [ ] Criar seed de admin padrao para primeiro acesso.
- [ ] Testar login com credenciais invalidas.
- [ ] Testar bloqueio de usuario inativo.
- [ ] Testar permissao negada por role.

## Fase 3 - Alunos

Requisitos relacionados: RF005, RF006, RF007, RF008, RF009, RN01, RN02, RN03, RN15.

- [x] Model `Student`.
- [x] Schema de criacao de aluno.
- [x] Schema publico de aluno.
- [x] Schema de update sem `id` e sem `user_id`.
- [x] Criar aluno.
- [x] Buscar aluno por ID.
- [x] Listar alunos com offset/limit.
- [x] Atualizar aluno.
- [x] Soft delete de aluno.
- [x] Validar CPF com 11 digitos.
- [x] Validar idade minima de 14 anos.
- [x] Validar unicidade de CPF.
- [x] Validar unicidade de e-mail dentro de alunos.
- [~] Filtro existe por busca geral; falta aderir ao contrato `name`, `cpf`, `status`.
- [ ] Verificar e-mail duplicado entre `users`, `students` e `teachers`, conforme RN02.
- [ ] Bloquear operacoes relevantes para aluno inativo.
- [ ] Definir se `is_active` pode ser alterado via PATCH ou apenas por endpoint especifico.
- [ ] Testar cadastro com CPF duplicado.
- [ ] Testar cadastro com e-mail duplicado.
- [ ] Testar aluno menor de 14 anos.
- [ ] Testar filtros e paginacao.

## Fase 4 - Professores

Requisitos relacionados: RF010, RF011, RF012, RF013, RN02, RN15.

- [x] Model `Teacher`.
- [x] Schema de criacao de professor.
- [x] Schema publico de professor.
- [x] Schema de update sem `id` e sem `user_id`.
- [x] Criar professor.
- [x] Buscar professor por ID.
- [x] Listar professores ativos.
- [x] Atualizar professor.
- [x] Soft delete de professor.
- [x] Validar CREF unico.
- [x] Validar user_id unico por professor.
- [ ] Confirmar regra de `user_id`: documentacao diz obrigatorio para professor; model permite nulo.
- [ ] Verificar se o `User` vinculado tem role `TEACHER`.
- [ ] Implementar turnos, caso RF012 entre no MVP.
- [ ] Melhorar especialidades se virar lista/tabela propria.
- [ ] Verificar e-mail duplicado entre `users`, `students` e `teachers`.
- [ ] Testar criacao com usuario inexistente.
- [ ] Testar criacao com usuario ja vinculado.
- [ ] Testar criacao com CREF duplicado.

## Fase 5 - Planos

Requisitos relacionados: RF014, RF015, RN06.

- [ ] Criar model `Plan`.
- [ ] Criar migration de `plans`.
- [ ] Criar schemas `PlanCreate`, `PlanUpdate`, `PlanPublic`, `PlanList`.
- [ ] Validar `price > 0`.
- [ ] Validar `duration_months > 0`.
- [ ] Criar endpoint `GET /api/v1/plans`.
- [ ] Criar endpoint `POST /api/v1/plans`.
- [ ] Criar endpoint `PATCH /api/v1/plans/{plan_id}`.
- [ ] Criar soft delete/inativacao de plano.
- [ ] Garantir que plano inativo nao entra em nova matricula.
- [ ] Testar criacao de plano valido.
- [ ] Testar bloqueio de preco/duracao invalidos.
- [ ] Testar listagem apenas de planos ativos por padrao.

## Fase 6 - Matriculas

Requisitos relacionados: RF016, RF017, RF018, RF019, RN04, RN05, RN06, RN07.

- [ ] Criar enum/status de matricula: `ACTIVE`, `CANCELED`, `EXPIRED`.
- [ ] Criar model `Enrollment`.
- [ ] Criar migration de `enrollments`.
- [ ] Criar schemas de matricula.
- [ ] Endpoint `POST /api/v1/enrollments`.
- [ ] Endpoint `GET /api/v1/students/{student_id}/enrollments`.
- [ ] Endpoint `PATCH /api/v1/enrollments/{enrollment_id}/cancel`.
- [ ] Validar existencia do aluno.
- [ ] Validar existencia do plano.
- [ ] Bloquear nova matricula com plano inativo.
- [ ] Bloquear duas matriculas `ACTIVE` para o mesmo aluno.
- [ ] Calcular `end_date` no service usando `duration_months`.
- [ ] Nao aceitar `end_date` no payload de criacao.
- [ ] Implementar renovacao de matricula vencida.
- [ ] Marcar matriculas antigas como `EXPIRED` quando aplicavel.
- [ ] Testar criacao de matricula.
- [ ] Testar bloqueio de matricula ativa duplicada.
- [ ] Testar cancelamento.
- [ ] Testar historico por aluno.

## Fase 7 - Financeiro

Requisitos relacionados: RF028, RF029, RF030, RN10, RN16, RN17.

- [ ] Criar enum/status de pagamento: `PENDING`, `PAID`, `REFUNDED`.
- [ ] Criar enum/metodo de pagamento: `PIX`, `CREDIT_CARD`, `CASH`.
- [ ] Criar model `Payment`.
- [ ] Adicionar campo de vencimento se a regra de atraso depender de due date; a doc usa `payment_date`, mas a regra fala em vencimento.
- [ ] Criar migration de `payments`.
- [ ] Criar schemas de pagamento.
- [ ] Gerar pagamentos ao criar matricula.
- [ ] Endpoint `GET /api/v1/payments`.
- [ ] Endpoint `PATCH /api/v1/payments/{payment_id}/pay`.
- [ ] Endpoint de estorno, se mantiver RF030.
- [ ] Validar `amount >= 0`.
- [ ] Permitir estorno apenas de pagamento `PAID`.
- [ ] Bloquear acesso quando houver pagamento pendente vencido.
- [ ] Definir implementacao da regra dos 5 dias de atraso.
- [ ] Testar pagamento pendente.
- [ ] Testar pagamento marcado como pago.
- [ ] Testar estorno permitido.
- [ ] Testar estorno negado quando nao estiver `PAID`.

## Fase 8 - Check-ins

Requisitos relacionados: RF025, RF026, RF027, RN08, RN09, RN10, RN11.

- [ ] Criar enum/metodo de entrada: `BIOMETRICS`, `APP`, `MANUAL`.
- [ ] Criar model `Checkin`.
- [ ] Criar migration de `checkins`.
- [ ] Criar schemas de check-in.
- [ ] Endpoint `POST /api/v1/checkins`.
- [ ] Endpoint `GET /api/v1/students/{student_id}/checkins`.
- [ ] Validar existencia do aluno.
- [ ] Bloquear check-in sem matricula ativa.
- [ ] Bloquear check-in com matricula vencida.
- [ ] Bloquear check-in com pagamento pendente vencido.
- [ ] Bloquear check-in repetido em menos de 30 minutos.
- [ ] Retornar `403` para bloqueios de regra de acesso.
- [ ] Retornar `429` para tentativa repetida em menos de 30 minutos.
- [ ] Testar check-in liberado.
- [ ] Testar todos os cenarios de bloqueio.

## Fase 9 - Exercicios e treinos

Requisitos relacionados: RF020, RF021, RF022, RF023, RF024, RN12, RN13, RN14.

- [ ] Criar model `Exercise`.
- [ ] Criar model `Workout`.
- [ ] Criar model associativo `WorkoutExercise`.
- [ ] Criar migrations de exercicios e treinos.
- [ ] Criar schemas de exercicio.
- [ ] Criar schemas de treino com lista de exercicios.
- [ ] Endpoint `GET /api/v1/exercises`.
- [ ] Endpoint `POST /api/v1/exercises`.
- [ ] Endpoint `POST /api/v1/students/{student_id}/workouts`.
- [ ] Endpoint `GET /api/v1/students/{student_id}/workouts`.
- [ ] Endpoint de atualizacao de treino.
- [ ] Criar treino e exercicios associados em uma unica transacao.
- [ ] Validar que apenas `TEACHER` ou `ADMIN` cria ficha de treino.
- [ ] Bloquear treino para aluno inativo.
- [ ] Validar existencia dos exercicios informados.
- [ ] Preservar ordem via `order_index`.
- [ ] Definir comportamento de `is_active` para multiplas fichas do mesmo aluno.
- [ ] Testar criacao de treino completo.
- [ ] Testar permissao negada para role invalida.
- [ ] Testar exercicio inexistente no payload.

## Fase 10 - Avaliacoes fisicas

Requisitos relacionados: RF031, RF032.

- [ ] Criar model `PhysicalEvaluation`.
- [ ] Criar migration de avaliacoes fisicas.
- [ ] Criar schemas de avaliacao.
- [ ] Endpoint `POST /api/v1/students/{student_id}/evaluations`.
- [ ] Endpoint `GET /api/v1/students/{student_id}/evaluations`.
- [ ] Validar existencia do aluno.
- [ ] Validar existencia do professor.
- [ ] Validar `weight_kg > 0`.
- [ ] Validar `height_cm > 0`.
- [ ] Definir permissoes: professor/admin cria, aluno visualiza propria avaliacao.
- [ ] Testar criacao de avaliacao.
- [ ] Testar historico evolutivo.

## Fase 11 - Auditoria, seguranca e operacao

Requisitos relacionados: RNF001, RNF003, RNF004, RNF005, RNF006, RNF007.

- [ ] Criar model/tabela de auditoria.
- [ ] Registrar alteracoes cadastrais importantes.
- [ ] Registrar soft delete.
- [ ] Registrar estorno financeiro.
- [ ] Registrar usuario executor, timestamp e IP.
- [ ] Adicionar middleware/utilitario para capturar IP quando necessario.
- [ ] Definir politica de HTTPS para ambiente produtivo.
- [ ] Avaliar troca de SQLite para PostgreSQL antes de producao.
- [ ] Criar indices para consultas frequentes: aluno por CPF, matricula ativa por aluno, pagamentos pendentes, check-ins recentes.
- [ ] Adicionar logs estruturados.
- [ ] Garantir que erros 500 nao exponham stack trace em producao.
- [ ] Criar health check com status de banco, se necessario.

## Ordem sugerida de implementacao

1. Finalizar base de autenticacao e RBAC.
2. Separar accounts em services/repositories antes do sistema crescer.
3. Fechar alunos e professores com testes.
4. Implementar planos.
5. Implementar matriculas.
6. Implementar pagamentos.
7. Implementar check-in, porque ele depende de matricula e financeiro.
8. Implementar exercicios e treinos.
9. Implementar avaliacoes fisicas.
10. Adicionar auditoria, indices e ajustes de operacao.

## Criterio de pronto por modulo

Um modulo so deve ser marcado como pronto quando:

- [ ] Models e migrations existem.
- [ ] Schemas de entrada e saida existem.
- [ ] Endpoints documentados existem.
- [ ] Regras de negocio do modulo estao no service, nao no router.
- [ ] Erros principais retornam HTTP coerente e mensagem clara.
- [ ] Testes cobrem fluxo feliz e principais bloqueios.
- [ ] O Swagger abre e mostra os contratos corretamente.
- [ ] `poetry run alembic upgrade head` executa sem erro.
- [ ] Suite de testes executa sem erro.

## Decisoes pendentes

- [ ] O MVP tera recuperacao de senha agora ou depois?
- [ ] O refresh token sera apenas recriacao de access token ou tera token separado persistido/rotacionado?
- [ ] Pagamento precisa de `due_date` separado de `payment_date`?
- [ ] Professores terao turnos em string simples, enum, tabela propria ou ficarao fora do MVP?
- [ ] O banco final sera SQLite apenas para estudo local ou PostgreSQL para simular producao?
- [ ] `is_active` podera ser alterado via PATCH ou apenas por endpoints especificos de ativar/inativar?
