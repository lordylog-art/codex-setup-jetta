# Regras do ERP Jetta

Herde as preferências globais; este arquivo contém apenas exceções do projeto. A Constituição governa o Spec Kit e as skills não devem repeti-la.

- Em produção, sem autorização explícita para ação e alvo, faça somente diagnóstico read-only. Nunca pare, reinicie, recarregue, apague, recrie ou substitua serviços/processos.
- Trabalhe em `main`. Antes de uma operação Git autorizada, revise o diff e não versione dumps fora de migrations Prisma, `.env`, logs, exports, backups, credenciais ou dados reais.
- Preserve fluxos do ERP fora do escopo. Não introduza fallback silencioso, retorno vazio, mock mascarador ou limite/retry/cache/paginação sem requisito explícito.
- Prefira SQL-first, agregação no servidor, batching e padrões existentes. Para e-mail, use exclusivamente a fila global; não chame `SmtpService` fora dela nem crie retry paralelo.
- Se build, runtime, Prisma, configuração, entrypoint, porta, health check ou release forem afetados, revise a compatibilidade com `NewDeploy.ps1`; isso não autoriza deploy/restart.
- Horários operacionais usam `America/Sao_Paulo`; trate `TIMESTAMP` sem fuso conforme a convenção do domínio.
- Valide somente quando o usuário pedir, o risco exigir ou houver indício de arquivo/import/sintaxe quebrado; declare a lacuna. Para código compartilhado, contrato, permissão, cálculo, data, cache ou integração, avalie regressão relacionada.
- Para reconhecimento, leitura de dados e testes do ERP, use subagente quando disponível. Subagentes não alteram arquivos nem executam operações externas; evite dois testes concorrentes que usem o mesmo banco, porta ou artefato.

## Roteamento Spec Kit

- Direto: ajuste pontual, bug isolado ou task já especificada.
- Enxuto: mais de uma superfície ou requisito incompleto.
- Completo: feature, integração, dados, permissão, UI nova/relevante, deploy ou pedido explícito.

Na entrega, informe arquivos, mudança, validação real, lacunas e riscos.
