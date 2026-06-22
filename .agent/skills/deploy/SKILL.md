# 🚢 Deploy Skill

Best practices and automation workflows for deploying projects to cloud ecosystems, specifically Microsoft Azure, Docker, and GitHub Actions CI/CD pipelines.

## 📦 Protocolo de Deploy

1. **Testes e Build de Validação**:
   - Antes de iniciar qualquer deploy, certifique-se de executar os testes locais e gerar o build de produção (`ng build --configuration=production` ou build do Python).
   - Resolva todos os alertas do linter para evitar quebras em produção.

2. **Segurança de Variáveis**:
   - Nunca versione chaves de API, segredos ou URLs de produção locais.
   - Configure secrets no GitHub (`GitHub Secrets`) e as referencie no pipeline de CI/CD.
   - Use injeção de ambiente dinâmica do Azure App Service/Static Web Apps.

3. **Verificação de Saúde**:
   - Configure endpoints de health check (ex: `/api/v1/health`) e use monitoramento de uptime para validar o deploy pós-atualização.
