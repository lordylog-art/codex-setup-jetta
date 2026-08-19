---
name: speckit-implement-clickup
description: Executa tarefas Spec Kit em sequência e sincroniza ClickUp somente quando aplicável.
---

# Spec Kit Implement

Leia a task atual, a spec/plano relevantes, `AGENTS.md` e a Constituição. Execute uma task por vez, com diff mínimo; não transforme task em refatoração.

Antes de editar, confirme arquivos, contratos e testes próximos. Valide no menor nível que cubra o comportamento alterado. Amplie para UI, integração, segurança, contrato, NewDeploy ou fluxo real apenas se a task afetar essa superfície ou o usuário pedir.

Se ClickUp estiver habilitado, atualize o item real somente após a validação e registre a evidência mínima. Não crie checklist, state, checkpoint ou log novo se o artefato existente já permitir retomada.

Pare para gates humanos, falha não explicada ou divergência de escopo. Ao fechar, informe resultado, arquivos, validação real, pendências e risco.
