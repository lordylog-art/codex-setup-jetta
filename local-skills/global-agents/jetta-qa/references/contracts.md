# Contratos de execução e prova

## Aplicabilidade: auditoria formal solicitada

As exigências de manifesto, ledger, pacote, hashing e schema abaixo aplicam-se somente quando o usuário pedir auditoria estruturada ou quando um artefato já em uso precisar desse formato. No QA direto, use o registro do ticket e testes automatizados conforme SKILL.md. O Harness desativado e seus scripts de despacho não são pré-requisitos; delegação usa ferramentas nativas autorizadas. Helpers de manifesto são opcionais, não gates de toda implementação.

Somente em auditoria formal com esse formato ativo, o pacote de despacho pode usar `scripts/dispatch.py --ledger <ledger-compartilhado> --packet <pacote.json>`; se depender do Harness desativado, use despacho nativo e conserve os dados pertinentes no registro existente. O pacote declara qa_mode (Quick/Standard/Deep) e verification=true; o executor segue a política central por etapa. Medições/capturas determinísticas usam ferramentas; julgamento semântico de pixels recebe capacidade pertinente. O modo e as fontes/gates deste contrato permanecem obrigatórios. A auditoria do runtime é separada do veredito funcional.

## Plano e atribuições

Antes da execução, registre no destino privado escolhido: schemaVersion=1, runId/ticketId, raiz/base/HEAD e hashes de conteúdo local, fonte/versão do contrato, arquivos e consumidores, requisitos/obrigações, mapa de dependências, risco, cenários/personas, fatores/restrições, orçamento, capacidades, identidade do ambiente/fixture e autorização. Não criar tracker paralelo: use o registro do ticket/workflow existente; manifesto é artefato de prova.

Cada cenário precisa pré-condições, fixture/ator/escopo, passos (seed quando gerado), oráculo com fonte, fronteira exigida, assert relevante, evidências esperadas, custo e limpeza. ID estável/versionado; alternativa de teste para a mesma obrigação só é equivalente após revisão semântica. Requisito composto tem todas as obrigações necessárias; sem oráculo aprovado, mantenha pendente. As fontes históricas/exemplos na spec são mapa de investigação, não regras imutáveis do produto.

Root é único escritor do plano/resultado consolidado. Lote delegado recebe assignmentId, cenários/oráculos congelados, resources/fixtures com dono, pasta exclusiva, limites e condição de parada. Dois filhos no máximo por padrão, menos se o host/recurso exigir. Concorrência de negócio usa dois contextos próprios sobre um objeto compartilhado deliberado, com barreiras/timeline. Sem essa condição, serializar disputa de fixtures/sessão/porta/banco.

Artefatos: `<artifactRoot>/<runId>/manifest.json`, plano e report; cada lote escreve `<assignmentId>/<scenarioId>/<attemptId>/...`. O manifesto fica na raiz **desse run**, e todos os caminhos de evidência são relativos a ela. Root consolida cópias sanitizadas/refs, preservando originais privados e hashes. Não versionar traces/sessões brutos nem arquivos com dados pessoais. Extensões JSON podem carregar detalhes do contexto; schemaVersion desconhecida exige migração explícita.

## Helpers locais — sem acesso ao ERP

Requerem apenas Node.js, sem npm install, browser, rede ou dependência nova. Eles leem entradas/artefatos e escrevem JSON no stdout; não iniciam testes, geram código de produto, modificam baseline ou fazem limpeza. Caminho `<skill>` é a pasta desta skill.

```powershell
node <skill>/scripts/plan.mjs risk 4 3 3 3
node <skill>/scripts/plan.mjs cover model.json
node <skill>/scripts/plan.mjs measure model.json rows.json
node <skill>/scripts/plan.mjs rank candidates.json 9
node <skill>/scripts/validate-run.mjs manifest.json
```

`risk`: I/P/E/C inteiros 0–4, sem default silencioso para desconhecido; devolve `{risk:83.75}` no exemplo. Use 3 provisório apenas com indicação no plano.

`cover/measure`: modelo JSON com `schemaVersion:1`, `factors` objeto de arrays não vazios com valores primitivos únicos (string/número finito/booleano), `strength` 2 ou 3 e `forbidden` opcional. Cada item forbidden é uma conjunção proibida; array é disjunção. `{}` proíbe tudo e gera erro de modelo insatisfatível. Representar implicação por conjunções proibidas; nunca executar expressão JS vinda do modelo. Modelo e regra só podem referir fator/valor existente.

```json
{
  "schemaVersion": 1,
  "factors": { "A": [0, 1], "B": [0, 1], "C": [0, 1] },
  "strength": 2,
  "forbidden": [{ "A": 1, "B": 1 }]
}
```

