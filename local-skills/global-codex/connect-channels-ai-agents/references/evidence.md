# Evidências e limites — 13/10/2026

Pasta técnica: `C:/Users/caila/Documents/Codex/connect-channels-ai-agents`.

## Pesquisa antes do REA

[public-research.md](C:/Users/caila/Documents/Codex/connect-channels-ai-agents/public-research.md) reúne fontes primárias e divergências. Guias: [Novo agente](https://docs.flw.chat/guide/documentacao/apps/agentes-inteligentes/novo-agente), [Configurações](https://docs.flw.chat/guide/documentacao/apps/agentes-inteligentes/aba-configuracoes), [Habilidades](https://docs.flw.chat/guide/documentacao/apps/agentes-inteligentes/habilidades), [Supervisor Connect](https://connect-channels.gitbook.io/connect-channels-docs/documentacao/apps/agentes-de-ia/supervisor-de-ia), [V0.8](https://docs.flw.chat/guide/documentacao/apps/agentes-inteligentes/versoes-dos-agentes/v.08). As fontes não publicam o DTO privado completo de IA.

## Artefatos atuais e REA

Index atual do app usa main.c1b6a1d22d66025d.js/runtime.dbf40c80464d29c2.js. Os arquivos da investigação antiga de chatbot têm outro main: por isso foram adquiridos bundles atuais diretamente do host público do app. Não executamos JavaScript do fornecedor para recuperar contratos.

`acquisition-manifest.json` registra URLs/hashes dos chunks adquiridos. `module-index.json` registra offsets de módulos originais; `methods.json` inclui métodos completos e offsets. `excerpts/main-3094.js` contém enums IA, e `excerpts/main-85125.js` contém tipos/status knowledge.

REA análise parent **ev_57f03e8d8a5049807c1a655f25af47af129935b3322b7edf658328f0833f04d4**; summary **ev_10605f723c1d9c7b58756f66cb901630ef03921722c10f262c4c973b77c48451**, preservado em rea-summary.json. Foram parsed15 arquivos/353514 nós AST/239 findings, sem parse failures. Parte do grafo semântico de3 módulos foi limitada pelo budget; fatos estáticos foram retidos. Coverage global é **partial**, não “todas relações resolvidas”.

Item do módulo API14824: **ev_2548a4ceacf7bfdc88f481c662fcd81fc8f9fbecd455d617c7cf696d5d2bcbeb**, preservado em rea-api-module.json, cobertura completa somente dentro daquela vista. Wrappers locais dos módulos são extrações inertes rastreadas, não aplicação executável reconstruída.

## Leitura real autenticada

`live-read-shapes.json` registra respostas sanitizadas e shapes:

- GET aiagent:18 agentes/supervisores.
- GET aicredential:1 credencial, valores secretos omitidos.
- GET aicompany:1 contexto de empresa.
- GET aiKnowledge com active=true:14 bases ativas. O catálogo do helper sem filtroactive devolveu22 bases; esse total inclui o inventário mais amplo, não é crescimento comprovado de8 bases.
- GET aipermissionconfig/current:allowedAdmins.

Conta/base foram acessadas via cliente HTTP da skill de chatbot e sessão DPAPI existente, sem browser e sem OTP novo. Snapshot é temporal. Atualizações de tokens só ocorrem conforme cliente compartilhado; login/refresh não foram reprojetados. Nenhum POST/PUT/DELETE de produto foi executado nesta investigação.

## Reúso e validação

Autenticação e transporte são importados da skill de chatbots. Contratos da fábrica `tools/connect-agent-factory` foram reaproveitados como fonte parcial e upload com executor injetável; testes “integration” dessa fábrica alimentam resultados simulados e não provam fornecedor. Restrições TESTE|/modelo único/no-secrets da fábrica não se tornaram regras globais nesta skill.

scripts/agents.test.mjs teve19/19 testes locais aprovados com mocks e invariantes. Os quatro achados da primeira revisão (stderr sensível, marcador mascarado em array, paginação contraditória e campos obrigatórios) foram corrigidos e receberam regressões. Catálogos do helper foram executados também em HTTP real:18 agentes/supervisores,1 empresa,1 credencial mascarada,22 bases no inventário sem filtroactive. delivery-proof/local-validation/revisão independente na pasta técnica registram resultado final do candidato, com hashes. Skill validator passou; confere embalagem/frontmatter, não conversa real.

## Superfícies não executadas

Criação/edição/readback de novo agente, mutação de credencial/empresa, supervisor novo, upload/processamento/table/FAQ write, archive/reactivation/privacy, generate-summary, sandbox, ask, optimizer, tool actions, MCP efetivo, follow-up e conversa em canal. Não existe prova de integração final desses mecanismos. A skill recupera contratos e fornece cliente; uso externo futuro exige autorização do pedido e validação apropriada.
