```markdown
# 🤝 Guia de Contribuição

Obrigado por se interessar em contribuir para o **AprovAI**! Este documento descreve o padrão que utilizamos para manter o projeto organizado.

## 🌿 Padrão de Branches

Sempre crie uma branch a partir da `main` para trabalhar na sua funcionalidade ou correção. Use o formato: `tipo/descricao-curta`.

* `feat/` -> Para novas funcionalidades (ex: `feat/upload-pdf`)
* `fix/` -> Para correção de bugs (ex: `fix/erro-grafico-pizza`)
* `docs/` -> Para atualizações na documentação (ex: `docs/atualiza-readme`)
* `refactor/` -> Para refatoração de código (ex: `refactor/servico-api`)

## 💬 Padrão de Commits (Conventional Commits)

Nossos commits seguem a convenção para facilitar a leitura do histórico.
Estrutura: `tipo(escopo opcional): descrição curta em português`

**Exemplos:**
* `feat(auth): adiciona login com JWT`
* `fix(pdf): resolve travamento na leitura de arquivos maiores de 5MB`
* `docs: adiciona o arquivo contributing.md`

## 🚀 Fluxo de Pull Request (PR)

1. Faça o Fork do repositório.
2. Crie sua branch (`git checkout -b feat/minha-feature`).
3. Faça os commits (`git commit -m 'feat: adiciona nova funcionalidade'`).
4. Envie para sua branch (`git push origin feat/minha-feature`).
5. Abra um Pull Request explicando o que foi feito.