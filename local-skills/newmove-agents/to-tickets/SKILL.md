---
name: to-tickets
description: Criar tickets diretos com entregas completas, dependências técnicas reais e aceite proporcional.
disable-model-invocation: true
---

# To Tickets

Transforme o pedido em trabalho implementável. Use o menor número de tickets que entregue o comportamento solicitado; uma entrega coesa pode ser um único ticket. Separe por resultado utilizável ou fronteira de trabalho, sem criar tickets por camada, teste, relatório ou tamanho de contexto.

## Preparar e criar

1. Leia o pedido atual, decisões pertinentes e tickets existentes. Inspecione apenas o código necessário para localizar a implementação e suas dependências. Reutilize a base pronta; registre somente o delta restante.
2. Aplique o [contrato proporcional](C:/Users/caila/.agents/skills/smart-orchestrator/references/planning-contract.md). Todo critério deve corresponder ao pedido, a uma regra aplicável do projeto ou a um risco concreto introduzido pelo delta. Cite essa origem de forma compacta. Prefira poucos critérios observáveis; normalmente 2–5 bastam, sem omitir requisitos explícitos.
3. Crie diretamente os tickets locais quando o usuário pedir tickets. Pergunte apenas se uma ambiguidade muda o resultado, os dados ou a autorização. Uma fila já aprovada não precisa de outra rodada de quiz. Planejar não autoriza implementar produto nem publicar externamente.
4. Use o tracker/caminho existente. Sem tracker configurado, salve um arquivo por ticket em `.scratch/<feature>/issues/<NN>-<slug>.md`. Publicação ou alteração de issues externos exige autorização específica; sem ela, entregue os arquivos prontos.

## Dependências e aceite

- Declare o insumo técnico que falta e a etapa afetada: implementação, integração ou ativação. Issue OPEN, ausência de parecer ou falta de registro no controller não demonstram, sozinhos, ausência de código/contrato utilizável.
- Trabalho independente avança contra o contrato existente. Integração pendente não impede implementar a tela; funcionalidade ainda sem autorização efetiva permanece indisponível até sua integração segura. Sobreposição de escrita exige coordenação, sem sobrescrever trabalho alheio.
- Critérios descrevem comportamento do usuário. Comandos de teste e provas ficam numa breve seção de verificação, sem virar entregas adicionais.
- Escolha a menor prova que exercite o mecanismo alterado. Layout/composição pede checagem da tela/componente afetado; persistência pede salvar e reler; autorização pede permitir/negar no servidor; migração pede preservação e repetição segura quando aplicável. Não acrescente CAS, rollback, auditoria, matriz de viewports ou todas as integrações do sistema sem requisito ou risco demonstrado.
- Reuse provas ainda válidas. Consolide a revisão conforme o risco e a integração pertinente; após correção, confira o delta e seus impactos. Pare quando o pedido estiver implementado, verificado e sem defeitos materiais pendentes.
- Plano V2/controller, inventário VAL por arquivo e múltiplos relatórios não são entregáveis padrão. Use o modo V2 somente se explicitamente solicitado. Em fila existente, preserve histórico e provas; reconcilie exigências de processo com a instrução atual, sem apagar requisitos de produto nem transformar falta de metadados em defeito.

## Modelo

```markdown
# <NN>: <resultado>

**Entregar:** <comportamento solicitado e delta sobre a base existente>.
**Escopo:** <limites relevantes; preservar consumidores existentes>.
**Dependências:** <insumo e etapa bloqueada, ou nenhuma>.

**Concluído quando:**
- [ ] <resultado observável ligado ao pedido>.
- [ ] <invariante do projeto ou risco concreto, se aplicável>.

**Verificação:** <teste/interação focal e resultado esperado; reutilizar provas válidas>.
**Referências:** <pedido/spec/decisão, sem copiar protocolos inteiros>.
```

Use o [Spec Workspace Adapter](../spec-workspace/SKILL.md) somente com referência explícita ou herdada ao Obsidian. Nesse caso, preserve `Tickets/`, metadados e vínculos canônicos e atualize o Index; não duplique no tracker externo. Nos demais casos, conserve o tracker existente. Não altere a issue pai automaticamente.
