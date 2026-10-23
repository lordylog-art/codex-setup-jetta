---
name: templates-new-move
description: Selecionar, reutilizar e criar templates de telas e modais do New Move, incluindo layout, Jotinha e transições. Use ao compor ou migrar interfaces do ERP Move e ao manter /templates; operações como SAC e Disponibilidade são referências, não limites de reutilização.
---

# Templates New Move

Reutilize a composição existente em runtime. Escolha pela tarefa e densidade de informação; SAC, Guarulhos e Disponibilidade são exemplos de aplicação, não uma taxonomia de componentes por operação.

## Localizar a fonte

1. Confirme checkout autorizado, instruções locais e presença de `apps/web/src/app/templates`. Leia `docs/templates-new-move.md`: metadados, índice, regras e os registros pertinentes. Os caminhos do catálogo são relativos à raiz desse checkout.
2. Leia a implementação indicada antes de editar: `catalogo-uso-modais.ts` resolve padrões; o catálogo Markdown registra decisões, contratos e aparência. Em divergência, confirme a implementação e relate a divergência; código atual não invalida uma regra aprovada.
3. Se o checkout não contiver o catálogo, procure uma worktree já vinculada ao trabalho. Base integrada conhecida: `D:/newmove/docs/templates-new-move.md`. Verifique sua existência e autorização antes de operar. Um candidato isolado não comprova integração em `D:/newmove`, nem autoriza copiar arquivos entre bases.

Para migração central e operação/CC, aplique `new-move` quando disponível e leia o documento da migração no checkout que o contém. Para UI, mantenha os padrões de `nosso-design` e `impeccable` quando disponíveis. Esta skill não inicia runtime ou QA para uma tarefa apenas documental.

## Reutilizar antes de pesquisar alternativas

Para adaptação de tela/modal com referência aprovada, reutilize essa decisão e leia apenas o registro, componente e consumidores pertinentes. Não refaça inventário do catálogo inteiro nem compare duas variantes por rotina. Uma busca focal basta para localizar o padrão; amplie somente se ele não atender ao conteúdo ou houver conflito concreto.

Quando houver escolha de composição realmente nova, compare as opções pertinentes e comunique em uma frase componente/preset, proporção e motivo. Ficha detalhada e matriz de variantes somente quando solicitadas ou quando forem necessárias para resolver uma decisão visual material. Não interrompa implementação já autorizada para obter aprovação intermediária.

Preserve handlers, validações, foco/teclado, descarte, estados e identidade. Verifique os aspectos alterados no mecanismo pertinente; acessibilidade continua parte da implementação, sem exigir uma auditoria completa para cada reutilização. Priorize testes automatizados; navegador interativo para aparência ou lacuna concreta que a automação não cubra.

## Selecionar e compor

- Resolva o objetivo para um `pattern_id` do catálogo; selecione depois um `reference_id` próximo em campos e interações. Escolha comportamento antes da imagem.
- Defina tamanho, apresentação, altura e posição separadamente. Comece pelo recomendado do padrão; conte os campos, comprimento dos textos, linhas e ações do caso real. Use a tabela de dimensões do catálogo para o componente escolhido.
- Mantenha Jotinha lateral em quase todos os cenários de desktop. Conteúdo denso amplia a superfície e reduz a ilustração; informações e KPIs relevantes dominam. Esquerda é ponto inicial, direita é variante compatível; não associe lado a uma operação.
- Escolha o asset pelo estado/ação e registre o caminho existente. Preserve identidade cartoon, recorte, qualidade e ausência de logos. Para imagens novas autorizadas, use imagegen com uma referência atual do personagem; consulte as regras e o mapa de imagens do catálogo.
- Reutilize o componente exportado e seus estilos. Componentes de exemplo não são APIs de backend. Adapte dados e handlers reais sem importar fixtures de operação para o produto.
- Integração real conserva autorização, validações, contexto de CC, regras e efeitos existentes. O consumidor fornece estado confirmado e mensagens da operação. Se um componente já for compartilhado com telas reais, a alteração atinge esses consumidores: examine os usos antes de editar.

### Escolha de variante quando necessária

Em composição nova ou materialmente alterada, escolha uma variante e comunique brevemente: **padrão/modal + tamanho e largura de referência + apresentação + altura + lado e escala do Jotinha + motivo**. Faça essa escolha autonomamente conforme o conteúdo e as preferências já dadas; a declaração é informação de execução, sem uma etapa adicional de aprovação.

Trate os eixos separadamente: `compacto | padrao | amplo` é tamanho; `ilustrado | conteudo` é apresentação; `padrao | alta` é altura; `esquerda | direita` é posição; `menor | padrao | maior` é escala. “Expandido” corresponde à apresentação `conteudo`, podendo ter qualquer um dos três tamanhos. Resolva expressões como “pequeno amplo” em uma configuração inequívoca, distinguindo tamanho do modal e tamanho do personagem.

