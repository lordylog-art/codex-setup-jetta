---
name: obsidian-feature-blocks
description: "Turn an Obsidian idea into agreed scope and testable feature blocks using Grill With Docs. Materialize blocks only after approval; no tickets or implementation."
---

# Blocos Obsidian

Conduza ideia, investigação, Grill, consenso, proposta, negociação, aprovação e documentação. Termine após documentar; nunca implemente automaticamente um bloco. Busque a menor sequência de entregas funcionais que permite avanço seguro, validação prática e contexto simples em outra conversa.

## 1. Resolver origem e projeto

- Identifique `SOURCE_NOTE` pelo caminho explícito, anexo ou seleção comprovada por ferramenta. Não adivinhe a seleção. Prefira MCP Obsidian; indisponível, use arquivos locais e os vaults configurados em `%APPDATA%/obsidian/obsidian.json`. Um caminho explícito não depende de qual vault está aberto.
- Anexo copiado exige localizar sua nota original; não trate a cópia da conversa como origem gravável. Para referência ausente ou ambígua, peça o identificador necessário e aguarde.
- Resolva `VAULT_ROOT`, `PROJECT_ROOT` e repositório técnico, quando aplicável, por evidências da nota, links, índice/README próximos e configuração. `PROJECT_ROOT` é a raiz do projeto dentro do vault; não é automaticamente o cwd, a raiz do vault ou a pasta Features. Se ambígua, pergunte antes de gravar.
- Leia progressivamente: origem; referências diretas; documentação relevante do projeto; busca pontual por dúvida. Consulte AGENTS aplicáveis, arquitetura, domínio e código pertinente. Não varra o vault nem carregue dezenas de notas por garantia. Distinga fatos, decisões e hipóteses.
- Procure blocos existentes somente nos links da origem e em `PROJECT_ROOT/Blocos`. Em reexecução, leia primeiro a Visão Geral correspondente, compare com a origem e identifique mudanças.

## 2. Reutilizar Grill With Docs

Leia [references/grill-integration.md](references/grill-integration.md). Localize e carregue `grill-with-docs`, depois execute suas capacidades `grilling` e `domain-modeling`. Não substitua por questionário próprio ou `grill-me`. Dependência ausente: informe a lacuna e pare antes de declarar o Grill concluído.

Passe origem, projeto e fatos verificados com o contrato: **workflow de blocos, sem tickets; definição permanece em SOURCE_NOTE; nenhum diretório novo antes da aprovação da divisão**. Preserve métodos do Grill, adaptando seus destinos conforme a referência. Não altere as skills reutilizadas ou regras globais.

Investigue decisões materiais aplicáveis: objetivo, usuários, fluxos principal/alternativos, estados, regras, permissões, erros, persistência/dados, frontend/UX/responsividade, backend/DB/APIs, integrações, compatibilidade/impactos, concorrência/idempotência/sincronização, jobs/cache, segurança/auditoria/observabilidade, mensagens, limites e critérios de pronto. Pergunte somente se a resposta muda arquitetura, comportamento, escopo, UX, implementação, teste ou divisão.

Siga a fronteira de decisões do `grilling`: perguntas desbloqueadas, numeradas, com recomendação; aguarde respostas, recompute consequências e próximas rodadas. Busque fatos no ambiente, delegando reconhecimento read-only quando disponível. Silêncio não é decisão. Quando não houver dúvidas materiais, peça confirmação do entendimento compartilhado antes de propor blocos.

## 3. Consolidar a origem

Durante o Grill, registre decisões já resolvidas na origem, sem esperar a criação dos blocos. Preserve integralmente ideia original em sua posição, frontmatter, aliases, tags, links e texto manual. Acrescente/atualize seções sem mover ou apagar o original para impor um template. Releia antes de gravar e reconcilie alterações concorrentes.

Leia a seção Origem em [references/templates.md](references/templates.md). Documente resultados e razões úteis, sem transcrição extensa ou repetição. Não declare escopo confirmado antes da confirmação. Não crie segunda especificação, CONTEXT/ADR separado ou pasta. Termos/decisões da feature ficam na origem; documentos globais existentes são referências, não alvos de edição.

## 4. Propor, negociar e parar

Após consenso, mostre no chat a divisão completa usando o formato Proposta da referência e emojis temáticos discretos. Não grave novos arquivos.

- Cada bloco é um estágio funcional, preferencialmente vertical, podendo unir banco, backend, frontend, integração e testes. Não separe banco/API/frontend/testes como etapas sem resultado observável.
- Para cada bloco, responda: o que alguém poderá executar, visualizar ou testar ao final? Com UI, indique tela, fluxo, estado, dados e teste manual. Infra sem UI exige teste, comando, endpoint, harness, smoke ou outro mecanismo com ação e resultado verificáveis.
- Use o menor número útil; una blocos que isoladamente nada entregam, divida objetivos independentes grandes. Não force quantidade. Registre dependências reais, ordem sem ciclos, progressão e limite/rollback compreensível.
- Nunca gere Ticket, Task, Subtask, story points, issues ou decomposição técnica excessiva. Não acione `to-tickets`, implementação ou orquestradores de execução.
- **Apresente e pare.** Aguarde feedback sem criar Blocos/, pasta da feature ou notas. Após feedback, reconstrua e mostre a proposta inteira atualizada, não apenas diferenças.
- Materialize somente após aprovação inequívoca da versão atual: “aprovado”, “pode criar”, “faz os blocos”, “é isso”, “essa estrutura ficou boa” ou equivalente contextual. “Faz sentido” isolado, dúvida, aprovação condicional ou mudança solicitada não autorizam criação. Revisão invalida aprovação da versão anterior. O pedido inicial para usar a skill não aprova uma divisão desconhecida.

## 5. Materializar a versão aprovada

Leia os formatos Materialização, Visão Geral e Bloco da referência. Reutilize/crie `PROJECT_ROOT/Blocos/<Nome da Feature>/`, com uma nota geral e uma pasta contendo a nota de cada bloco. Use prefixos numéricos, emojis pertinentes e nomes válidos no Windows. Wikilinks relativos à raiz do vault, sem .md, evitam títulos ambíguos.

Confira colisões sem diferenciar caixa e leia arquivos existentes antes de escrever. Identifique a feature pelo vínculo à origem; ambiguidade exige decisão. Não sobrescreva outra feature, normalize, renumere, mova, apague ou substitua blocos existentes automaticamente. Reexecução exige proposta de impacto e aprovação antes de atualizar somente o necessário, preservando estados/histórico/conteúdo manual. Remoção/migração exige autorização específica.

Notas devem permitir execução futura independente: resultado, regras locais, direção técnica definida, áreas verificadas, dependências e prova objetiva. Use links para contexto compartilhado, sem copiar conversa/projeto/outros blocos. Não invente tabelas, APIs ou caminhos; identifique áreas conceituais como tais. Lacunas materiais voltam ao Grill.

Status: use somente uma interface clara e verificada do mecanismo instalado para iniciar novos blocos como Pendente (`pending` se esse for o identificador real). Não altere plugin/schema/sistema/paleta. Sem integração segura, ignore e informe. Documentação pronta não significa implementação concluída.

## 6. Conferir e encerrar

Confira arquivos salvos, links resolvíveis, correspondência com a última proposta aprovada, origem preservada, ordem/dependências e validação observável por bloco. Corrija defeitos da documentação. Entregue links, quantidade de blocos e próximo bloco recomendado. Diga que implementação exige outra execução informando a nota do bloco. Pare sem editar código, executar migrações, publicar ou iniciar Bloco 01.
