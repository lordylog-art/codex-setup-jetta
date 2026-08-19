---
name: investigar-detalhes
description: Investigar profundamente telas, fluxos, botões, menus, modais, APIs e regras antes de criar TDD ou implementar, levantando tudo que cada elemento deve fazer, incluindo cliques, estados, formatos de dados, contratos, efeitos colaterais, caminhos alternativos e lacunas de teste. Use quando o usuário pedir para olhar profundamente, investigar a fundo, detalhar uma tela/fluxo/botão, descobrir comportamento esperado de produção ou preparar cenários de TDD.
---

# Investigar Detalhes

## Objetivo

Investigar o comportamento real de uma tela, fluxo ou ação antes de propor testes ou alterações. A entrega deve dizer "tudo que isso precisa fazer" com base no código existente, testes, contratos e efeitos observáveis, sem inventar endpoint, tabela, payload ou regra.

## Fluxo

1. Delimitar o alvo exato: tela, rota, botão, modal, API, fluxo ou regra citada pelo usuário.
2. Localizar os pontos de entrada: rotas, páginas, componentes, hooks, services, DTOs, migrations, handlers de API e testes existentes.
3. Seguir o fluxo de usuário ponta a ponta, incluindo cliques, menus, atalhos, modais, navegação, estados de loading/erro/sucesso e fechamento.
4. Seguir o fluxo de dados ponta a ponta, incluindo origem dos campos, fallbacks, formatações visíveis, normalizações, dados derivados e persistência.
5. Mapear contratos públicos: endpoints, métodos, payloads, respostas, erros, permissões, writes em banco, e-mails, anexos, jobs e integrações externas.
6. Mapear variantes reais: caminho feliz, dados ausentes, dados legados, permissão negada, erro de rede, item desabilitado, clique repetido, cancelamento e comportamento mobile/desktop quando aplicável.
7. Comparar com os testes existentes e apontar lacunas de TDD no nível mais próximo do uso real.
8. Entregar conclusão objetiva com evidências em arquivos/linhas, separando fato confirmado de inferência.

## Checklist De Cliques E UI

Para cada botão, link, linha clicável, menu ou ação:

- Registrar texto visível, `aria-label`, role e onde aparece.
- Identificar se o clique é direto ou passa por menu/action sheet/dropdown.
- Verificar condições de exibição, desabilitado, loading e permissão.
- Verificar `onClick`, `onContextMenu`, `stopPropagation`, `preventDefault` e tratamento de alvo interativo.
- Verificar se o clique fecha outro modal/menu antes de abrir o próximo.
- Verificar estado inicial criado pelo clique e quais campos são resetados.
- Verificar eventos de fechamento: clique fora, `Escape`, cancelar, voltar, submit concluído.
- Verificar se a ação apenas abre UI ou se já dispara side effects como POST, sync, e-mail, upload, navegação ou write no banco.

## Checklist De Dados

Para cada campo exibido ou enviado:

- Registrar a origem primária e todos os fallbacks.
- Confirmar formatos visíveis, especialmente combinações como `Código - Cliente`, placa, rota, nota, pedido, valor, peso e status.
- Distinguir ID técnico, código externo, label humano e chave de persistência.
- Verificar se dados externos/legados podem chegar sem acento, vazios, duplicados ou em formatos alternativos.
- Confirmar quais campos são obrigatórios em UI, API e banco.
- Identificar o que não deve aparecer para o usuário, como JSON cru, IDs internos ou mensagens técnicas.

## Checklist De TDD

Propor testes que capturem regressão real, não apenas helpers isolados:

- Teste de interação para cada caminho de abertura ou submit.
- Teste para cada formato visível crítico.
- Teste para fallback de dados ausentes ou legados.
- Teste para diferenciar ação parecida: link que navega versus botão que abre modal, menu que abre versus submit que salva.
- Teste negativo para erro, permissão, validação obrigatória e clique em elemento interativo dentro de container clicável.
- Teste de contrato/API quando houver payload, persistência, e-mail, anexo ou integração.

## Forma Da Resposta

Responder em português do Brasil, direto e com detalhes operacionais. Preferir esta estrutura:

- `O que a tela/fluxo deve fazer`
- `Detalhes de clique e estado`
- `Dados e formatos importantes`
- `Contratos e persistência`
- `Testes existentes`
- `Lacunas de TDD recomendadas`
- `Incertezas / pontos não validados`

Ao citar código local, incluir caminhos de arquivo e linhas quando possível. Se algo for inferência, marcar como inferência. Se não foi validado em runtime, dizer claramente.
