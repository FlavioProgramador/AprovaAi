# Regras de IA para o Projeto AprovaAi

1. **Stack Tecnológica:** Use Angular (v17+) no frontend com TypeScript rigoroso e FastAPI no backend (Python 3.10+).
2. **Estilização:** Use exclusivamente Tailwind CSS. Não crie arquivos `.css` ou `.scss` separados a menos que seja estritamente necessário para animações complexas.
3. **Comunicação:** O backend deve ser totalmente assíncrono (`async def`). Respostas de processamento de PDF devem retornar um ID de job, e não bloquear a requisição.
4. **Idioma:** Variáveis, funções e comentários de código devem ser escritos em português claro.
5. **Tipagem:** Sempre adicione tipagem estática no Python (`def func(a: int) -> str:`) e interfaces no TypeScript.