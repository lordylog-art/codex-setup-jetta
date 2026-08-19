# Governança de features do ERP Jetta

Use este contrato em **toda** feature, correção, melhoria, job, integração ou alteração
operacional do ERP. Ele complementa a constituição e o `AGENTS.md`; quando houver conflito,
prevalece a regra mais restritiva e a decisão explícita do usuário.

## Regra central

Não invente escopo, fluxo, regra de negócio, dado, layout, serviço, job, integração, fallback,
limite ou estratégia de deploy. Reaproveite a evidência do ERP e peça confirmação ao usuário antes
de registrar ou implementar uma decisão que mude comportamento, alcance ou risco operacional.

Fatos determinísticos podem ser descobertos no código. Decisões de produto e operação pertencem ao
usuário. Não transforme ausência de resposta em autorização.

## Contrato de descoberta e aprovação

Antes de planejar ou implementar, criar no `spec.md` uma seção `## Contrato ERP aprovado` com:

| Item | Evidência obrigatória |
|---|---|
| Resultado e limite do escopo | Problema, usuários, unidade/cliente afetados, incluído e fora do escopo. |
| Precedentes do ERP | Módulo, tela, componente, serviço, endpoint, job ou integração mais próximo e caminhos reais. |
| Fluxos preservados | Fluxos, permissões, regras, contratos, ordenação, estados e dados existentes que não podem mudar. |
| Decisões do usuário | Pergunta, resposta, data e impacto de cada decisão não determinística. |
| Matriz de impacto | Cada domínio abaixo marcado como Aplicável ou N/A, com evidência. |
| Aceite e validação | Comportamento observável, estados de erro/vazio/loading, segurança e teste proporcional. |

Pergunte ao usuário, de forma objetiva e uma decisão por vez, sempre que faltar confirmação sobre:

1. resultado esperado, pessoas afetadas, unidade/cliente e limites do escopo;
2. regra de negócio, permissão, cálculo, estado, filtro, ordenação, navegação ou persistência;
3. experiência e composição da tela, ações, feedback, acessibilidade e comportamento móvel;
4. efeito em dados, API, banco, migração, importação/exportação, arquivo, e-mail ou integração;
5. criação/alteração de job, fila, cron, webhook, retry, cache, timeout, limite, fallback ou efeito externo;
6. estratégia de validação, rollout, compatibilidade, observabilidade, `NewDeploy.ps1` ou risco de produção.

O usuário deve aprovar explicitamente o contrato antes de `$speckit-plan`, o plano/matriz antes de
`$speckit-tasks` e as tarefas antes de `$speckit-implement`. Se surgir fato novo que altere uma
decisão aprovada, interrompa e pergunte novamente.

## Hierarquia de reaproveitamento

Use esta ordem e registre a referência encontrada:

1. comportamento existente no mesmo módulo, cliente/unidade e fluxo;
2. implementação mais próxima do ERP para o mesmo tipo de dado ou operação;
3. componente, serviço, contrato, fila ou helper compartilhado já usado pelo ERP;
4. padrão documentado do ERP, incluindo as baselines visuais aplicáveis;
5. novo padrão somente com pedido ou aprovação explícita do usuário.

Não use convenções genéricas de framework quando o ERP já possuir precedente aplicável.

## Página referenciada: investigar antes de reutilizar

Quando o usuário citar uma tela, rota, página, módulo, botão, modal ou fluxo como referência — por
exemplo, “faça como a página X” — isso é uma ordem de investigar o comportamento real, e não apenas
de copiar a aparência. **Invoque obrigatoriamente** a skill
`C:\Users\Jetta\.codex\skills\investigar-detalhes\SKILL.md`; somente lê-la ou citar seu nome não
é suficiente. Sem execução e resultado registrado, não avance para plano, tarefas ou implementação.
Em seguida:

1. localizar a rota/entrada e os arquivos reais da referência;
2. seguir componentes, hooks, serviços, APIs, DTOs, persistência, jobs e testes envolvidos;
3. mapear cada ação visível: condições, permissões, loading, erro, sucesso, cancelamento, fechamento,
   navegação e efeitos externos;
4. mapear dados, formatos, campos obrigatórios, fallbacks existentes, estados vazios/legados e regras;
5. verificar desktop, mobile, acessibilidade, tema e estados interativos quando aplicáveis;
6. testar o estado real em runtime quando for seguro e disponível; caso contrário, declarar que a
   evidência é estática e não afirmar comportamento não observado.