| Conteúdo real | Ponto de partida para escolher |
| --- | --- |
| Resultado, aviso ou decisão curta | Compare compacto, padrão e amplo ilustrados pela proporção final, respiro, texto e personagem; mensagem curta também pode usar padrão ou amplo. |
| Formulário ou filtros de rotina | Padrão ilustrado; use conteúdo expandido quando houver muitos campos. |
| Busca com lista de candidatos | Conteúdo expandido, altura alta, busca fixa e Jotinha menor. |
| Tabela, lote ou formulário extenso | Amplo com conteúdo expandido, altura alta e Jotinha menor. |

Consulte `layout_matrix` para a largura efetiva e os limites da viewport. Conteúdo expandido mantém o personagem lateral menor e prioriza os dados; reserve a área acima dele para KPIs pertinentes quando existirem. Escolha esquerda ou direita pela composição e pelo pedido. Na apresentação `conteudo`, a figura já tem tamanho menor fixado pelo layout; a escala ilustrada não implica outra dimensão nesse modo.

Exemplos de resumo para decisões novas:

- “Vou usar confirmação compacta ilustrada, largura de referência de 760 px, altura padrão e Jotinha à direita em escala menor, porque a composição permanece horizontal e acomoda texto, personagem e ações com respiro.”
- “Vou usar busca ampla com conteúdo expandido, largura de referência de 1400 px, altura alta e Jotinha menor à esquerda; a busca ficará fixa acima da lista.”

Use a configuração abaixo apenas quando ela ajudar o handoff ou quando solicitada; não é um artefato obrigatório de reutilização. Mapeie os valores semânticos para as props reais do componente escolhido e confirme a compatibilidade no código; para várias ocorrências, especifique uma seleção por contexto distinto. Resultados e confirmações de descarte também recebem composição própria, proporcional à mensagem, em vez de herdar automaticamente o tamanho do formulário de origem.

```yaml
selection:
  pattern_id: busca
  reference_id: atribuicao
  component: ModalCenario
  layout: { tamanho: padrao, apresentacao: conteudo, altura: alta, posicao: esquerda, escala: menor }
  image: /templates/avatar-cadastro.png
  scope: operation_id_fornecido_pelo_consumidor
  transitions: { vazio: aviso, falha: erro, concluido: sucesso, sair_com_rascunho: confirmacao_descarte }
  rationale: busca fixa e lista longa de candidatos
  alternative_considered: amplo/conteudo/alta/direita; padrao atende a lista e preserva espaço da tela
```

Use valores verificados, não copie a decisão acima como configuração universal.

### Proporção visual antes da menor dimensão

Escolha pela composição renderizada, não pelo menor tamanho em que os campos cabem. Pouco texto não exige compacto. Avalie largura versus altura efetiva, quebras de linha, espaço entre informação e personagem e equilíbrio do rodapé. Quando o compacto ficar quadrado, alto demais ou apertado, compare padrão/amplo e outra distribuição existente antes de escolhê-lo. Altura alta atende conteúdo longo; não a aplique a uma decisão curta para preencher espaço.

Na ficha, descreva a proporção esperada e por que a variante funciona visualmente. “Cabe no menor” não é justificativa suficiente. Defaults e recomendações de tamanho do catálogo são candidatos de avaliação, não uma seleção automática; preserve contratos obrigatórios do componente.

### Variedade intencional na seleção

Quando houver decisão nova sem referência aprovada, compare variantes compatíveis que possam alterar o resultado visual. Considere tamanho, apresentação, altura, lado, escala e imagem do Jotinha; registre brevemente a alternativa considerada e o motivo da escolha. Quando só houver uma composição compatível, registre essa limitação.

Ao projetar um conjunto novo de modais sem composições aprovadas, uma matriz curta pode ajudar: `contexto | tamanho | apresentação | altura | lado/escala | imagem | motivo`. Revise o conjunto antes de implementar: distribua as variantes disponíveis conforme densidade, tarefa e hierarquia visual. Entre opções igualmente adequadas, prefira a composição menos utilizada no conjunto. Verifique a distribuição dos tamanhos e apresentações: mudar apenas o lado ou a imagem do Jotinha não resolve uma sequência de modais igualmente compactos e quadrados. Se todos receberem o mesmo tamanho, reavalie o conjunto e apresente motivos específicos quando a uniformidade continuar sendo necessária. A tabela de pontos de partida orienta a avaliação; cada linha admite outras combinações compatíveis.

