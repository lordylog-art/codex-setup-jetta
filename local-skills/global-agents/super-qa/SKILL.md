---
name: super-qa
description: Execute mandatory change-aware QA in coding chats using project-native runners and remembered strategies, without a persistent Super QA MCP server.
---

# Super QA no chat

Para mudanças de comportamento, execute este protocolo antes de declarar conclusão. QA é responsabilidade do agente no chat; memória guarda estratégias e resultados históricos, e os runners produzem prova atual. Documentação pura exige revisão de conteúdo e links.

1. Leia instruções locais, o delta e consumidores atingidos. Preserve alterações alheias. Reutilize contexto já resolvido; consulte [aprendizado](references/learning.md) uma vez para gaps/regressões pertinentes.
2. Relacione os comportamentos alterados aos testes existentes e à fronteira real. Corrija ou acrescente regressão persistente no runner nativo quando necessário. Para defeitos, prove que o caso detecta a falha. Autorização, persistência, concorrência e integrações exigem provas da fronteira atingida; mocks não demonstram integração real.
3. Escolha o menor conjunto de suítes que cobre o pedido. Execute uma vez por candidato válido e leia resultado, contagens, falhas/skips e relatórios. Repita somente após falha, mudança invalidante ou nova evidência. Agregado completo somente por pedido, marco previsto ou risco compartilhado concreto.
4. Mantenha testes novos alcançáveis pelo agregado existente. Registre resultado, evidência e limites no ticket/nota existente quando houver. Não crie relatório/ticket por rotina. Confirme gravação de aprendizado antes de alegar salvamento.

## Execução sob demanda

Use os comandos revisados do próprio projeto. Se existir `tools/super-qa/cli.mjs`, ele conserva o registro `.super-qa.json` e os relatórios `.super-qa/<runId>/result.json` sem servidor persistente:

```powershell
node tools/super-qa/cli.mjs run --project <checkout-absoluto> --suites <ids-revisados>
```

Leia o `result.json` do run retornado; execução CLI aguarda conclusão, sem polling MCP. Para lacunas/seleção incerta, use `inventory`, `analyze` ou `check` no mesmo CLI. Delta pequeno com suíte conhecida dispensa inventário/plano separado. Outros projetos usam seus runners nativos; não copie um agregador apenas para cumprir o protocolo. O CLI genérico preservado em `C:/Users/caila/.codex/local-marketplaces/super-qa/plugins/super-qa/cli.mjs` é opcional para projetos que já adotam seu registro, nunca um servidor a iniciar.

Consulte somente as frentes pertinentes: [personas](../qa-personas/SKILL.md), [API/dados](../qa-api-data/SKILL.md), [UI](../qa-ui/SKILL.md), [suítes](../qa-suite/SKILL.md), [resiliência](../qa-resilience/SKILL.md).

Declare PASS, FAIL ou BLOCKED apenas no escopo comprovado. Falta de fixture/relatório, skip ou suíte não executada deixa a fronteira sem prova; contagem verde não demonstra completude semântica, aceite visual ou prontidão de produção. Preserve configurações, sessões, agendas e autorizações de CI, custo, envios e deploy. Revise efeitos dos comandos antes de executar. Esta obrigação é instrução para o agente durante o trabalho, não automação ausente nem bloqueio técnico de encerramento do chat.
