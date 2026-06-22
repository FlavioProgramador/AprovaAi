```markdown
# 🚀 Roadmap: AprovAI

## Fase 1: Setup do Ambiente & Modelagem
- [ ] Inicializar backend em FastAPI e configurar ambiente virtual.
- [ ] Inicializar frontend em Angular com TailwindCSS.
- [ ] Modelar banco de dados (Tabelas: Edital, Matérias, Questões).

## Fase 2: O Motor de IA (Python)
- [ ] Implementar extração de texto de PDF (`pdfplumber`).
- [ ] Integrar API do Gemini para estruturar editais em JSON.
- [ ] Criar loop de classificação para envio de questões para a IA.
- [ ] Usar `pandas` para compilar frequências e estatísticas.

## Fase 3: Construção da API REST
- [ ] Endpoint `POST /api/upload`: Recebe PDFs (Edital/Provas).
- [ ] Endpoint `GET /api/status/{id}`: Monitora progresso do processamento.
- [ ] Endpoint `GET /api/dashboard/{id}`: Retorna dados estruturados.

## Fase 4: Interface Reativa (Angular)
- [ ] Componente Drag & Drop para upload.
- [ ] Tela de loading animada com polling RxJS.
- [ ] Dashboard com integração Chart.js para gráficos estatísticos.

## Fase 5: Nuvem (Microsoft Azure)
- [ ] Fazer deploy do Frontend no Azure Static Web Apps.
- [ ] Fazer deploy do Backend no Azure App Service.
- [ ] Configurar Azure Database for PostgreSQL.