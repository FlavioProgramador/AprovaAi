# ⚙️ Backend Expert Skill

Advanced backend engineering guidelines focusing on clean architecture, API standards, performance, asynchronous jobs, and clean code principles.

## 📐 Diretrizes do Backend

1. **Clean Architecture e Desacoplamento**:
   - Mantenha a separação rígida de responsabilidades: Rotas (API), DTOs (Validação/Schemas), Regras de Negócio (Serviços) e Persistência (Modelos/Repositórios).
   - Inicie a injeção de dependências para gerenciar sessões de banco de dados e serviços externos.

2. **Padrões de API (RESTful)**:
   - Siga as convenções de métodos HTTP (GET para leitura, POST para criação, PUT para atualização total, PATCH para parcial, DELETE para remoção).
   - Utilize códigos de status HTTP corretos (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity, 500 Internal Error).
   - Forneça respostas de erro estruturadas e legíveis.

3. **Performance e Concorrência**:
   - Dê preferência a operações assíncronas (`async/await`) em tarefas de I/O (chamadas de banco, rede, leitura de disco).
   - Proponha estratégias de cache (Redis/Memory Cache) para consultas lentas ou de alta frequência.
