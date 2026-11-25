# Perguntas importantes e cobertura por risco

Use ao preparar a fronteira. Isto é mapa de investigação, não perguntas obrigatórias. Cada pergunta aponta uma incerteza concreta e a decisão que muda; dependências aguardam respostas anteriores. Mantenha recomendações do grill sem repetir respostas registradas.

## Visual e aparência

Confira referência aprovada, componentes, hierarquia, linguagem, temas e contexto de uso. Preserve o que já está decidido; não reabra paleta, fontes ou shell. Pergunte decisões ausentes sobre ação principal, informação prioritária, densidade, estados e alcance móvel/desktop. Exemplo: “A configuração precisa funcionar no telefone ou o produto pode restringi-la ao desktop?” Fundamente a recomendação no uso real.

Para direção visual materialmente nova, use o roteamento de design instalado e aceites de composição aplicáveis. Isso não autoriza redesign, protótipo ou implementação automática. A pergunta identifica superfície e resultado esperado; “quer bonito/moderno?” não orienta a entrega. Backend sem superfície afetada não recebe entrevista visual.

## Acessibilidade e extremos

Converta obrigações em critérios, não preferências opcionais: ação disponível sem hover; rótulo/nome acessível; informação além da cor; ordem de teclado; foco visível pelo teclado; foco inicial/retorno e saída do modal; anúncio de progresso/erro; recuperação; zoom/textos longos; redução de movimento quando houver animação. Respeite o projeto: foco por teclado, sem halos decorativos no clique.

Pergunte escolhas de comportamento/público ainda abertas. Ação inacessível é defeito, não oportunidade de perguntar se pode ignorá-lo. Sem UI implementada, proponha a prova futura por teclado, tecnologia assistiva, viewport e estados pertinentes. Documento/desenho não comprova acessibilidade real.

## Qualidade e testes

Associe comportamento e fronteira ao menor teste discriminante: unidade/componente para lógica local; persistência/autorização real quando alteradas; isolamento por ator/workspace; retry/idempotência/concorrência/cancelamento quando existirem; erro/vazio/carregamento/recuperação no fluxo. Diferencie teste proposto, executado e comprovado.

Snapshot de botão não prova isolamento/transação/idempotência; double não prova transporte ou persistência real. Corrija alegação sem evidência, não pergunte se o usuário aceita chamá-la de teste aprovado. Pergunte escolhas reais de resultado, como falha parcial, e investigue runners/seams existentes em vez de pedir fatos disponíveis no repo.

## Escala e recursos

Confira volume, bytes, concorrência, latência e limites já definidos. Cenário de 250 linhas não ganha fila/cache por associação. Crescimento comprovado que muda memória/tempo/consistência abre decisões: espera aceitável, simultaneidade, snapshot versus dados mudando, cancelamento, revogação durante trabalho, retenção/expiração e recuperação.

Calcule a partir do contrato; identifique medições ausentes. Resolva resultados esperados antes de escolher tecnologia/provedor/schema. Não invente SLA nem declare escalabilidade por ler spec. Tickets indicam prova de carga/recurso pertinente quando esse requisito existe.

## Segurança, dados e efeitos

Confira identidade/permissão confiável, escopo por operação, workspace, integridade e efeitos externos. Proteção obrigatória é limite, não opção de conveniência. Perguntas definem papéis/regras/exceções dentro do limite. Integração configurada não autoriza envio de teste.

Ideia nova como envio automático reabre gatilho/destinatário/permissão/retry na fronteira aplicável e invalida a aprovação anterior. Capacidade ausente, origem ambígua ou revisor incompleto bloqueia só sua ação dependente, sem mudar entregas selecionadas ou autorizar fallback externo.

## Filtro da rodada

Retire fatos consultáveis, perguntas respondidas, achados duplicados, cosmética sem impacto, decisões ainda dependentes e sugestões fora do escopo. Preserve decisões materiais e pendências que impedem concluir. Se restarem zero perguntas, não invente entrevista: execute a próxima ação autorizada ou peça apenas o gate realmente pendente.
