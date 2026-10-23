# Estratégias, risco e orçamento

## Padrão: personas automatizadas e recorte focal

Escolha cenários pertinentes e implemente-os no runner existente: persona é fixture/ator/escopo e resultado esperado. Reuse testes válidos. Fluxo normal e regressões relevantes bastam para delta local; autorização/persistência exigem provas reais focalizadas dessas fronteiras, sem acionar auditoria completa automaticamente. Nenhuma persona obriga abrir ERP interativo.

As fórmulas, modos cronometrados, pairwise/3-way, quotas e matrizes abaixo são ferramentas opcionais para auditoria ampla solicitada. Seus mínimos não são gates do modo direto, e os tempos são tetos históricos, nunca duração a consumir. Não escale uma alteração focal de autorização para duas horas de QA só pelo nome do risco.

## Risco e obrigatórios

Por requisito: `R = 100 × (0,35I/4 + 0,25P/4 + 0,20E/4 + 0,20C/4)`, em pontos 0–100. I/P/E/C são ordinais inteiros 0–4: impacto, indício de defeito, exposição e complexidade. Zero exige evidência de ausência de consequência/alcance/mudança; 1 é local/estável/raro/simples; 2 intermediário; 3 impacto operacional/indício recente/uso diário/múltiplas camadas; 4 impacto grave/regressão conhecida/uso amplo/concorrência ou migração crítica. Informação ausente usa 3 provisório, explicitamente desconhecido. Pesos não são probabilidades.

Segurança, autorização, isolamento, integridade, efeito irreversível e critérios obrigatórios do ticket precedem ranking. Inclua positivos e negativos e a fronteira real exigida. Sem sandbox equivalente, obrigatório impedido permanece BLOCKED.

| Modo | Elegibilidade e mínimo | Limite inicial ajustável |
|---|---|---|
| Quick | R<40, delta local sem auth/persistência/concorrência/alcance amplo; fluxo normal, negativo/regressão relevante, UI/teclado focal se aplicável | 15 min; 1 filho; 20 mil tokens totais |
| Standard | Ticket funcional/formulário/consulta/UI; obrigatórios, personas pertinentes, estados e 2-way de fatores adequados; Guardian para UI | 45 min; 2 filhos; 60 mil tokens |
| Deep | R≥70 ou auth/isolamento/integridade/concorrência/migração/regressão crítica; 3-way focal, múltiplas sessões e consumidores | 120 min; 2 filhos; 120 mil tokens |

Descoberta de fronteira adicional escala Quick; gatilho crítico escala qualquer modo a Deep. Profundidade não aumenta orçamento autorizado. Reserve 60% execução, 25% diagnóstico, 15% relato; registre parede e worker-minutos separadamente. Tokens sem contador são não medidos. Ao faltar tempo, checkpoint e pendências; nunca amostrar fora obrigatório para declarar PASS.

## Personas mensuráveis

Cada cenário define estado/ator/escopo, ações, limites, oráculo/fonte, evidência e condição conclusiva. Conte cenários únicos, não aparições de personas. Estratégia foi bem executada quando produz conclusão sustentada, inclusive FAIL do produto; sem oráculo/ambiente é inconclusiva/bloqueada.

| Persona | Estratégia e condições iniciais | Ações/defeitos | Oráculo, evidência e medida |
|---|---|---|---|
| A experiente | Fixture elegível, ator autorizado; sequência operacional fixa | Filtrar/atribuir/trocar/voltar em sequência; procurar estado antigo, perda de seleção e associação errada; só atalhos implementados | Contrato + comando/resposta + leitura; trace/IDs; ações e transições verificadas |
| B iniciante | Preferências limpas, tarefa sem passos de clique, até 12 ações | Descobrir labels/ação/ajuda; ambiguidade e feedback ausente | Objetivo contratual, DOM/captura e decisões; atingiu tarefa ou obstáculo observável. Dificuldade humana inferida é hipótese |
| C desatento | Fixture exclusiva, saída externa bloqueada | Vazio/espaços/campo trocado, duas submissões, fechar/reabrir/interromper; duplicação, sucesso falso, validação/perda | DTO/regra + requests/contagem/estado antes/depois; clique duplo UI não prova idempotência HTTP |
| D caçador | Modelo e duas sessões próprias, seed/barreiras | Sequência proibida, cancelamento/reversão, limites e disputa; corrida/gravação parcial | Guardas/pós-condição aprovadas, timeline/seed e estado real; sem política concorrente, INCONCLUSIVE |
| E adversarial | Dois escopos/atores sintéticos autorizados | ID/body/query adulterados, sessão expirada, API direta; IDOR/exposição/efeito indevido | Matriz por recurso; resposta sanitizada + recurso preservado. 4xx de DTO não prova guarda |
| F acessibilidade | Estados carregado/modal/erro, teclado/axe/zoom reais disponíveis | Tab/Shift+Tab, nomes, foco, contraste/erro; barreiras assistivas | WCAG aplicável; axe/nós, ordem de foco, capturas/zoom. Tecnologia assistiva não disponível é pendência |
| G condições limitadas | Fixture isolada, perfil rede/viewport e duas abas conhecidos | Offline antes/depois da resposta, reconexão/expiração/reload; spinner/corte/reenvio | Contrato de recuperação + timeline e leitura após reconexão. Sem regra, não inventar resultado |
| H gestor | População, snapshot, timezone fixos | Cruzar módulos, filtros, agregação/exportação existente; total errado/recorte vazado | Cálculo independente da regra + IDs incluídos/excluídos + DTO; mesma população/instante |

