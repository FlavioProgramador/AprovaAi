# 🧠 Engenharia de Prompts (AI Models)

Este documento centraliza todos os prompts passados para a API do Google Gemini. Manter o versionamento é essencial para testes A/B e melhoria contínua da IA.

## ⚙️ Configurações Globais do Modelo
* **Modelo:** `gemini-1.5-pro` (ou `gemini-1.5-flash` para performance).
* **Temperatura:** `0.1` (Respostas lógicas e determinísticas).

---

## 📄 Prompt 1: Extração do Edital

**Objetivo:** Ler o texto bruto do PDF e extrair a árvore de conhecimentos.

**Prompt V1.0:**
```text
Você é um analista especialista em concursos públicos brasileiros. 
Abaixo, fornecerei o texto extraído de um edital.
Sua tarefa é encontrar a seção de "Conteúdo Programático" ou "Conhecimentos Exigidos" e extrair as matérias e seus tópicos.

REGRAS:
1. Ignore regras do concurso, salários, ou isenções.
2. Retorne a resposta ESTRITAMENTE em formato JSON.
3. Não inclua blocos de código ou texto extra na resposta.

FORMATO ESPERADO:
{
  "materias": [
    {
      "nome": "Língua Portuguesa",
      "topicos": ["Compreensão de texto", "Ortografia", "Sintaxe"]
    }
  ]
}

TEXTO DO EDITAL:
{{TEXTO_EXTRAIDO_DO_PDF}}