Gerador greedy é determinístico por ordem de fatores/valores, sem aleatoriedade: guarda versão do algoritmo e hash do modelo; não promete mínimo global. Limites locais: 2–12 fatores, até 20 mil atribuições cartesianas, 100 mil ocorrências de tuplas e 10 milhões de avaliações de tupla durante geração. Acima, dividir modelo sem perder interações críticas ou usar ACTS autorizado; nunca truncar e alegar cobertura total. Para força variável, rodar 2-way global e 3-way em submodelo de fatores críticos, unir linhas estendidas validamente e medir cada modelo separado. Helper não faz essa extensão automaticamente.

`measure` aceita arquivo com array de linhas completas ou objeto retornado por `cover`. Mede as tuplas válidas por grupo independentemente da seleção greedy; aceita linhas repetidas sem inflar cobertura e rejeita linha inválida. Tupla válida tem extensão a uma atribuição completa possível. Resultado `{covered,total,ratio}` é cobertura do conjunto informado, não prova de execução. Só chamar com linhas observadas quando houve aplicação dos fatores até o oráculo; reportar planejado/observado separadamente.

`rank` aceita array de candidatos com `scenarioId`, `eligible` booleano, `mandatoryReasons` array, `impact` 0–4, `R` 0–100, `G/N/H/U/A/D` 0–1 e `T>0` worker-minutos. Campos/fronteiras/oráculos vêm do plano, não do helper. `selected/deferred/remainingMinutes/mandatoryFeasible` são propostas para o próximo lote; se obrigatório inelegível ou custo total inviável, `mandatoryFeasible=false` e extras ficam deferred. Obrigatórios elegíveis que cabem ainda podem compor lote parcial, sem aprovar o plano completo. Recalcular após cada lote; não interpretar selecionados como cenários já executados nem como cobertura completa. Não adicionar extras que invadam a reserva de triagem/relatório.

CLI: saída 2 para entrada inválida/erro; `validate-run` retorna 0 apenas para PASS estrutural, 1 para FAIL/BLOCKED/INCONCLUSIVE, 2 para manifesto inválido. Revisor do root decide suficiência, não o exit code isolado.

## Manifesto mínimo de consolidação v1

`validate-run` valida o **formato de consolidação** abaixo. Plano completo/assignment têm campos adicionais de preparação citados acima; o helper não os inventa nem confirma autorização/semântica. Não monte manifesto “verde” para substituir execução real. Antes de aprovar, root deve confirmar completude do inventário de obrigações e revisar provas e `modeReview`.

| Campo | Obrigatório |
|---|---|
| Identidade | schemaVersion=1; runId/ticketId strings não vazias; mode Quick/Standard/Deep |
| fingerprint | baseSha/headSha SHA Git de 40 hex; localDeltaHash/contractHash/servedContentHash/environmentHash SHA-256 de 64 hex; usar os mesmos campos em cada tentativa |
| environment | authorizationRef/isolationRef não vazios; syntheticDataOnly=true; externalEffectsDisabled=true. Ref aponta à prova/registro revisado, não declaração suficiente de isolamento |
| modeReview | reviewer/rationale não vazios; satisfied booleano. Falso impede PASS; declarar que critérios do modo foram cumpridos exige revisão, não conveniência |
| requirements[] | requirementId único; risk 0–100; obligations[] não vazio com obligationId globalmente único, mandatory booleano e requiredBoundary congelada |
| scenarios[] | scenarioId único; obligationIds conhecidos/únicos; persona A–H; oracle.source/expected; requiredBoundary; notRunReason null/ausente ou motivo de dependência específica |
| attempts[] | executionId único; scenarioId; attempt ordinal 1–3; fingerprint; outcome; failureClass; boundary; assertions[]; evidenceIds[]; startedAt/endedAt ISO com ordem válida |
| evidence[] | evidenceId único; executionId/runId correspondentes; path relativo e arquivo regular dentro da raiz física do run; sha256; sanitized=true; mechanism igual à boundary da tentativa |
| findings[] | findingId único; confirmed booleano; executionId e evidenceIds relacionados. Confirmado exige severity P0–P3, expected/observed e reproduction[] não vazios; tentativa FAIL/PRODUCT correspondente |

