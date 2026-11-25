# Perfis dos peixinhos

Use missões especializadas reais, não personagens narrados por um só agente. Cada peixinho recebe alvo/localização, contratos e requisitos necessários, permissões, superfície de prova e critério de conclusão. Conclui com achados verificáveis, contraprovas e lacunas; ausência de achados também é resultado. Preserve isolamento inicial e autoria ao consolidar. Os IDs abaixo identificam especialidades de auditoria, não personas de uso nem uma lista obrigatória de agentes; não substituem nomes descritivos: “Testar checkout — mobile e teclado”, “Revisar cadastro — dados e permissões” e “Validar pagamentos — retry e recuperação” identificam ação, alvo e foco; “peixinho 02” ou “Golden Fisher” isolados não.

| ID | Perfil | Foco e prova esperada |
|---|---|---|
| 01 | Veterano de produto | Utilidade de cada elemento, adequação à tarefa/público, etapas e dependências, recursos ausentes ou desnecessários, simplificação. Vincular crítica a necessidade real, sem inventar requisito. |
| 02 | Perfeccionista visual | Superfície renderizada: espaçamento, alinhamento, hierarquia, tipografia, contraste, cores, ícones, bordas/sombras, densidade e acabamento entre estados. Usar identidade e componentes existentes; preferência estética fica identificada. |
| 03 | Cognição e informação | Esforço mental, decisões simultâneas, agrupamento, ordem de leitura, repetição, descoberta, memória exigida e ambiguidade. Exercitar a jornada, justificar revelação progressiva e redução de passos. |
| 04 | QA implacável | Botões, formulários, validação, modais, busca/filtro, paginação/ordenação, navegação, loading/vazio/erro, rede parcial, repetição, concorrência e atualização de estado. Percorrer normal, alternativo e extremo. |
| 05 | Dados e métricas | Reconciliar UI/API/persistência e regra de negócio, universo dos KPIs, agregação, filtros/períodos, unidades, legendas, gráficos e exposição sensível. Separar regra conhecida de hipótese. |
| 06 | Acessibilidade | Teclado, ordem e indicação de foco, nomes/labels/semântica, contraste, cor, erros, anúncios de estado, alvos, zoom/reflow e leitor de tela se disponível. Distinguir violação observada de risco e ferramenta ausente. |
| 07 | Responsividade | Desktop/notebook/tablet/celular, estreito, retrato/paisagem, zoom, tabelas/gráficos/menu/modal, corte/overflow/sobreposição e toque. Registrar resoluções e estados realmente verificados. |
| 08 | Performance | Medir latência percebida, conteúdo útil, renderizações, JavaScript/assets, requisições redundantes, layout shifts, cache/paginação e degradação com volume. Inspeção estática gera risco, não gargalo medido. |
| 09 | Usabilidade por tarefa | Avaliar orientação inicial, linguagem, descoberta, conclusão, ajuda, erros e recuperação mediante personas concretas de uso definidas abaixo. Separar comportamento observado de interpretação. |
| 10 | Segurança e privacidade | Revisão defensiva não invasiva: exposição sensível, minimização, erros, componentes/integrações e controles de autorização por papel/tenant/operação. Inspecionar controles e fluxos previstos com contas de teste autorizadas; sem exploração, exfiltração ou acesso indevido. |
| 11 | Microinterações e feedback | Hover/focus/active/disabled, loading, erro/sucesso, duplicação de clique, operações demoradas, continuidade, transições/ausência ou excesso de movimento. Avaliar ação e estado final, não só decoração. |
| 12 | Conteúdo e comunicação | Nomes, labels, termos técnicos, ortografia, consistência, contexto, orientação de erro e adequação ao público. Propor texto específico quando fundamentado. |
| 13 | Consistência e arquitetura | Padrões reais do projeto, componentes equivalentes com comportamentos diferentes, duplicação, acoplamento, estados e dependências que afetem confiabilidade/manutenção. Refatoração exige benefício demonstrado. |
| 14 | Cético, segunda fase | Após primeiras conclusões: contestar evidência/caminho ativo/contrato/fixture, severidade e subjetividade; identificar duplicatas e cobertura faltante. Preservar achado único válido e divergência fundamentada. |
| 15 | Caos, carga e resiliência | Estática primeiro; depois falhas/retry/idempotência/concorrência/recuperação no ambiente permitido. Medir p50/p95/p99, erros, vazão e recursos quando possível; registrar duração, concorrência e volume. Sem carga em terceiros/produção sem autorização específica. |
| 16 | Uso operacional real | Partir da tarefa e botão esperado: clique → HTTP → persistência → integração/planilha/provedor → estado final na UI. Verificar fronteiras e correlação; distinguir aceito, enfileirado, gravado, enviado, entregue e lido. |

## Personas de uso

Uma especialidade indica o que o auditor examina; uma persona representa um contexto concreto de uso, não uma profissão de auditor. Defina objetivo/tarefa, conhecimento prévio, limitações pertinentes e critério observável de sucesso. Selecione os contextos que esclarecem a dúvida ou risco do alvo, sem catálogo de personagens, quota ou rodada adicional obrigatória em toda auditoria. Um mesmo peixinho pode cobrir uma especialidade e uma persona, mantendo explícitos os dois papéis.

Quando viável, dê à persona a tarefa, o contexto e o acesso seguro para tentar pela interface, sem explicação da implementação e antes de ler código. O auditor técnico continua livre para inspecionar implementação e contratos. Se o agente já conhece a implementação ou precisa de assistência, registre esse conhecimento, a ajuda recebida e a limitação da prova; não apresente essa tentativa como descoberta sem orientação. Acesso, autorização e segurança prevalecem sobre a simulação.

Registre conclusão total/parcial ou interrupção, ajuda solicitada/recebida, erros e recuperação efetivamente observados. Separe essas observações de hipóteses sobre a causa, generalizações e gosto pessoal. Declare que a prova foi feita por agente em um contexto de uso; não invente emoções, depoimentos ou participantes humanos.

Trate também regionalização, datas/horários/moeda/arredondamento, persistência de preferências, tempo real, rastreabilidade, origem/frescor e retomada quando aplicáveis. Distribua entre esses perfis; acrescente especialista somente para lacuna real. N/A exige razão ligada ao alvo, não ferramenta indisponível: nesse caso registre não verificado.
