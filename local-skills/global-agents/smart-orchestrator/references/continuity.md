# Continuidade do Smart

O controller V2 e o execution-plan continuam autoritativos. Cada gravação publica um índice imutável em `<state-root>/checkpoints/<sha256>.json`, seguido de `latest.json`, com as mesmas travas, flush/fsync e replace do estado. `init` repetido e `status` reparam publicação interrompida. Se a publicação falhar após gravar estado, o comando falha e o estado já gravado permanece: consultar `status` antes de repetir qualquer mutação. Não apagar histórico para reparar um índice.

Os índices incluem execução/owner, feature, referências ao plano/SPEC/contratos/critérios e regras da skill instalada, estágios/dependências/responsáveis, fingerprints das provas, leases e Git (HEAD/branch/status; null fora de Git). Decisões, achados, tentativas e logs são referenciados nos registros originais. `run_id` identifica o chat quando disponível; `execution_id` é o owner persistente do controller. Conteúdo idêntico reutiliza o arquivo; novos estados preservam versões anteriores. O índice não contém documentos ou logs completos nem concede aceite.

Com os argumentos normais `--plan`, `--root`, `--state-root` e `--resources-root`:

- `controller.py ... checkpoint`: validar/publicar índice atual; uso diagnóstico, sem administração manual habitual.
- `controller.py ... recover`: conferir plano e root, recalcular gates e aceites contra arquivos reais e devolver fila atual. Não restaura estado antigo nem aceita tickets; provas inválidas retornam pendentes. Provas válidas e aceites atuais dispensam repetição.
- `controller.py ... status --summary`: consultar estado e eventos; `schedule` mostra elegibilidade e disponibilidade de recursos.

Checkpoints permanecem locais à execução, sem registro global por chat.

## Retomada e operações pendentes

A compactação pertence ao runtime nativo. O Smart não define thresholds de contexto, dispara compactação nem cria ou troca chats para contorná-la. Após compactação ou interrupção, retome o plano e o mesmo estado local com `recover`; confira operações em andamento e recursos reservados antes de novos despachos. Preserve as regras de modelo em [Delegação](../SKILL.md#delegação).

O controlador conserva `context-begin --operation-id ID` e `context-end --operation-id ID` como proteção local explícita de uma fronteira de contexto. `context-begin` exige ausência de estágios críticos ativos e de recursos reservados pelo owner; enquanto a operação estiver pendente, mutações ficam bloqueadas. Esses comandos não executam compactação.

Se houver `context_operation` persistida, consulte `status`, confirme que a operação responsável terminou ou parou e use `context-end` com o ID exato antes de retomar. Nunca libere por idade nem apague estado para contornar a proteção. Plano alterado, índice corrompido ou fontes ausentes exigem reconciliação explícita; nenhum checkpoint restaura automaticamente o controller.

Reservas protegem apenas participantes cooperantes; ferramentas externas podem usar o mesmo recurso. Mantenha ownership, permissões, revisão independente e todos os gates de qualidade. Retomada ou checkpoint não transforma provas ausentes, inválidas ou FAIL em PASS.