A para normal; B quando descoberta/nomes mudam; C gravação; D estado/concorrência; E acesso/dados; F controles; G responsividade/recuperação; H consultas. Sem oito agentes ou todos os cenários em toda alteração.

## Combinações e estados

Fatores derivam do código atual: cliente/unidade/perfil/status/ação/dados/viewport/rede. Restrinja pares impossíveis como configuração positiva; mantenha entradas inválidas na suíte negativa. Limitação de massa é BLOCKED, não restrição de produto.

`scripts/plan.mjs cover model.json` gera array local limitado por enumeração; `measure model.json rows.json` mede independentemente tuplas estendíveis a atribuições válidas. Use 2-way base e 3-way nos fatores críticos; inclua casos direcionados de ordem maior. Força não é cobertura funcional. Modelo insatisfatível é erro, nunca 100% vazio. Relate array planejado e fatores realmente atingidos separadamente.

Modelo de estados por módulo: comando, guarda, estado anterior/posterior, persistência/efeitos e reload. Cubra permitidas, proibidas, reversões, duplicidade e disputa. Até 20 comandos Standard/60 Deep inicialmente, com seed, ordem e minimização do prefixo. Barreiras observáveis substituem sleeps. Estado não alcançado em busca limitada não é prova de impossibilidade.

Invariantes só viram exigência após fonte: escopo autorizado; recusa sem efeito indevido (auditoria legítima pode existir); sucesso UI só quando backend confirma; duplicidade apenas sob contrato idempotente. Propriedades/metamorfismos pertinentes: limites de texto após trim, data civil São Paulo/virada de dia, permutar filtros por interseção, manter chave de parada após reordenação. Não assumir monotonicidade de médias/percentuais ou snapshot que mudou. Reutilize biblioteca de propriedades instalada ou casos seedados simples; mutation testing só em sandbox autorizado e lógica isolável, sem remover guardas em produto compartilhado.

## Seleção adaptativa

Extras elegíveis têm oráculo conhecido e preparação possível. `S = (R/100) × (0,30G+0,20N+0,20H+0,15U+0,15A) × (1−D) / T`, índice heurístico/minuto. G ganho de obrigações/tuplas ainda não verificadas; N novidade (0/0,5/1); H `(bugs+1)/(execuções conclusivas+2)` em histórico compatível; U incerteza resolvível (0/0,5/1, falta de regra torna inelegível); A regressão relacionada (0/0,5/1); D redundância. Todos 0–1; T>0 em worker-minutos, com setup/coleta. R é maior risco realmente exercitado. Sem dados, registre estimativas; H inicial é 0,5. Não interpretar S como probabilidade.

Use `rank candidates.json minutos` como ordenação de lote, reservando obrigatórios primeiro; recalcule G/D e custos após cada lote. IDs diferentes/personas diferentes não justificam cenário redundante: deduplicar pré-condição+ações+pós-condição+fronteira+escopo. Helper não conhece a semântica dessa equivalência. Empate: maior impacto, menor custo, ID estável. Teto inviável mantém obrigatórios pendentes. Preserve primeira falha e até duas novas tentativas diagnósticas; retentativa aprovada não apaga flake nem falha real anterior.

Exemplos: R(4,3,3,3)=83,75; R(2,2,3,2)=55; R(4,3,3,4)=88,75. Pares de 000/011/101/110 cobrem 12/12 pares e 4/8 triplas. Cobertura de risco com 80/60 verificados e 20 bloqueado é 87,5%, mesmo com um FAIL. Calibrar pesos/tolerâncias com histórico versionado, avaliação temporal comparável, custo e defeitos escapados; manter overrides críticos. Detalhes e 18 cenários reais históricos: seções 8 e 14 da spec aprovada.
