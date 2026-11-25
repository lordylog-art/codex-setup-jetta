# Capacidades reutilizadas

Leia o corpo real antes de usar cada capacidade; não copie sua implementação para esta skill. Sem ferramenta Skill, carregar e seguir `SKILL.md` é a adaptação local permitida; não invente chamadas.

Procure primeiro o catálogo atual e a skill local de mesmo nome; depois `$CODEX_HOME/skills` (ou `~/.codex/skills`) e `~/.agents/skills`. Nesta instalação, os caminhos verificados são:

| Etapa | Capacidade | Caminho verificado |
| --- | --- | --- |
| Perguntas e vocabulário | grill-with-docs | C:/Users/caila/.agents/skills/grill-with-docs/SKILL.md |
| Árvore de decisões | grilling | C:/Users/caila/.agents/skills/grilling/SKILL.md |
| Linguagem e decisões | domain-modeling | C:/Users/caila/.agents/skills/domain-modeling/SKILL.md |
| Spec selecionada | to-spec | C:/Users/caila/.agents/skills/to-spec/SKILL.md |
| Blocos selecionados | obsidian-feature-blocks | C:/Users/caila/.codex/skills/obsidian-feature-blocks/SKILL.md |
| Tickets selecionados | to-tickets | C:/Users/caila/.agents/skills/to-tickets/SKILL.md |

Esses caminhos são dependências instaladas, não projetos que devem fornecer requisitos. A ausência do catálogo não prova ausência no disco. Se o caminho mudar, resolva a instalação; não importe contexto de outro repositório.

## Contrato de invocação

Passe origem, projeto técnico, decisões confirmadas, versão aprovada, seleção de entregas, destinos e limites da etapa. Carregue referências exigidas pela capacidade apenas quando pertinentes. Registre antecipadamente que o usuário escolheu esta coordenação: perguntas via grill; documentos finais somente após aprovação; revisão Goldfish em etapas próprias. Isso adapta a invocação, não altera a skill original.

No grill, vocabulário e decisões ficam na origem autorizada ou no registro em chat; não crie ADR/CONTEXT global para documentar a feature. No modo blocos, siga a adaptação de destinos descrita em `obsidian-feature-blocks/references/grill-integration.md`; o fluxo não executa automaticamente os escritores Spec Workspace.

`obsidian-feature-blocks` só cria blocos. Sua etapa termina antes de `to-tickets` começar. `to-spec` só é chamada quando uma spec foi escolhida; sua confirmação de fronteiras de teste continua válida. Não use a spec para criar tickets implicitamente.

Reutilize confirmação explícita de fronteiras de teste já registrada para a mesma versão/escopo; não repita o gate só por trocar de capacidade. Aprovar uma estrutura ou selecionar “spec” não confirma implicitamente fronteiras ainda não discutidas. Mudança material de fronteira pede confirmação do delta.

## Destinos

Resolva origem/vault/projeto por caminhos e evidência, nunca pela seleção presumida. Pedido claro de Obsidian usa adaptadores originais e respeita seus formatos. Ambiguidade de origem bloqueia a escrita dependente, não a investigação técnica. Não procure em todo o vault quando referências diretas bastam.

Antes da aprovação, não crie pasta de feature, `Blocos/`, `Specdriven/`, tickets ou issues. Rascunhos de trabalho necessários para Goldfish usam o diretório EGM do projeto atual ou, sem configuração, sua pasta de trabalho, conforme a integração Codex incluída; ficam claramente não aprovados e fora da instalação global. Destino definitivo muda somente com decisão do usuário. Sem referência clara, proponha o destino antes de escrever; não dispare o fallback externo de `to-spec`.

Para reexecução, leia o que existe, reconheça a mesma feature por origem/links e proponha o delta. Preserve status, histórico, texto manual, links e identificadores; não renumere, remova ou publique por associação.
