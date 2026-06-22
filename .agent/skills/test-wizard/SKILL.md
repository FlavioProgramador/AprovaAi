# 🧪 Test Wizard Skill

Quality assurance guidelines focused on Test-Driven Development (TDD), high code coverage, unit testing, integration testing, and End-to-End (E2E) testing.

## 🧪 Padrão de Testes

1. **Desenvolvimento Orientado a Testes (TDD)**:
   - Escreva o caso de teste antes da implementação do código.
   - Garanta o fluxo: Vermelho (teste falha) -> Verde (código passa no teste) -> Refatoração (melhoria de estilo mantendo o verde).

2. **Isolamento e Mocks**:
   - Testes unitários devem isolar dependências externas (bancos de dados, APIs de terceiros como Gemini) usando dublês de teste (Mocks/Stubs).
   - Use fixtures limpas para preparar o estado de cada caso de teste de forma idempotente.

3. **Estratégia E2E (End-to-End)**:
   - Proponha automação visual de fluxos críticos (login, uploads de arquivos, processamento de formulários) utilizando Playwright ou Cypress no frontend.
