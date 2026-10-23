# Escalonamento: DAG, CPM, RCPSP e filas

## Dependências por etapa

Modele arestas `origem/etapa -> destino/etapa`, com tipo/condição verificável:

| Tipo | Liberação |
|---|---|
| Contrato | Interface congelada/disponível; implementação da origem pode continuar. |
| Implementação | Código necessário disponível no candidato/base compatível. |
| Validação | Prova específica válida para critério dependente. |
| Integração | Componente aprovado efetivamente integrado na base exigida. |

Integração bloqueia integrar, não implementação independente sobre contrato estável. Confira referências ausentes, ciclos e conflitos antes de delegar. Corrija modelagem ou peça decisão real; nunca remova dependência obrigatória para liberar trabalho. Bloqueie fatia dependente; ramos independentes podem prosseguir.

## Caminho crítico

Em ordem topológica reversa:
`CP(i) = d(i) + max(CP(j) para sucessores j)`; terminal: `CP(i) = d(i)`.

`d(i)` cobre implementação, validação, correção esperada e integração **restantes**. Com medições confiáveis:
`E[d(i)] = t_impl + t_val + t_int + P(rework) * E[t_rework | rework]`.

Não invente durações/probabilidades. Sem dados, registre faixas com origem/hipóteses; sem faixa defensável, marque desconhecido e obtenha prova curta antes de anunciar CP numérico. Propague extremos sem chamá-los de intervalo estatístico de confiança.

Para paralelismo entre etapas/dependências que liberam cedo, expanda tickets em nós de etapas. Agregação no ticket pode bloquear trabalho e superestimar caminho: trate esse CP como heurística, não limite inferior comprovado. Use trabalho restante de nós ativos, excluindo duração consumida/concluída.

Priorize ações elegíveis que encurtem maior caminho real; número de dependentes é auxiliar. Empates: liberação do gate dominante, menor contenção/retrabalho, depois ordem estável. Recalcule após mudança material de duração, dependências, estado/recursos.

## Capacidade e RCPSP

`N_ativos <= min(N_disponíveis, N_trabalhos_elegíveis, N_capacidade_recursos)`.

Respeite limite real da ferramenta, incluindo principal/agentes já ativos conforme sua semântica. Escalar é teto, não teste suficiente: para cada recurso r, soma das demandas concorrentes <= capacidade(r). Arquivos, navegador, banco/fixture, portas, runners e slot de integração têm reservas próprias. Exclusivo tem capacidade 1; libere só após conclusão/cancelamento confirmado.

Considere CPU, memória, revisão e coordenação. Novo agente deve reduzir conclusão estimada mais do que overhead, conflitos e fila adicionados. Sem benefício plausível, mantenha execução atual. Sem medições, comece conservador, observe conclusão e amplie com trabalhos independentes/validação suficiente. Reduza quando contenção/fila inverter ganho; sem número universal.

Com unidades/premissas compatíveis:
`LB = max(CP_restante, trabalho_total_restante / capacidade_efetiva, max_r(carga_restante_r / capacidade_r))`.

Trabalho/capacidade usam unidades compatíveis (agente-minuto/agentes equivalentes); carga exclusiva inclui só ocupação. CP válido usa precedência real de etapas. Gate obrigatório indisponível sem previsão impede prazo finito defensável; capacidade 0 não é infinita. LB é condicionado a durações/premissas, não previsão nem ótimo. Se CP/recurso exclusivo dominar, agentes extras têm pouco potencial nesse trecho.

## Validação e WIP

Mesma janela: `λ` candidatos prontos/hora; `μ` capacidade de validação/hora; `ρ=λ/μ` quando μ>0. Aceites dependem também de reprovação/correção. Sem medições, desconhecido; zero aceites sozinho não prova μ=0. Gate comprovadamente indisponível implica capacidade operacional 0.

Se λ>=μ sustentadamente, estoque tende a crescer. Limite WIP por capacidade observada/tolerância de espera do projeto (ex.: capacidade * janela tolerada), com trabalho ativo justificável. Hipótese recalibrável, não quota arbitrária. Idade de abertos detecta espera; médias de lead time usam concluídos.

Com μ=0: suspenda expansão desnecessária do estoque, recupere gate, realoque para revisão estática/diagnóstico/contratos ou trabalho independente útil, preserve candidatos/provas válidas. Retome implementação gradualmente ao recuperar capacidade. Bloqueado não é aceito.

Lei de Little `L=λ*W` só em sistema aproximadamente estável, mesma fronteira/janela, conservação do fluxo e médias compatíveis. Fila crescendo/gate parado: contagem, idade/tendência; não derive prazo por Little.
