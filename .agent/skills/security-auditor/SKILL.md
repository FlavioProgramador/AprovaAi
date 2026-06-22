# 🛡️ Security Auditor Skill

Security auditing, OWASP Top 10 vulnerabilities mitigation, input sanitization, rate limiting, and CORS configuration.

## 🔒 Regras de Segurança da Aplicação

1. **Mitigação de OWASP Top 10**:
   - **SQL Injection**: Sempre use ORMs (como SQLAlchemy) ou parâmetros preparados. Nunca concatene variáveis em strings SQL brutas.
   - **XSS (Cross-Site Scripting)**: Higienize todas as entradas do usuário no backend e utilize o motor de templates seguro do frontend (Angular já protege nativamente contra inserções inseguras de HTML, mas evite usar `bypassSecurityTrustHtml` a menos que estritamente validado).

2. **CORS e Rate Limiting**:
   - Configure políticas de CORS restritas (permita apenas as origens específicas do frontend em produção).
   - Implemente middlewares de limitação de requisições (`Rate Limiting`) em rotas sensíveis como login e processamento de PDFs para evitar ataques de força bruta ou negação de serviço (DoS).
