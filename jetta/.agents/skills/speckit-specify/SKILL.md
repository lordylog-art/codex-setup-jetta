---
name: speckit-specify
description: Cria ou atualiza uma especificação de feature do ERP Jetta.
---

# Spec Kit Specify

Leia `AGENTS.md`, a Constituição e o template ativo. Use a feature apontada em `.specify/feature.json` quando existir; caso contrário, crie um diretório numerado em `specs/` sem trocar branch.

1. Extraia objetivo, usuários/unidade, escopo, exclusões, fluxo, regras, efeitos externos e aceite.
2. Investigue somente os precedentes, contratos e telas citados ou afetados. Para rota/tela/modal/fluxo referido, execute `investigar-detalhes`.
3. Pergunte apenas o que código e precedente não resolvem e que possa mudar escopo, regra, contrato, UX, dados, segurança ou efeito externo (até cinco perguntas).
4. Preencha `spec.md` com cenários, requisitos testáveis, exceções, critérios mensuráveis, dependências e comportamentos preservados. Marque domínios não aplicáveis com motivo curto.
5. Para UI administrativa, registre a referência visual mais próxima e reutilização prevista; só pergunte composição de tela nova quando não houver precedente claro.
6. Faça uma revisão única de completude. Não gere checklist separado, hooks, artefatos ou perguntas adicionais sem necessidade.

A spec está pronta quando não há decisão material pendente. Relate caminho, decisões pendentes e próximo passo.
