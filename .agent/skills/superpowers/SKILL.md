# ⚡ Superpowers Skill

Opinionated software engineering methodology and framework that transforms the agent from vibe coding to strict engineering discipline.

## 🚀 Como Funciona (Fluxo de Execução)

Ao ativar esta skill, você deve seguir o seguinte protocolo estrito de desenvolvimento:

1. **Fase de Planejamento e Especificações**:
   - Antes de escrever qualquer linha de código, pesquise a tarefa e crie um plano detalhado em `implementation_plan.md`.
   - Inclua perguntas abertas e riscos de arquitetura.
   - Obtenha aprovação do usuário antes de iniciar qualquer execução.

2. **Micro-tasking (Checklist)**:
   - Após a aprovação do plano, inicialize e gerencie o progresso das tarefas no arquivo `task.md`.
   - Divida os grandes problemas em tarefas de tamanho de componente e marque cada passo como pendente `[ ]`, em progresso `[/]` ou concluído `[x]`.

3. **Desenvolvimento Orientado a Testes (TDD)**:
   - Crie testes automatizados ou valide o comportamento de cada unidade lógica assim que terminar de criá-la.
   - Não acumule código sem validação intermediária.

4. **Verificação Final**:
   - Faça build de produção, execute linters e teste todas as integrações.
   - Gere um relatório em `walkthrough.md` documentando o sucesso dos testes.