Registrar no contrato da feature: referência citada, rota/arquivos investigados, comportamento
confirmado, dados/contratos/efeitos encontrados, elementos que serão reutilizados e diferenças
aprovadas. Não transportar seletivamente um layout, API, regra ou job sem entender o fluxo completo.
Se a referência for ambígua, inacessível ou divergir do pedido, parar e pedir ao usuário que confirme
qual parte deve ser seguida; nunca preencher a lacuna com uma interpretação própria.

## Matriz de impacto obrigatória

Avalie e registre evidência para todos os domínios; `N/A` exige motivo curto.

| Domínio | Verificar antes de decidir |
|---|---|
| UX e interface | Shell, topbar, navegação, composição, tabela/blocos, modais, estados, acessibilidade, desktop, tablet e celular. |
| Fluxo e negócio | Atores, permissões, estados, transições, cálculos, filtros, ordenação, mensagens e fluxos legados preservados. |
| Frontend e API | Componentes reutilizados, contratos, payloads, erros, paginação, autenticação e efeitos em consumidores existentes. |
| Dados e banco | Schema, migration, backfill, índices, integridade, volume, timezone e compatibilidade com dados legados. |
| Jobs e filas | Gatilho, agendamento, concorrência, idempotência, retry, erro explícito, observabilidade e impacto de duplicação. |
| Integrações e efeitos externos | Contrato, autenticação, rate/timeout, idempotência, auditoria, webhook, e-mail pela fila global e autorização para efeitos reais. |
| Segurança e privacidade | Papéis, escopo de cliente/unidade, validação no backend, exposição de dados, logs e segredos. |
| Desempenho e observabilidade | Volume real, consultas, paginação, cache aprovado, métricas, logs operacionais e sinais de falha. |
| Deploy e operação | Build, variáveis, artefatos, provider/runtime, `NewDeploy.ps1`, migration, health check e rollback sem downtime não autorizado. |
| Testes e aceite | Testes existentes afetados, validação proporcional, falhas pendentes e evidência de aceite. |

## Regras por tipo de mudança

- **Tela ou UX**: seguir a baseline e o precedente funcional; especificar estados, teclado, foco,
  erro, vazio, loading, responsividade e efeitos de cada ação. Tela nova exige escolha explícita da
  composição. Modal segue `modal-operacional` quando aplicável.
- **Regra de negócio**: documentar comportamento antigo, mudança proposta, casos de borda,
  autorização e consequência para fluxos existentes. Não alterar sem aprovação explícita.
- **API, contrato ou integração**: preservar compatibilidade; definir entradas, saídas, erros,
  autenticação, autorização, idempotência e consumidores afetados antes de codificar.
- **Banco ou dados**: não criar migration, backfill, limpeza ou mudança de semântica sem confirmação
  do usuário e plano de compatibilidade/reversão.
- **Job, fila, cron ou webhook**: reutilizar infraestrutura existente; definir dono, gatilho,
  frequência, concorrência, idempotência, retry, falha visível e efeitos externos. Não criar limite,
  fallback ou retry por suposição.
- **E-mail**: usar exclusivamente a fila global do ERP e declarar se o fluxo aguarda `SENT`/`FAILED`.
- **Deploy/runtime**: revisar `NewDeploy.ps1` e declarar por que já cobre a mudança ou o que deve
  mudar. Nunca executar ação que possa causar indisponibilidade sem autorização específica.

## Bloqueios de conformidade

É bloqueante seguir adiante quando faltar: aprovação do usuário, precedente/evidência pesquisado,
matriz de impacto, decisão sobre efeito externo, preservação de fluxo antigo, critério de aceite ou
declaração de compatibilidade operacional. O agente deve parar, explicar o ponto objetivo e perguntar;
não pode escolher uma alternativa silenciosamente.

## Evidência de encerramento

O resultado de uma feature deve declarar as referências reutilizadas, decisões aprovadas, domínios
impactados, comportamento preservado, validações executadas/não executadas, falhas pendentes e
compatibilidade com `NewDeploy.ps1`. Se o escopo aprovado não estiver totalmente coberto, relatar a
lacuna em vez de alegar conclusão.
