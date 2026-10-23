# TDD Decente

Use este padrao em qualquer skill ou instrucao que altere comportamento.

## Objetivo

Proteger comportamento real e regressao real. Teste que so valida helper isolado, existencia de string no source, ou snapshot sem fluxo nao basta quando o bug vive na orquestracao da feature.

## Regras obrigatorias

1. Defina o comportamento publico em uma frase antes de editar.
2. Escolha o menor nivel de teste que realmente detecta a regressao.
3. Escreva ou atualize o teste antes do codigo de producao.
4. Rode o teste em `red` e confirme que ele falha pelo motivo esperado.
5. Implemente o menor ajuste necessario.
6. Rode o mesmo teste em `green`.
7. Rode a regressão adjacente mínima usando os comandos automatizados nativos mais próximos do escopo alterado.

## Como escolher o nivel certo do teste

- Use teste de unidade quando a regra esta inteiramente contida em uma funcao pura e o bug nao depende de encadeamento entre componentes.
- Use teste de integracao quando o comportamento depende da colaboracao entre modulo, estado, servico, repositorio, DTO, permissao ou adaptador.
- Use teste de fluxo de UI quando a regressao depende de clique, estado, modal, drawer, confirmacao, ordenacao, render condicional ou encadeamento de callbacks.
- Use smoke/E2E quando o risco principal esta na integracao real entre frontend, backend, auth, ambiente, deploy ou automacao.

## Heuristica anti-teste-fraco

Se o bug foi percebido pelo usuario em um fluxo real, pelo menos um teste deve exercer esse fluxo no mesmo nivel ou em nivel imediatamente abaixo que ainda consiga quebrar antes da correcao.

Nao aceite como cobertura suficiente:

- teste so de helper quando a falha real depende de orquestracao
- teste que verifica apenas que modal/string/classe existe no source
- snapshot sem acao do usuario
- mock que elimina exatamente a integracao onde o bug mora
- smoke generico que nao passa pelo caminho corrigido

## Obrigatorio para bugfix

Todo bugfix precisa ter pelo menos:

- 1 teste de regressao que reproduz o bug relatado ou o estado equivalente
- 1 verificacao do caminho corrigido no nivel mais proximo do uso real

Se o bug envolver UI com decisao condicional, o teste deve validar a acao do usuario e o resultado visivel ou o proximo estado esperado.

## Obrigatorio para UI/orquestracao

Quando a mudanca toca UI, estado ou orquestracao:

- valide o gatilho da acao
- valide a transicao de estado
- valide o resultado visivel ou a proxima decisao do fluxo
- valide pelo menos um edge case relevante introduzido pela mudanca

Exemplo de edge case: carga sem motorista, placa mantida, motorista ainda em outra carga.

## Obrigatorio para mutacao imperativa de DOM e troca de layout

Quando a UI depende de codigo que move/altera DOM fora do reconciler do framework ou troca entre layouts/branches distintos:

- cubra a transicao real entre os modos, nao apenas cada modo isolado
- prefira teste de interacao/integracao que execute a troca e falhe com erros de reconciliacao como `removeChild`, `insertBefore`, hydration mismatch ou crash do renderer
- trate como alto risco casos com scroll sync, portal customizado, drag/drop imperativo, observer que reescreve markup, ou toggles como `table/grid`, `list/calendar`, `inline/portal`

Nao aceite como suficiente:

- teste que renderiza apenas o modo final sem passar pela troca real
- teste de source/classe que nao exercita a desmontagem/remontagem da arvore
- smoke generico sem clicar no toggle ou sem atravessar o branch que derrubava o renderer

## Obrigatorio para backend/permissao/integracao

Quando a mudanca toca API, auth, permissao, jobs ou integracao:

- cubra o contrato publico afetado
- cubra a regra de permissao ou validacao alterada
- cubra um caminho negativo relevante

## Obrigatorio para integracoes em lote, payload grande e fan-out

Quando a mudanca toca sync, importacao, persistencia em lote, consulta externa, enriquecimento de dados, cache de integracao ou qualquer fluxo que envie muitos itens para outro endpoint/servico:

- cubra o caminho publico/orquestrado que monta e envia o lote, nao apenas o helper de chunk
- teste pelo menos um lote abaixo do limite de quantidade que ainda estoura por tamanho de payload quando isso for possivel
- valide que a correcao divide em multiplas requests seguras e preserva todos os itens
- valide que cada request respeita o limite operacional conhecido, por exemplo tamanho maximo de body, quota, pagina, batch ou timeout
- valide fan-out quando um resultado de integracao precisa atualizar multiplas linhas/entidades irmas
- valide que erro de persistencia/consulta externa aparece no contrato ou na UI quando o usuario depende desse feedback

Nao aceite como suficiente:

- teste somente de `chunk(items, 50)` quando o bug real depende do tamanho serializado do JSON
- teste so com muitos itens pequenos quando o risco real vem de poucos itens grandes
- mock que retorna sucesso sem inspecionar o body enviado ao endpoint
- teste que valida somente a primeira linha atualizada quando o fluxo deve propagar para linhas irmas
- teste de helper isolado sem exercitar a rota, job, scheduler ou acao que usa o helper

Exemplo de regressao esperada: 10 cargas com snapshots grandes da Greenmile devem virar mais de uma request para `/daily-loads/greenmile-enrichment`, cada body abaixo do limite da API, e a soma dos itens persistidos deve continuar sendo 10.

## Obrigatorio para restricoes, elegibilidade e alocacao

Quando a mudanca toca qualquer regra de:

- restricao operacional
- elegibilidade de motorista/veiculo
- bloqueio por regiao, dia ou capacidade
- atribuicao manual ou automatica
- selecao, ignorar, pular ou barrar candidatos

alem da cobertura automatizada, exija uma validacao pratica no endpoint ou fluxo real quando houver ambiente local seguro para isso.

Minimo esperado:

- 1 caso real em que a regra permite a operacao quando deveria permitir ou
- 1 caso real em que a regra bloqueia/ignora a operacao quando deveria bloquear

Se houver mais de um tipo de restricao alterado, valide cada tipo no fluxo real sempre que o custo for razoavel.

Nao aceite como suficiente:

- apenas teste de funcao pura de matching de regiao
- apenas mock do servico sem chamada ao endpoint real
- apenas leitura de codigo dizendo que "deve barrar"

Se o endpoint real nao puder ser usado com seguranca, registre explicitamente o motivo e qual smoke real ficou pendente.

## Evidencia minima esperada no fechamento

- comportamento protegido
- teste adicionado/atualizado
- evidência de `red` quando praticavel
- evidência de `green`
- suites adjacentes executadas
- resultado dos comandos automatizados relevantes

## Quando o red literal nao for praticavel

Se o harness estiver quebrado, o ambiente impedir execucao, ou o red literal causar custo desproporcional:

- diga isso explicitamente
- registre qual seria o teste de regressao correto
- adicione a cobertura mais forte possivel no nivel imediatamente abaixo
- nunca chame isso de `TDD completo`

## Regra de reprovacao

Se a mudanca altera comportamento e nao existe teste capaz de detectar a regressao real, a entrega nao esta suficientemente protegida e deve ser tratada como incompleta.
