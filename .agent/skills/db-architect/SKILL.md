# 🗄️ DB Architect Skill

Database modeling, migrations management, index optimization, query tuning, and transactional integrity guidelines.

## 💾 Diretrizes de Banco de Dados

1. **Modelagem Relacional e Normalização**:
   - Desenhe tabelas focadas na consistência de dados (3ª Forma Normal como padrão). Use chaves primárias UUID para tabelas distribuídas ou BigInteger auto-incremento para tabelas puramente relacionais locais.
   - Configure restrições de integridade referencial (`FOREIGN KEY`) com comportamentos explícitos (`ON DELETE CASCADE` ou `RESTRICT`).

2. **Gerenciamento de Migrações**:
   - Nunca altere o banco de dados de produção diretamente. Toda mudança estrutural deve ser feita por arquivos de migração versionados (Alembic no Python, Flyway/Liquibase ou migrations nativas).

3. **Performance de Consultas**:
   - Analise queries lentas (`EXPLAIN ANALYZE`).
   - Crie índices estratégicos em colunas de busca frequente (`WHERE`) e chaves estrangeiras de junção (`JOIN`), evitando índices em excesso que prejudicam inserções.
