---
name: speckit-analyze
description: Faz uma análise curta de consistência entre artefatos Spec Kit.
---

# Spec Kit Analyze

Leia `spec.md`, `plan.md` e `tasks.md` apenas se existirem. Compare objetivo, requisitos, decisões, dependências, tarefas e validação.

Reporte apenas falhas acionáveis: requisito sem task, task sem aceite, contrato contraditório, dependência ausente, risco não tratado ou validação incompatível. Classifique em bloqueador, importante ou observação; cite arquivo/seção e correção mínima.

Não reescreva artefatos, não gere relatório separado e não invente lacunas. Se não houver achados, declare isso em poucas linhas.