Boundaries reconhecidas, sem hierarquia automática: `static`, `component`, `browser-mocked-api`, `real-browser`, `real-http`, `real-http-and-database`, `real-browser-http-and-database`, `external-integration`. A fronteira exigida pertence à obrigação do contrato; cenário alternativo não pode rebaixá-la. Cada cenário tem a mesma requiredBoundary das obrigações vinculadas; se exigirem fronteiras diferentes, dividir o cenário/registro. Necessidade e mecanismo devem coincidir explicitamente; rejeitar prova real por erro de classificação é mais seguro que transformar simulação em real. Se precisar nova combinação, estender contrato/teste deliberadamente. O rótulo não prova o mecanismo: revisar artefato e configuração do teste.

Outcomes: PASS/FAIL/BLOCKED/INCONCLUSIVE. failureClass: NONE/PRODUCT/TEST/ENVIRONMENT/ORACLE_UNKNOWN. PASS exige NONE, assert e evidência; FAIL exige classificação. FAIL/PRODUCT exige finding confirmado reproduzível. FAIL de teste não é defeito de produto e fica inconclusivo até diagnóstico. Ausência de tentativa com dependência explícita → BLOCKED; ausência sem causa específica (oráculo/tempo) → INCONCLUSIVE.

Um cenário após divergência só usa PASS com `instabilityReview:{reviewer,rationale,evidenceIds}` ligada à história do cenário. Primeira falha fica preservada; até duas novas tentativas. Defeito PRODUCT confirmado no mesmo conteúdo mantém FAIL, mesmo que passe depois; correção muda conteúdo/fingerprint e inicia nova consolidação, vinculada ao histórico, não apaga falha anterior. Prova de fronteira insuficiente não contribui para cobertura exigida, mesmo com defeito confirmado nessa fronteira mais estreita.

Hash de ambiente deve identificar configuração relevante, fixture/relógio, versões e fonte servida sem secrets; não usar digest de credencial como substituto. Conteúdo local/hashes mudados invalidam prova dependente. O helper exige igualdade exata do fingerprint; reuso parcial entre runs precisa ser revisado e explicitamente reatribuído ao novo manifesto com origem preservada, nunca só trocar rótulo.

Evidência é arquivo regular: caminho absoluto, traversal, symlink/junction que escapa, hash divergente e vínculo a outro run/execução são rejeitados. O arquivo pode continuar ser uma prova ruim semanticamente; root verifica nó/assert/oráculo/reprodução e sanitização. `evidenceIds` conclusivos não podem estar vazios.

## Métricas, resultado e severidade

Obrigação pode ter cenários alternativos semanticamente equivalentes; uma prova válida basta, mas defeito confirmado prevalece. Requisito é verificado somente se **todas** suas obrigações têm prova válida PASS/FAIL na fronteira necessária. `C_R=Σ(R×V)/ΣR`, V binário: reprovação conclusiva cobre, bloqueio/inconclusão não; denominador zero é null/N/A. Requisitos aprovados e verificados têm contagens separadas. Cenários/personas/tentativas não multiplicam requisitos/bugs. Flake usa divergentes/repetidos comparáveis, nunca todos os testes sem amostra; tempo em parede e worker-minutos; regressão precisa prova anterior.

FAIL por bug confirmado; sem FAIL, BLOCKED por obrigatório com dependência; depois INCONCLUSIVE por obrigatório sem prova, execução inconclusiva, nenhum requisito efetivamente verificado ou critérios do modo pendentes; PASS somente após tudo obrigatório e modo satisfeitos. Extras não executados são lacuna explícita e não precisam impedir PASS do recorte. HOLD para não PASS, ELIGIBLE_FOR_REVIEW para PASS. Sem autorização de CI/publicação.

P0: exposição/perda/corrupção/irreversibilidade grave; P1: autorização/integridade/fluxo crítico comprometido; ambos bloqueiam sempre. P2: defeito material limitado; P3: defeito menor. Todos os bugs confirmados do recorte produzem FAIL técnico. Dispensa P2/P3 por responsável fica separada com fonte/validade; não renomeia FAIL para PASS. Suspeita sem prova é hipótese, não bug confirmado.

## Aprendizado

Registro sanitizado no tracker/registro existente, ou `docs/quality/regressions` apenas se não houver equivalente: bugId, falha original, causa identificada/desconhecida, reprodução mínima e seed, teste detector, regra/revisão, módulos/consumidores, commit/data da resolução quando houver e recorrência. Executor autorizado adiciona regressão permanente à suíte existente e demonstra detecção antes/depois; deduplicar casos equivalentes. Não editar memória pessoal automaticamente.

Histórico compatível calibra custo, seleção, pesos e tolerâncias, versionando política e preservando avaliação fora da amostra de ajuste. Não altera regra de negócio, permissão ou baseline automaticamente. Templates e referências da skill substituem documentação duplicada; cenários históricos detalhados permanecem na spec aprovada.
