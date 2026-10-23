---
name: tdd
description: Escolher provas de comportamento e executar RED/GREEN, distinguindo simulação do mecanismo real.
---

# TDD — qualidade e força da prova

Esta skill define prova e ciclo RED/GREEN. [Implement](../implement/SKILL.md) define ordem, gates e fechamento. Use interfaces do contrato aprovado; consulte CONTEXT/ADRs da área quando necessários. Fronteiras já explícitas no pedido/ticket não exigem nova aprovação; pergunte apenas se a escolha alterar materialmente escopo, contrato ou autorização.

## Prova discriminante

Qual é o menor exemplo que conseguiria mostrar que a implementação está errada? Use saída/efeito observável e resultado esperado independente, derivado do contrato. O mecanismo que pode invalidar a mudança precisa existir na prova.

Para a regra de alto risco da fatia atual, derive as classes de resultado antes de corrigir: sucesso confirmado, rejeição confirmada e resultado inconclusivo, quando previstos pelo contrato. Nas fronteiras de provedores, exercite campos obrigatórios ausentes, vazios ou malformados e confirmação válida; HTTP 2xx ou `ok: true` só confirmam o que o contrato do provedor garante. Reuse casos equivalentes e teste variantes que alterem a decisão, sem combinações exaustivas. Leve essa cobertura ao primeiro review da fatia, evitando descobrir a mesma regra uma variante por rodada.

| Mecanismo sob risco | Prova pertinente |
|---|---|
| Regra pura, precisão, trim | Teste focal com valores-limite e oráculo independente. |
| Corrida/estado | Ordem temporal controlada, incluindo invariantes relacionadas como revogação. |
| Ação nativa de formulário/history | Browser real observando navegação/requisições/efeitos. jsdom não cobre essa fronteira. |
| ORM/migration | Cliente real e banco sintético; bootstrap vazio quando a ordem de migrations estiver em risco. |
| SMTP/transporte | Boundary sintético integrado que reproduza a fase/falha; adapter não prova transporte. |
| Layout | Renderização com dados/estados que pressionem os elementos afetados; medir documento não prova tabela. |

Use mocks úteis para feedback barato. Leia [mocking.md](mocking.md) ou [tests.md](tests.md) quando precisar de exemplos, sem substituir o mecanismo que está sendo testado. Dados extremos devem participar da assertion/captura, não apenas existir numa fixture filtrada para fora.

## Força e resultado são dimensões diferentes

No registro existente, descreva superfície, substituições e limite. Rótulos curtos ajudam:

- **DOCUMENTAL:** declaração/configuração inspecionada; não comprova execução. `TDD-RED:` é um registro textual, mesmo quando o gate aceita o marcador.
- **FOCUSED:** execução de comportamento delimitado pela interface. Se houver simulação relevante, marque **SIMULATED** e diga qual; passar não cobre a fronteira substituída.
- **INTEGRATED:** componentes reais conectados nas fronteiras listadas; declarar isolamento e provedores sintéticos. Não implica entrega externa.
- **VISUAL:** estado renderizado e inspecionado no viewport/dados informados; não implica funcionamento de backend.

Resultado separado: passou, falhou, bloqueado, não executado ou N/A justificado. Readiness estática só prova arquivos/módulos disponíveis; não deve virar INTEGRATED. Um resultado pode combinar superfícies, explicitando limites.

## RED → GREEN por fatia

1. Execute a prova antes da correção e observe falha do comportamento, não de sintaxe/ambiente. Registre comando, falha e conteúdo relevante no registro já existente. Marcador não substitui o RED executado.
2. Implemente o mínimo que satisfaça a regra e as invariantes relacionadas; execute a mesma prova. Só amplie após a primeira fatia demonstrada.
3. Em correção, teste também o estado/consumidor alcançado pela condição alterada. Novos casos entram pelo risco, não pela contagem de testes.

Não escreva todos os testes de uma solução imaginada antes de exercer a primeira fatia. Preserve assertions/skips. Refatoração fora do necessário pertence a decisão separada, não ao ciclo automático.

Evite teste que reimplementa o algoritmo, afirma constante contra si mesma ou observa filename/handler quando o contrato exige efeito. Banco/fila sanitizados podem complementar a interface para provar persistência, isolamento e ausência de efeitos quando exigidos. Teste falhando por ambiente é bloqueio da prova, não RED válido do produto.
