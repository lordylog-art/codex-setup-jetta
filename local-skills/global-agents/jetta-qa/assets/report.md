# QA — {{ticketId}} / {{runId}}

**Parecer:** {{PASS | FAIL | BLOCKED | INCONCLUSIVE}}
**Recomendação:** {{HOLD | ELIGIBLE_FOR_REVIEW}} — não autoriza publicação.

Checkout/base/HEAD/delta local: {{proveniência e hashes}}
Contrato e escopo: {{fontes, requisitos, arquivos/módulos e consumidores}}
Ambiente/conteúdo servido/fixtures: {{identidade sem segredos}}
Modo/personas: {{modo e estratégias realmente aplicadas}}
Orçamento: {{parede, worker-minutos, tokens medidos ou não medidos}}

| Indicador | Resultado e denominador | Limites |
|---|---|---|
| Cenários únicos / tentativas / ignorados | {{contagens por outcome}} | {{não executados}} |
| Requisitos / aprovação / risco | {{verificados/aplicáveis; C_R}} | {{simulado versus real}} |
| Interações 2-way / 3-way | {{atingidas/válidas; versão do modelo}} | {{planejado versus observado}} |
| Invariantes / flake | {{verificadas/aplicáveis; divergentes/repetidos}} | {{amostra ou N/A}} |

## Defeitos confirmados

Por achado: ID, P0–P3, fonte/regra, pré-condições/IDs sintéticos, seed, passos mínimos, esperado/observado, evidências e mecanismo realmente exercitado. Diferencie defeito de regressão comprovada por base anterior.

## Visual, acessibilidade e segurança

{{Achados e provas por categoria, referência/atual/diff, visão executada ou NOT_RUN, critérios WCAG, matriz de acesso e lacunas. Sem duplicar bugs comuns às categorias.}}

## Suspeitas, hipóteses e recomendações

{{Separar de fatos provados; causa desconhecida permanece desconhecida.}}

## Pendências

{{Obrigação/cenário não executado, motivo, impacto, decisão de negócio ou dependência, dono/próximo passo. Dispensa preserva FAIL e fonte da decisão.}}

Limpeza/artefatos: {{fixtures removidas ou pendentes, destinos privados/sanitizados}}
Prova reutilizada/invalidada: {{conteúdo e equivalência}}
Correções sugeridas/regressões: {{encaminhamento ao executor autorizado, sem alterar regra automaticamente}}
