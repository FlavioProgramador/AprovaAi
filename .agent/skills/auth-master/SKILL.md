# 🔐 Auth Master Skill

Secure authentication, authorization, token lifecycle management, and access control guidelines (JWT, OAuth2, RBAC).

## 🔒 Protocolo de Segurança e Acesso

1. **Autenticação Segura (JWT/OAuth2)**:
   - Tokens JWT devem ter tempo de expiração curto (ex: 15-30 minutos) e utilizar algoritmos robustos de assinatura (RS256 ou HS256 com chave forte).
   - Implemente fluxos de Refresh Token armazenados em Cookies HttpOnly com flag `Secure` e `SameSite=Strict` para evitar ataques XSS e CSRF.

2. **Criptografia de Senhas**:
   - Nunca guarde senhas em texto puro. Utilize algoritmos de hashing adaptativos e lentos como **bcrypt** ou **Argon2** com salting individual automático.

3. **Autorização Rígida (RBAC/ABAC)**:
   - Toda rota privada deve validar não apenas se o usuário está autenticado, mas se possui a permissão/role necessária (Role-Based Access Control) antes de processar dados.
