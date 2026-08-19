---
name: listar-possibilidades
description: Listar cenários possíveis de uso, estados esperados, lacunas e riscos em formato de tabela anti-burro. Use quando o usuário pedir possibilidades, cenários, casos de uso, comportamento esperado, matriz de situações, "o que pode acontecer", "anti-burro", "o que já foi implementado e o que não foi", especialmente a partir do contexto ativo, print, issue, feature, bug, fluxo operacional, tela, integração, SAC, Greenmile, programação, sync, backend/frontend ou uma descrição passada pelo usuário.
---

# Listar Possibilidades

## Objetivo

Transformar o contexto ativo ou o texto passado pelo usuário em uma tabela prática de cenários de uso, com foco em comportamento esperado, proteção contra erro humano, lacunas de implementação e próximos ajustes.

Use esta skill para pensar como usuário operacional: o que ele faz, o que espera ver, onde pode se confundir, onde o sistema pode manter dado velho, não atualizar, duplicar informação, esconder erro ou depender de ação manual.

## Entrada

Use, nesta ordem:

1. Contexto explícito que o usuário passou na mensagem.
2. Contexto recente da conversa.
3. Prints/imagens anexadas.
4. Issues, commits, arquivos ou diffs já citados na conversa.
5. Código local somente quando necessário para diferenciar "implementado" de "não implementado".

Se o contexto for insuficiente, entregue a tabela com marcação `Não sei / precisa validar` em vez de inventar.

## Workflow

1. Identifique o fluxo principal e a entidade central.
   - Ex.: motorista Greenmile, plano, SYNC SAC, ocorrência, rota, programação diária.
2. Liste ações reais do usuário, não apenas casos técnicos.
   - Adicionar, trocar, remover, sincronizar, recarregar, carregar mais, tentar de novo, falhar, deixar vazio, editar em outro sistema, usar dado antigo.
3. Para cada ação, separe:
   - O que o usuário faz.
   - O que o sistema deveria fazer.
   - O que já foi implementado.
   - O que não foi implementado ou não foi validado.
   - Risco anti-burro.
4. Inclua cenários felizes, vazios, divergentes, repetidos, removidos, atrasados, cacheados, falhas externas e dados incompletos.
5. Marque prioridades com julgamento claro:
   - `Alta`: pode mostrar dado errado, velho ou causar decisão operacional errada.
   - `Média`: pode confundir ou perder cobertura em caso comum.
   - `Baixa`: melhora UX, clareza ou polimento.

## Formato Padrão

Responda em português do Brasil e use tabela Markdown.

Tabela principal:

| Cenário | O que o usuário faz | Resultado esperado | Status | Risco anti-burro | Prioridade |
|---|---|---|---|---|---|
| ... | ... | ... | Implementado / Parcial / Não implementado / Não validado | ... | Alta / Média / Baixa |

Depois da tabela principal, adicione um resumo curto:

| Prioridade | Falta / validação | Por que importa |
|---|---|---|
| Alta | ... | ... |

## Regras

- Não maquiar lacunas. Se não foi validado, escreva `Não validado`.
- Não dizer que está implementado só porque "parece provável"; use `Esperado` ou `Precisa validar`.
- Foque no usuário, não em arquitetura interna.
- Prefira frases operacionais curtas.
- Inclua cenários de remoção de dado, troca de dado, dado vazio e cache sempre que houver sync, integração ou tela com atualização.
- Quando houver risco de dado velho aparecer, destaque como `Alta`.
- Quando houver diferença entre fonte oficial e fonte externa, explicite as duas fontes.
- Quando o usuário pedir "anti-burro", seja rigoroso: procure cenários de clique repetido, ordem errada, falta de refresh, integração atrasada, duplicidade, valor antigo e falha parcial.

## Status Permitidos

Use estes rótulos:

- `Implementado`: há evidência suficiente no contexto ou no código.
- `Parcial`: parte funciona, mas há lacuna relevante.
- `Não implementado`: ainda não existe comportamento.
- `Não validado`: pode existir, mas não há evidência.
- `Depende do dado externo`: sistema só consegue agir se a integração retornar o dado.

## Exemplo Curto

| Cenário | O que o usuário faz | Resultado esperado | Status | Risco anti-burro | Prioridade |
|---|---|---|---|---|---|
| Remove motorista externo e sincroniza | Tira motorista no sistema externo e clica SYNC | O nome antigo deve sumir da tela | Parcial | Mostrar motorista velho como se ainda estivesse vinculado | Alta |
| Troca motorista externo | Altera Motorista A para Motorista B e sincroniza | Tela deve trocar para Motorista B | Implementado | Se cache não renovar, usuário acha que não funcionou | Alta |
| Integração retorna vazio | SYNC retorna motorista vazio | Não mostrar `null`, `undefined` ou texto falso | Implementado | Polui a tela e induz leitura errada | Média |

