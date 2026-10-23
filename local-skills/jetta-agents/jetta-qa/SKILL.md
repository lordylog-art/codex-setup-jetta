---
name: jetta-qa
description: "Validate ERP Jetta implementations with risk-based local QA, personas, security, accessibility and Design Guardian. Documentation or skill authoring does not start ERP tests."
---

# Jetta QA

Avalie o recorte autorizado e devolva prova reproduzível. Uma única skill coordena o QA; personas são estratégias, não agentes permanentes. PASS vale para o recorte e as fronteiras demonstradas, sem autorizar publicação.


Antes de escolher executores ou iniciar QA, leia a [política compartilhada](C:/Scripts/Jetta Harness/WORKFLOW.md). Use `scripts/flow.py` dessa instalação para reservar orçamento e preparar despacho por etapa; qa_mode e model_profile são independentes. Preserve os gates abaixo.

## Preparar

1. Leia AGENTS/overrides aplicáveis. Receba ticket, critérios/decisões, checkout e base confiável; registre HEAD, staged/unstaged e arquivos novos pertencentes ao ticket, incluindo hashes. Preserve trabalho alheio. Mapeie UI → BFF → API/guards/DTOs → serviço/dados/jobs → consumidores afetados. Sem regra conhecida, registre pendência; código e teste não substituem decisão de negócio.
2. Confira código e ferramentas realmente disponíveis. A [spec aprovada](C:/Scripts/Jetta Harness/references/JETTA_QA_ADVERSARIAL_SPEC.md) registra fontes **históricas** em `ef5284edf`, não disponibilidade atual. Revalide caminhos, cliente/unidade, permissões e migrations no checkout alvo. Porta aberta, manifest ou teste existente não provam execução.
3. Leia [contratos](references/contracts.md) para congelar plano e evidências, e [estratégias](references/strategies.md) para risco, modo, personas e seleção. Use os helpers locais quando houver cálculo/cobertura ou consolidação estruturada; eles não acessam o ERP.
4. Antes de browser/API/mutação, leia [segurança e acessibilidade](references/safety.md). Reutilize ambiente e autenticação válidos conforme `../jetta-local-runtime/SKILL.md` e `C:/Scripts/Jetta Harness/references/qa-visual.md`, somente se necessários. Ausência de capacidade mantém a obrigação pendente. Não instale dependências, execute CI, envie mensagens ou publique por inferência.

## Executar e coordenar

5. Execute obrigatórios primeiro e extras por utilidade/custo. Reutilize testes relevantes antes de gerar cenários. Selecione runner/comando na configuração **atual**, sem hardcode de portas. Playwright Test é preferencial para browser/API reproduzíveis; ferramentas CLI/MCP/CUA são opcionais. Storybook prova componente isolado; não prova autenticação ou persistência.
6. Delegue lotes independentes somente quando autorizado e vantajoso: root mais até dois filhos por padrão, respeitando limites menores do host. Cada atribuição recebe cenários/oráculos congelados, recursos/fixtures, pasta exclusiva, orçamento e parada. Use subagentes nativos disponíveis, não novos chats do usuário. Root controla plano e parecer; executor testa; Design Guardian recebe UI pertinente; investigador/Healer só diante de falha. Sem subagentes, execute sequencialmente e declare ausência de revisão independente.
7. Para alteração de aparência ou UI integrada, leia [Design Guardian](references/visual.md), Nosso Design e Impeccable pertinentes. Confirme análogo/estado aprovado antes de comparar. Diferencie estilos/DOM, screenshot e inspeção real de pixels; visão sem ferramenta fica NOT_RUN.
8. Preserve primeira falha, seed, dados sintéticos, resposta e estado antes/depois. Classifique produto, teste, ambiente ou oráculo desconhecido. Limite reprodução a duas novas tentativas com hipótese/condição registrada; executor Luna tem teto mais estrito de uma tentativa inicial e um reparo, seguido de Sol, dentro do orçamento comum; nunca enfraqueça assert, ignore teste ou atualize baseline para obter verde. QA propõe correção; executor autorizado muda ERP e devolve delta para revalidação.

## Concluir

9. Use [template](assets/report.md) e matriz requisito → risco → obrigação → cenário → persona → execução → evidência. Valide os registros com `node <skill>/scripts/validate-run.mjs <manifest.json>` quando houver manifesto; valide também suficiência semântica. O helper verifica consistência, não se uma captura prova a regra.
10. Pare no aceite do recorte, limite de orçamento ou impedimento identificado. FAIL por defeito confirmado; sem FAIL, BLOCKED por dependência obrigatória; depois INCONCLUSIVE por prova/oráculo insuficiente; PASS só com critérios aplicáveis satisfeitos. Declare não executados, riscos, limpeza e próxima ação. Sem reset geral, correção do produto, commit/push/merge/deploy implícitos.

Para casos concretos, consulte a seção 14 da spec por módulo, sem carregar todo o documento por rotina. Para registrar regressão, siga [aprendizado](references/contracts.md#aprendizado). Respeite Implement/Code Review e o workflow V2 vigente; esta skill devolve evidência, não substitui o controlador de entrega.
