---
name: speckit-orquestrador
description: Orquestra features do ERP Jetta com o menor fluxo Spec Kit compatível com o risco.
---

# Spec Kit Orquestrador

Leia `AGENTS.md` e `.specify/memory/constitution.md`. Não repita suas regras nem crie artefatos sem uso.

## Escolha do modo

- **Direto:** bug isolado ou mudança já especificada; investigar o ponto, alterar e validar proporcionalmente.
- **Enxuto:** mais de uma superfície, requisito incompleto ou risco moderado; usar `specify`/`clarify`, investigação focal, plano e tasks curtas somente se ajudarem a execução.
- **Completo:** feature, integração, dados, permissão, UI nova/relevante, deploy, ou pedido explícito do usuário; executar as fases abaixo.

Informe o modo e o motivo em uma frase. Suba de modo apenas quando a evidência revelar risco adicional.

## Fluxo completo

1. Confirmar objetivo, escopo, usuários/unidade, comportamento preservado, aceite e efeitos externos. Perguntar somente decisões materiais pendentes (máximo cinco).
2. Investigar precedentes, contratos e superfícies citadas. Use `investigar-detalhes` para rota/tela/fluxo referenciado. Para UI, inclua a referência visual aplicável.
3. Criar ou atualizar `spec.md`, `plan.md` e `tasks.md` com decisões, impactos aplicáveis, dependências, arquivos prováveis e validação. Domínios não aplicáveis recebem apenas uma justificativa curta.
4. Executar uma task por vez. Validar o nível mínimo que cubra o risco; revisar segurança, UI/UX, contrato ou deploy apenas quando afetados.
5. Fechar com evidências reais, pendências, validações não executadas e riscos.

## Artefatos e ClickUp

Use os três artefatos padrão. Crie log, checkpoint ou matriz extra somente para retomada, operação externa ou auditoria exigida. Ative ClickUp apenas se o usuário o indicar como referência principal ou pedir sincronização; antes de mutar, consulte os IDs/estado reais e registre apenas os vínculos necessários.

## Delegação e custo

Delegue formatação, extração e checagens mecânicas a modelo econômico disponível; decisões, investigação, arquitetura, implementação e aceite ficam com o modelo principal. Não trocar modelo ou degradar validação silenciosamente. Evite reler arquivos inteiros e use contexto progressivo.

## Paradas obrigatórias

Pare para os gates humanos da Constituição e para conflito entre requisito, evidência e código. Não invente contratos, IDs, payloads, estados remotos ou resultados de validação.
