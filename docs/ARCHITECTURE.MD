# 🏛️ Arquitetura do Sistema

O AprovaAi foi desenhado utilizando uma arquitetura orientada a serviços (SOA), separando claramente as responsabilidades do cliente (Angular) e do servidor (FastAPI).

## Fluxo de Dados (Análise de Edital)
1. **Frontend:** O usuário faz o upload do PDF. O Angular converte o arquivo para `FormData` e envia via `POST`.
2. **Backend:** O FastAPI recebe o arquivo e aciona o worker assíncrono.
3. **Extração:** A biblioteca `pdfplumber` limpa o texto e remove ruídos.
4. **IA:** O texto é enviado ao Gemini com um prompt rigoroso para retornar um JSON.
5. **Persistência:** O JSON é mapeado pelo SQLAlchemy e salvo no PostgreSQL.