import os
import json
import logging
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL_NAME
        
        # Configure the SDK if a valid-looking key is provided
        if self.api_key and self.api_key != "mock_api_key" and self.api_key != "sua_chave_aqui":
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                self.is_configured = True
                logger.info("Google Gemini SDK configurado com sucesso.")
            except Exception as e:
                logger.error(f"Erro ao configurar Google Gemini SDK: {str(e)}")
                self.is_configured = False
        else:
            self.is_configured = False
            logger.warning("Google Gemini SDK NÃO configurado. Usando respostas mockadas para simulação.")

    def analyze_syllabus(self, syllabus_text: str) -> dict:
        """
        Envia o texto extraído do edital para o Gemini e retorna a análise estruturada.
        Caso o SDK não esteja ativo ou ocorra um erro, retorna dados simulados (mock).
        """
        if not self.is_configured:
            return self._get_mock_analysis(syllabus_text)

        prompt = f"""
        Você é um especialista em concursos públicos e vestibulares.
        Analise o seguinte conteúdo programático extraído de um edital e identifique os principais tópicos.
        Para cada tópico, estime a relevância histórica dele em provas (em porcentagem de relevância de 0 a 100%),
        o peso sugerido (Alto, Médio, Baixo) e forneça uma breve recomendação de foco de estudo.
        Retorne a resposta estritamente no formato JSON abaixo, sem blocos de código markdown ou texto explicativo extra:
        {{
            "metadata": {{
                "extracted_topics_count": 5
            }},
            "topics": [
                {{
                    "name": "Nome do Tópico",
                    "weight": "Alto|Médio|Baixo",
                    "relevance_percentage": 85.5,
                    "study_recommendation": "Focar em resoluções de questões..."
                }}
            ],
            "general_strategy": "Visão geral estratégica de como abordar esta disciplina..."
        }}

        CONTEÚDO PROGRAMÁTICO:
        {syllabus_text[:8000]}  # Limita o tamanho para evitar estourar limites de tokens na versão inicial
        """

        try:
            response = self.model.generate_content(prompt)
            # Tentar fazer o parse do JSON da resposta
            text = response.text.strip()
            # Limpar formatações comuns do Markdown se a IA enviar
            if text.startswith("```json"):
                text = text.split("```json")[1].split("```")[0].strip()
            elif text.startswith("```"):
                text = text.split("```")[1].split("```")[0].strip()
                
            return json.loads(text)
        except Exception as e:
            logger.error(f"Erro durante chamada à API do Gemini: {str(e)}")
            return self._get_mock_analysis(syllabus_text, error_occurred=True)

    def _get_mock_analysis(self, syllabus_text: str, error_occurred: bool = False) -> dict:
        """
        Retorna dados simulados estruturados para fins de desenvolvimento.
        """
        status_msg = "Simulado (Chave de API não configurada)" if not error_occurred else "Simulado (Erro na API do Gemini)"
        
        # Mapeamento estático apenas para gerar algo dinâmico baseado no tamanho do texto
        len_text = len(syllabus_text) if syllabus_text else 100
        
        return {
            "metadata": {
                "extracted_topics_count": 4,
                "status": status_msg
            },
            "topics": [
                {
                    "name": "Língua Portuguesa (Compreensão e Interpretação de Texto)",
                    "weight": "Alto",
                    "relevance_percentage": 92.0,
                    "study_recommendation": "Tópico com maior índice de recorrência. Resolva no mínimo 50 questões de exames anteriores para fixar as pegadinhas de interpretação."
                },
                {
                    "name": "Direito Administrativo (Atos Administrativos e Licitações)",
                    "weight": "Alto",
                    "relevance_percentage": 85.0,
                    "study_recommendation": "Estude detalhadamente os requisitos de validade e as hipóteses de dispensa e inexigibilidade da nova lei de licitações."
                },
                {
                    "name": "Informática (Segurança da Informação e Nuvem)",
                    "weight": "Médio",
                    "relevance_percentage": 68.5,
                    "study_recommendation": "Concentre-se nos tipos de malwares e nos conceitos de criptografia simétrica/assimétrica."
                },
                {
                    "name": "Raciocínio Lógico (Lógica de Proposições)",
                    "weight": "Baixo",
                    "relevance_percentage": 45.0,
                    "study_recommendation": "Domine as tabelas-verdade dos conectivos 'e', 'ou' e 'se... então'. Questões costumam ser literais."
                }
            ],
            "general_strategy": f"Com base no edital analisado (tamanho aproximado: {len_text} caracteres), foque 60% do seu tempo de estudo nas disciplinas de peso Alto. Utilize finais de semana para simulados focados em Língua Portuguesa e Direito Administrativo."
        }

gemini_service = GeminiService()
