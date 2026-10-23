# Métricas e calibração

Use registro existente ou tabela no chat; instrumentação adicional exige benefício concreto. Eventos observáveis com timestamp/fuso, ticket/etapa, owner, candidato/recursos:

`started`, `codeReady`, `validationStarted`, `validationEnded`, `accepted`, `blocked`, `unblocked`.

Acrescente veredito, motivo de bloqueio, tentativas, hipótese/assinatura e retrabalho separando defeito de requisito alterado. Registre integração/liberação de recursos. Sem segredos; commit não é início real do trabalho.

| Métrica | Fronteira/cautela |
|---|---|
| Makespan | Início do objetivo até último aceite necessário; parcial não encerra. |
| Vazão | Tickets aceitos/hora na janela declarada; candidatos não contam. |
| Lead time | Entrada acordada do ticket até aceite. |
| Cycle time | Primeiro started até aceite, incluindo esperas. |
| Fila/WIP | Iniciados não aceitos/candidatos aguardando; fronteira/idade dos abertos. |
| Etapas | Tempos ativos de implementação, revisão/validação, correção/integração; esperas separadas. |
| Retrabalho | Tempo/custo por defeito separado de mudança de requisito. |
| Falha pós-aceite | Incidentes por entrega/janela; não observado não significa zero. |
| Tokens/recursos | Só quando expostos; desconhecido não é zero. |
| Bloqueios | Duração, etapa/impacto no CP; sobreposição não soma atraso automaticamente. |

Rotule fatos, estimativas, hipóteses, limites inferiores/resultados aprovados. Idade de aberto é censurada, não amostra concluída de lead time. Mediana/percentis pedem n, janela, método/amostra adequada à conclusão; poucos dados pedem valores/faixas. Gate sem recuperação prevista implica prazo desconhecido.

Calibre durações por etapa/família, probabilidade/custo de retrabalho, capacidade de validação, overhead, contenção, tolerância de espera/WIP e integração usando eventos reais. Atualize após mudanças materiais; não prometa estimativas. Ganho causal exige baseline comparável em escopo, risco, equipe/recursos/critérios; sem ele, associação. Linhas de código, commits/contagem de testes não substituem produtividade/qualidade global.