Reavalie escolhas idênticas em contextos distintos e justifique a repetição pela necessidade real. Preserve a mesma composição para o mesmo contexto e fluxo recorrente: variedade é uma decisão estável de design, sem sorteio ou alternância a cada abertura. Respeite preferências explícitas, acessibilidade e espaço para informações; mantenha identidade, componentes e comportamento compartilhados.
## Resultados e composição obrigatória

Aplique as regras `R-*` do catálogo na extensão que a tarefa toca. Pontos que definem esta biblioteca:

- Sucesso usa `ModalResultado` e `ConfirmationIcon animated`, o mesmo componente da captação. Falha usa o padrão de erro; aviso usa o padrão de orientação. Resultado substitui o anterior: um único diálogo de resultado aberto, inclusive em cadeias aninhadas.
- Preserve `useDialogoTemplate`, seus providers, foco, restauração e bloqueio de rolagem. O formulário suspenso permanece montado para correção. Finalização encerra a origem; não reabra uma etapa concluída. Confirmação de descarte é decisão intermediária e conserva o rascunho.
- Ações principais azuis; vermelho reservado ao erro. Indicadores de validade podem comunicar situação documental em verde/vermelho sem transformar a ação principal em vermelha.
- Ações em `AcoesModal`, fora da rolagem e alinhadas à direita. Busca de candidatos fixa, uma rolagem geral. Preserve associação `form` de botões submit e o contorno de foco inteiro.
- Motorista/veículo usa `CartaoMotorista`, `VeiculoMotorista` ou `PerfilVeiculoMotorista`, conforme o caso. Foto e identidade formam um bloco; use as imagens canônicas da Disponibilidade.
- Anexos usam a seleção customizada, arquivos revisáveis e remoção explícita. KPIs e ações têm SVG dimensionado e não se sobrepõem ao texto. Use dados reais para indicadores.
- Acompanhamento prioriza uma operação e suas etapas, sem histórico textual no painel. Etapas vêm do consumidor; minimizar não cancela; resultado incerto exige reconciliação antes de retry.
- Texto de produto descreve a operação. O ambiente de catálogo continua isolado mesmo com aparência real. Template Mãe permanece uma tela completa; as regras de largura e ilustração de modal não são aplicadas ao seu banner.

## Quando falta um template

Primeiro verifique composição com os padrões existentes. Se falta uma capacidade, sinalize a lacuna antes de inventar outra identidade ou contornar contratos:

```yaml
template_gap:
  need: tarefa_e_dados_reais
  closest_pattern: id_ou_nenhum
  missing_capability: comportamento_ou_composicao_ausente
  proposal: compor_existente_ou_novo_padrao
  scope: arquivos_e_consumidores_afetados
  authorization: ja_autorizado_ou_decisao_necessaria
```

A sinalização não obriga nova confirmação se o usuário já autorizou criar essa capacidade. Prossiga dentro dessa autorização; se o pedido for só escolher/reutilizar, apresente a lacuna e proposta sem implementar um novo template por conta própria.

## Criar ou ampliar

1. Reutilize primeiro moldura, footer, resultados, assets, métricas e cards existentes. Crie capacidade global com dados/slots/handlers; use operação apenas como referência demonstrável.
2. Preserve a ordem de domínio. Na ocorrência SAC, consulte a ordem documentada; disposição não é apenas estética. Defina estados, saídas e transições antes de fechar a composição.
3. Registre a nova entrada em `docs/templates-new-move.md` pelo schema `registration_schema`; atualize o registro TS, a descrição visível, o preview de código e a navegação quando forem aplicáveis. Atualize entradas existentes na mesma alteração que muda seu contrato; evite dois catálogos detalhados divergentes.
4. Valide conforme o pedido e o risco. Se testes/QA estiverem autorizados, cubra sucesso, erro, vazio, pendência/incerteza, Escape, rascunho, foco/submit, rolagem e contagem de diálogos; inspecione os layouts afetados no navegador. Skill documental pede validação de fontes/links/schema, sem iniciar ERP.
5. Relate componente escolhido, variante, novos registros e evidência real. Catálogo local, integração e produção são estados diferentes. Preserve as permissões de CI, push, deploy e envios externos definidas pelo projeto.

## Saída e manutenção

Conclua quando o comportamento/composição pedido estiver implementado com o padrão pertinente, consumidores preservados, novos contratos registrados quando existirem e verificações afetadas realizadas. Informe resultado e limitações uma vez; pesquisa, fichas e matrizes não são entregáveis obrigatórios de uma adaptação já decidida. Use a seção de registro do catálogo para cada criação/evolução. Não grave credenciais, tokens, fixtures pessoais ou evidência operacional sensível na documentação.
