# 🎯 AprovAI - Analisador Estratégico de Concursos

O **AprovAI** é uma plataforma Full-Stack focada em otimizar o estudo para concursos públicos e vestibulares. Utilizando Inteligência Artificial, o sistema lê editais em PDF, mapeia o conteúdo programático e cruza essas informações com provas anteriores para gerar um painel estatístico do que realmente cai nas provas.

## 🚀 Tecnologias Utilizadas

**Frontend:**
* [Angular](https://angular.dev/) (v17+)
* [Tailwind CSS](https://tailwindcss.com/)
* [Chart.js](https://www.chartjs.org/)

**Backend & IA:**
* [Python 3.10+](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/) (Framework Web Assíncrono)
* [Google Gemini API](https://ai.google.dev/) (Motor de IA)
* [PostgreSQL](https://www.postgresql.org/) / SQLite

**Infraestrutura (Cloud):**
* Hospedagem: Microsoft Azure (App Service & Static Web Apps)

## ⚙️ Como rodar o projeto localmente

### 1. Configurando o Backend (Python)
```bash
# Clone o repositório
git clone [https://github.com/seu-usuario/aprovai.git](https://github.com/seu-usuario/aprovai.git)
cd aprovai/backend

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Crie o arquivo de variáveis de ambiente
echo "GEMINI_API_KEY=sua_chave_aqui" > .env

# Rode o servidor
uvicorn main:app --reload
2. Configurando o Frontend (Angular)
Bash
cd ../frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
ng serve
Acesse http://localhost:4200 no navegador.