---
name: nosso-design
description: Criar ou alterar telas do próprio ERP Jetta com seus componentes e padrões existentes. Não se aplica ao Jetta Control, programas auxiliares, HTML avulso ou backend sem UI.
---

# Nosso Design

Preserve a identidade visual real do ERP em qualquer alteração, de um botão a uma tela inteira.

## Aplicabilidade e alvo visual

Antes de carregar referências ou iniciar servidores, identifique o arquivo/componente alterado e seu contexto real. Aplique esta skill à UI do próprio ERP Jetta, inclusive componentes isolados representados no Storybook. Estar no repositório Jetta, compartilhar o nome da empresa ou usar localhost não torna uma interface parte do ERP.

Jetta Control (`tools/deploy-control`), programas auxiliares, protótipos e HTML avulso usam os componentes e o meio de execução do próprio artefato. Valide o visual no programa, página ou preview correspondente; não abra o ERP nem use suas capturas como evidência desses trabalhos. Mesmo se o usuário pedir inspiração na identidade do ERP, isso autoriza consultar referências, não iniciar o runtime ERP sem dependência concreta. Se o ambiente não permitir renderizar o alvo correto, informe essa lacuna; abrir outra aplicação não a resolve.

## Regra principal

Antes de JSX ou CSS:

1. Reutilize referências/descobertas válidas no contexto; diante de lacuna, leia [references/INDEX.md](references/INDEX.md), classifique a família e abra somente as referências pertinentes.
2. Inspecione o componente canônico e a página existente mais próxima quando ainda não cobertos pela descoberta válida.
3. Reutilize componentes, classes, tokens, fontes, ícones, imagens e padrões de interação; componha o conteúdo conforme a tarefa.

As referências definem a identidade visual. Avalie a composição pelos critérios abaixo: existir no ERP não torna um layout aprovado. Dentro do escopo, ajuste agrupamento, hierarquia, alinhamento e proporções com os padrões da família, sem pedir aprovação para cada ajuste local.

## Qualidade da composição

- Destaque a informação necessária para a tarefa ou decisão; decoração e cabeçalhos devem ter peso proporcional.
- Agrupe dados relacionados e aproxime valores que precisam ser comparados. Use cartões quando houver grupos distintos, não um cartão por campo.
- Alinhe título, conteúdo e ações em recuos consistentes. Dimensione a superfície pelo conteúdo, pela legibilidade e pelo viewport; evite vazios acidentais e texto colado às bordas.
- Use cores de estado para comunicar significado. Mantenha ações agrupadas, consequências explícitas e uma ação visualmente principal quando houver prioridade real.

## Invariantes

- Reutilize o equivalente compatível; não introduza valor visual arbitrário, ativo substituto, template externo, estética genérica “SaaS/AI” nem mistura entre famílias.
- Preserve a tela e o legado fora do escopo. Prefira escopo/componente local a CSS global.
- Dashboards novos usam exclusivamente `@/components/dashboard`, permanecem em `.jetta-dashboard` e usam classes Tailwind `jetta:`.
- Compor localmente a partir do kit não exige mudá-lo. Generalize primitivos compartilhados somente quando duas superfícies reais precisarem da capacidade ou a entrega depender disso.
- Sem equivalente canônico, prefira composição local com os padrões existentes dentro do escopo autorizado. Peça decisão quando a novidade mudar materialmente a identidade visual, os contratos compartilhados ou o escopo.

## Fluxo

Esta skill define identidade e componentes do ERP. Reutilização ou ajuste focal pede apenas inspeção e testes dos aspectos alterados. Consulte a seção **Prova visual** do Impeccable instalado quando houver decisão visual relevante ou auditoria solicitada; não encadeie especialistas automaticamente. Use [QA visual](../../qa-visual.md) somente quando a prova precisar de ambiente/autenticação ou plugin Storybook. Compartilhe capturas válidas; sua execução não certifica o visual.

1. Determine a tarefa, a informação decisiva e a hierarquia das ações; localize tela/componente análogo. Discussão ou spec não autoriza implementação.
2. Use a referência válida da rota análoga; consulte novamente somente diante de mudança ou lacuna, ignorando rotas redirecionadas ou não canônicas.
3. Para aparência, espaçamento, layout, hierarquia, ativo ou tela completa, use o screenshot de referência já inspecionado e ainda válido; abra-o se faltar inspeção pertinente. Ao reutilizar exatamente um componente sem mudar aparência, basta registrar o arquivo canônico.
4. Leia o código apontado; screenshot não substitui comportamento, acessibilidade ou contratos.
5. Faça o menor diff, preservando shell, estados, responsividade e tema escuro existentes.
6. Use **Storybook como ambiente principal para componentes isoláveis**, com componente real, estilos/tokens e contexto relevantes. Baixo risco pede inspeção focal do estado alterado, sem ERP automático nem ritual visual completo; nos demais, valide estados/interações pertinentes e dados extremos capazes de refutar o layout. Use o ERP real quando autenticação, navegação, providers, layout integrado, comportamento nativo dependente da aplicação ou critério explícito exigirem essa fronteira; story que não reproduz o contexto não é equivalente. Confira outro viewport quando responsividade for afetada ou exigida; em tela inteira, compare também com a família canônica. Inspecione composição e corrija falhas materiais; testes de classes não comprovam qualidade visual. Reutilize capturas/inspeções válidas no mesmo conteúdo, contexto, estado, dados, viewport e tema; reexecute somente a prova invalidada.
7. Se a captura faltar, procure outro análogo e use o código canônico como evidência disponível; informe a lacuna de validação. Peça decisão apenas se faltar uma direção visual material.
8. Na entrega, cite componente, referência e evidência visual do estado alterado. Se não conseguiu renderizar ou inspecionar, declare a validação visual pendente. Registre lacunas e decisões materiais conforme as invariantes.

## Atualizar referências

Recapture evidências somente no localhost com [scripts/capture-erp-design.mjs](scripts/capture-erp-design.mjs) e sessão local provisionada. O script não autoriza produção, cliques de escrita ou exposição de credenciais. Capturas redigidas provam aparência; o código continua sendo a fonte de verdade.
