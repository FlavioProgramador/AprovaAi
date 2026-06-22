# 🎯 AprovaAi - Inteligência Artificial para Concursos

![Angular](https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)

O **AprovaAi** é uma plataforma Full-Stack orientada por Inteligência Artificial focada em otimizar o estudo para concursos públicos e vestibulares. O sistema lê editais em PDF, mapeia o conteúdo programático e cruza essas informações com provas anteriores, gerando um painel estatístico visual do que tem maior probabilidade de ser cobrado.

---

## ✨ Funcionalidades

* **Extração Inteligente:** Leitura automatizada de editais em PDF para estruturação do conteúdo programático.
* **Classificação de Questões:** Motor de IA que categoriza questões de provas anteriores vinculando-as aos tópicos do edital.
* **Dashboard Analítico:** Gráficos interativos mostrando a relevância percentual de cada disciplina e tópico.
* **Plano de Estudos Direcionado:** Checklist gerado automaticamente priorizando os assuntos que mais caem.
* **Processamento Assíncrono:** Arquitetura não-bloqueante para lidar com PDFs densos sem travar a interface do usuário.

---

## 🚀 Tecnologias Utilizadas

**Frontend:**
* [Angular](https://angular.dev/) (v17+) - Framework principal
* [Tailwind CSS](https://tailwindcss.com/) - Estilização utilitária
* [Chart.js](https://www.chartjs.org/) / Ngx-charts - Renderização de gráficos

**Backend & IA:**
* [Python 3.10+](https://www.python.org/) - Linguagem principal
* [FastAPI](https://fastapi.tiangolo.com/) - Framework web de alta performance
* [Google Gemini API](https://ai.google.dev/) - LLM para processamento de linguagem natural
* [pdfplumber](https://github.com/jsvine/pdfplumber) & [pandas](https://pandas.pydata.org/) - Manipulação de arquivos e dados

**Infraestrutura & Cloud:**
* Banco de Dados: PostgreSQL / SQLite
* Hospedagem: Microsoft Azure (App Service & Static Web Apps)

---

## 📂 Estrutura do Projeto

O repositório é um monorepo contendo tanto o cliente quanto a API:

```text
aprovai/
├── backend/                   # 🐍 API RESTful em Python
│   ├── app/
│   │   ├── core/              # Configurações globais, segurança e banco de dados
│   │   ├── models/            # Entidades do banco de dados (SQLAlchemy)
│   │   ├── schemas/           # Validação de dados (Pydantic)
│   │   ├── services/          # Regras de negócio (Integração Gemini, extração PDF)
│   │   └── routers/           # Endpoints da API (Upload, Dashboard, Status)
│   ├── main.py                # Arquivo de inicialização do FastAPI
│   └── requirements.txt       # Dependências do Python
│
├── frontend/                  # 🅰️ Aplicação Web em Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/          # Serviços, interceptors e guards
│   │   │   ├── components/    # Componentes UI reutilizáveis (Gráficos, Botões)
│   │   │   └── pages/         # Telas principais (Home, Upload, Dashboard)
│   │   └── assets/            # Imagens e arquivos estáticos
│   ├── angular.json           # Configurações do Angular Workspace
│   └── package.json           # Dependências do Node.js
│
├── docs/                      # 📚 Documentação técnica adicional
│   └── PROMPTS.md             # Engenharia de prompts e testes com a IA
├── CONTRIBUTING.md            # Guia para contribuições
└── ROADMAP.md                 # Planejamento e fases de desenvolvimento
🛠️ Pré-requisitos
Antes de começar, certifique-se de ter instalado em sua máquina:

Node.js (v18+)

Angular CLI (npm install -g @angular/cli)

Python (v3.10+)

Git

Você também precisará de uma chave de API gratuita do Google AI Studio para usar o Gemini.

⚙️ Como rodar o projeto localmente
1. Configurando a API (Backend)
Bash
# Clone o repositório
git clone [https://github.com/SeuUsuario/AprovaAi.git](https://github.com/SeuUsuario/AprovaAi.git)
cd AprovaAi/backend

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
echo "GEMINI_API_KEY=sua_chave_aqui" > .env
echo "DATABASE_URL=sqlite:///./test.db" >> .env

# Inicie o servidor
uvicorn main:app --reload
A API estará rodando em http://localhost:8000. Você pode acessar a documentação interativa (Swagger) em http://localhost:8000/docs.

2. Configurando o Cliente (Frontend)
Bash
# Abra um novo terminal e navegue até a pasta do frontend
cd AprovaAi/frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
ng serve
Acesse a aplicação no seu navegador em http://localhost:4200.

☁️ Deploy (Azure)
Este projeto está configurado para ser implantado no ecossistema Microsoft Azure:

Frontend: Implantação contínua via Azure Static Web Apps vinculada ao repositório GitHub.

Backend: Hospedado via Azure App Service (Linux/Python container).

👨‍💻 Autor
Flavio da Costa Marques

Full-Stack Developer

LinkedIn

GitHub

Desenvolvido com dedicação para revolucionar a forma como estudamos. 🚀