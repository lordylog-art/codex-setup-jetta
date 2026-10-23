# Design Guardian

Use Nosso Design instalado e somente a referência da família afetada. Impeccable entra quando houver decisão visual relevante; Harness desativado não é dependência. Reutilize prova visual válida entre especialistas. Decisão de identidade segue contratos e Nosso Design; não copiar design system genérico nem fonte/token de outro produto.

## Descobrir a referência

No checkout atual, localizar PRODUCT/DESIGN, CSS/cascata/overrides, componente canônico e tela da mesma família/cliente/unidade. Inventário gerado e screenshot não são aprovação. Contratos explícitos > composição aprovada/skill > componente/estilos atuais > referência válida e precedentes da família. Se fontes divergirem, registrar conflito; não normalizar legado fora do escopo.

Referência deve informar caminho/revisão/hash, aprovação, rota/story, estado, fixture, tema, viewport/DPR/zoom, navegador/SO e fontes carregadas. Recuse como baseline operacional captura de login, link expirado, redirect, erro ou spinner. A spec registrou `guarulhos__disponibilidade.png` como link inválido: só serve para aquele estado de erro, não disponibilidade.

Descobrir paleta/cores de estado, Aptos/fallbacks carregados, peso/tamanho/hierarquia, espaços, raio/borda/sombra, campos/botões, densidade, modais/tabelas/dashboards, topbar/sidebar, ícones/logos reais e vazio/loading/erro/sucesso/desabilitado. Confirmar mobile/dark existentes. Raios maiores de família não viram regra global. Dashboard novo segue kit `@/components/dashboard`, `.jetta-dashboard`, prefixo `jetta:` se contrato atual mantiver; não migrar antigo por conveniência.

## Inspeção focal por padrão

Para aparência alterada, reuse o componente/preview e inspecione o estado pertinente. Automação headless pode produzir captura e verificar geometria, foco e overflow. Abra navegador interativo apenas para observar pixels ou lacuna que a automação não resolva. Não execute o percurso funcional completo de ERP para chegar ao visual; reuse estado/fixture direta quando legítima. Outro viewport/tema só quando afetado ou solicitado. Não invente aprovação humana ou baseline obrigatório para reaplicar componente aprovado.

Os três mecanismos e métricas abaixo são recursos para regressão visual ou auditoria quando necessários; não são uma bateria obrigatória em toda mudança.

## Mecanismos disponíveis

1. **Determinístico:** classes/tokens e valor resolvido no componente/tema correto; retângulos, gap/padding, foco/labels/erro, scroll, ações alcançáveis e conteúdo. Código estático não comprova cascata runtime. Sobreposição de retângulos pode ser intencional; confirmar oclusão/perda.
2. **Screenshot:** referência/atual/diff com ambiente e conteúdo controlados; estabilizar dados, fontes e animação. Mascarar somente dinâmico autorizado, registrando seletor/área, sem ocultar alvo, erro ou valor de negócio. Sem baseline aprovado, produzir comparação para revisão, não aprovação automática de pixels.
3. **Semântico:** se ferramenta inspeciona pixels, abrir imagens relevantes e registrar ferramenta/imagens/observação ligada ao análogo. Verificar hierarquia, agrupamento, densidade, alinhamento e coerência. Sem visão registrar `semanticVisual=NOT_RUN`; criar screenshot ou ler DOM não é inspeção de pixels.

Preferir Storybook para componente isolável quando reproduz contexto. Rota ERP real quando provider/auth/navegação/cascata integrada ou critério exigir. Manifest do Storybook não prova preview funcionando; validar compatibilidade sem instalar/atualizar plugin.

## Métricas e classificação

| Medida | Unidade e limite |
|---|---|
| Tokens | divergentes/comparáveis, mais cada propriedade; cor fixa equivalente e token correto são fatos diferentes |
| Cor | RGBA/fundo; ΔE00 só com conversão Lab/biblioteca válida e parâmetros documentados |
| Fonte | família/peso categóricos, tamanho/entrelinha em CSS px; confirmar fallback real |
| Geometria | diferença absoluta de dimensões/gaps/raios/padding em CSS px, considerando transform/zoom |
| Overflow/corte | scrollWidth−clientWidth e região; scroll interno previsto não é overflow indevido da página |
| Screenshot | pixels divergentes/comparados, threshold/limite documentados, área mascarada separada |
| Responsividade | ação/conteúdo acessível em estado/viewport; largura da falha, scroll e expectativa |
| Componentes | regras satisfeitas/aplicáveis e violações individualizadas; média não dilui bloqueador |

Calibrar tolerâncias com repetição sem mudança no mesmo ambiente, pares sem regressão e divergências rotuladas pelo responsável. Sem medição, N/A. Não há threshold universal de estética ou garantia percentual de qualidade.

Classificar: erro funcional visual; violação objetiva da família/design system; possível inconsistência estética; mudança intencional sem aprovação. Achado inclui regra, componente/estado/viewport/tema, referência/aprovação, atual/diff, métricas e consequência. Suspeita estética sem contrato não vira bug confirmado. Mudança de identidade que exige aprovação mantém obrigação pendente. Baseline só muda com decisão explícita revisada; Guardian/Healer preservam original e diff.

Exemplo de controle: modal continua salvando, mas usa decoração roxa, espaçamento hero e shell alheio ao SAC. Função pode passar; regra objetiva da família pode reprovar. Separar os dois resultados e sustentar com código/estilo/capturas. Não tratar esse exemplo hipotético como defeito atual. Mais casos: seção 14 da spec.
