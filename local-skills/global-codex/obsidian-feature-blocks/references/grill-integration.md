# Integração com Grill With Docs

## Localizar e executar

Procure no catálogo atual, depois `<repo>/.agents/skills/grill-with-docs/SKILL.md`, `<repo>/.codex/skills/...`, `$CODEX_HOME/skills/...` (ou `~/.codex/skills`) e `~/.agents/skills/...`. Leia candidatos existentes sem busca recursiva no disco/vault.

Nesta instalação a dependência verificada está em `C:/Scripts/ERP JETTA/.agents/skills/grill-with-docs/SKILL.md`. Esse é um fallback de ferramenta instalada, não o projeto da feature. Pode atender qualquer projeto Obsidian sem importar contexto do ERP. Se movida, peça localização; não copie ou recrie o método silenciosamente. A skill é global, mas esta instalação depende desse checkout para o Grill; não é um pacote autônomo.

Contrato existente: “Call the Skill tool twice, for "grilling" and "domain-modeling".” Leia também `../grilling/SKILL.md` e `../domain-modeling/SKILL.md` da instalação escolhida. Com ferramenta de invocação, use-a explicitamente; sem ela, carregue os SKILL.md e siga suas instruções no Codex. Não invente uma chamada Skill indisponível. A política explicit-only da dependência permite esta reutilização deliberada.

`grilling` fornece árvore, rodadas da fronteira, recomendações, pesquisa factual delegada e confirmação de entendimento. `domain-modeling` fornece vocabulário preciso, confronto com código/glossário e registro de decisões justificadas. Carregue seus formatos adicionais somente quando necessários. Não duplique esses métodos.

## Destinos adaptados pelo pedido explícito

O hook atual do Grill usa `spec-workspace`, criando Spec Driven e roteando Context/Decisions/Tickets. O usuário exige origem única, blocos e nenhum diretório antes da aprovação. Passe `SOURCE_NOTE`, raízes e `workflow: obsidian-feature-blocks` às duas capacidades, declarando o contrato antes de qualquer escrita:

- Reutilize os métodos; registre termos em Vocabulário e decisões na origem. Decisão que mereça ADR fica ali com contexto, alternativas, escolha e consequências.
- Não execute o resolver gravável `spec_workspace.py`, write_artifact, update_index ou styling automático. Seus efeitos/layout pertencem ao workflow Spec Driven. Contexto existente pode ser consultado por links, sem conversão.
- Não crie CONTEXT.md/docs/adr no repo. Impacto global de domínio fora da feature é trabalho separado.
- Preserve dependências e demais fluxos. A adaptação é local à invocação, determinada pelo pedido do usuário, sem AGENTS ou hooks novos.

Regras aplicáveis continuam valendo. Exponha um conflito real antes de mutação; não crie tickets como contorno.
