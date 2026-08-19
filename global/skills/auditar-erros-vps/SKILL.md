---
name: auditar-erros-vps
description: Auditar erros e anomalias operacionais do ERP Jetta na VPS por SSH, coletando logs desde a última verificação, deduplicando fingerprints, separando erro real de job operacional/ruído, detectando comportamento estranho fora do padrão em telas como disponibilidade, programação, SAC, ocorrências e custo extra, classificando gravidade, identificando usuário/tela/rota quando disponível, investigando o código relacionado e gerando relatório Markdown enviado por Gmail. Use quando o usuário pedir monitoramento recorrente da VPS, auditoria de erros em produção, resumo de falhas/anomalias desde a última execução, ou configuração de automação para acompanhar logs e sinais operacionais.
---

# Auditar Erros VPS

## Overview

Auditar erros e anomalias novas da VPS do ERP Jetta sem alterar produção. A execução deve coletar evidências por SSH, deduplicar contra a última verificação, investigar causas prováveis no código local, gerar um relatório Markdown e enviar um resumo por Gmail para `cailaununes@gmail.com`.

## Regras

- Não fazer deploy, restart, pull, migration, alteração de `.env`, alteração de banco ou comando destrutivo.
- Não expor tokens, senhas, cookies, chaves, strings de conexão, payloads sensíveis ou dados pessoais completos no chat, relatório ou e-mail.
- Não mascarar erro como operacional sem evidência. Separar confirmado, provável e inconclusivo.
- Não modificar código nesta skill. Se encontrar bug provável, registrar causa e arquivo/função suspeitos.
- Não consultar ou alterar dados sensíveis sem necessidade objetiva. Para anomalias operacionais, preferir contagens, amostras sanitizadas e sinais agregados.
- Não inventar regra de tela. Quando o comportamento esperado não estiver claro no código/logs, marcar como `anomalia inconclusiva`.
- Usar horário de São Paulo (`America/Sao_Paulo`) em janelas, relatório e resumo.
- Usar credenciais, aliases SSH e scripts existentes no ambiente. Não inventar host, usuário, senha, token, porta ou comando de e-mail.

## Estado Local

Manter o estado fora do repositório:

- Estado: `C:\Users\Jetta\.codex\state\auditar-erros-vps.json`
- Relatórios: `C:\Users\Jetta\.codex\reports\auditar-erros-vps\`

Formato mínimo do estado:

```json
{
  "last_checked_at": "2026-06-26T09:00:00-03:00",
  "last_report_path": "C:\\Users\\Jetta\\.codex\\reports\\auditar-erros-vps\\2026-06-26_090000.md",
  "seen_fingerprints": []
}
```

Se não existir estado, usar a janela pedida pelo usuário. Em automação sem janela explícita, auditar as últimas 24 horas, declarar isso no relatório e criar o estado ao final.

## Workflow

1. Confirmar escopo da execução: projeto local, janela de tempo, destino do e-mail e se é execução manual ou automação.
2. Ler o estado local para definir `since`. Se o estado estiver corrompido, preservar o arquivo, criar um novo com sufixo `.recovered`, e declarar a limitação.
3. Descobrir comandos existentes do projeto para acessar a VPS e logs. Procurar por scripts/documentação locais antes de usar comandos genéricos: `rg -n "ssh|pm2|journalctl|caddy|deploy|logs|VPS"`.
4. Coletar logs somente leitura por SSH. Fontes esperadas quando existirem: PM2/API, web, webhooks, Caddy/Nginx, filas/jobs, deploy logs e erros de sistema relacionados ao ERP.
5. Quando possível, usar `scripts/audit-pm2-logs.ps1` enviado por stdin para a VPS. O script já evita contar linhas de stack trace, deduplica por fingerprint e classifica erro real versus job operacional.
6. Filtrar somente linhas de evento com timestamp desde `since`. Não contar linhas de stack trace, continuação de erro, linhas `at ...`, objetos Prisma, payloads, logs de sucesso ou uma mesma ocorrência repetida por linhas internas.
7. Normalizar e deduplicar por fingerprint estável: categoria + natureza + serviço + unidade/tela/rota + mensagem sanitizada. Não usar dados pessoais completos como fingerprint.
8. Para cada grupo, extrair quando disponível: primeiro/último horário, ocorrências brutas, fingerprint único, usuário/id sanitizado, tela, rota, método HTTP, status, serviço/processo, mensagem curta e stack principal.
9. Procurar anomalias operacionais fora dos logs de erro, usando sinais somente leitura quando houver caminho claro: pendências acumuladas, respostas recebidas sem efeito esperado, sync executado sem mudança, filas com retry recorrente, dados recentes que não apareceram na tela, divergência entre snapshot/cache e origem externa, ou job ativo com resultado zerado/incompatível.
10. Para anomalias de tela, abrir o ERP real no Chrome ou navegador controlável, reaproveitando a sessão logada do usuário quando existir. Entrar nas rotas reais do cliente/unidade auditados e coletar evidências de tela: KPIs, alertas, tabelas visíveis, console do navegador, estados vazios, contagens divergentes e possíveis duplicidades. Não tratar apenas logs como validação suficiente quando o problema citado envolver tela.
11. Se a sessão do ERP estiver expirada, a URL estiver inacessível ou a tela exigir ação manual, registrar bloqueio objetivo e não inventar conclusão. Nesse caso, manter apenas a parte de logs/API como cobertura parcial.
12. Investigar o código local correspondente com buscas específicas por rota, mensagem, função, tela, endpoint, nome do job ou stack. Não fazer refatoração nem correção.
13. Classificar cada grupo:
   - `critica`: indisponibilidade, perda/corrupção de dados, falha de autenticação/autorização, vazamento, loop massivo ou operação bloqueada.
   - `alta`: fluxo operacional importante quebrado, erro recorrente com muitos usuários, integração crítica falhando.
   - `media`: bug funcional localizado, retry recorrente, falha parcial com alternativa operacional.
   - `baixa`: erro raro, validação de entrada, caso operacional corrigível pelo usuário.
   - `informativa`: ruído, tentativa inválida esperada, health check, erro externo sem impacto confirmado.
14. Marcar natureza provável: `bug de código`, `erro operacional`, `anomalia operacional`, `dado inconsistente`, `integração externa`, `infra/deploy`, `permissão/autenticação`, `inconclusivo`.
15. Gerar relatório Markdown em `C:\Users\Jetta\.codex\reports\auditar-erros-vps\YYYY-MM-DD_HHMMSS.md`.
16. Enviar e-mail por Gmail para `cailaununes@gmail.com` com assunto objetivo e corpo resumido. Anexar o relatório Markdown quando possível.
17. Atualizar o estado somente depois de concluir coleta, relatório e tentativa de e-mail. Registrar status do envio no relatório.

## Classificação e Deduplicação

Separar estes conceitos no relatório:

- `erros reais`: falhas de código, contrato, banco, autorização, dados ou integração que impedem uma ação esperada do usuário ou corrompem/atrasam estado operacional.
- `anomalias operacionais`: sinais fora do padrão sem stack explícita, como resposta recebida mas não refletida, fila parada, sync sem efeito, contagem impossível, divergência entre tela/cache/origem, dados recentes invisíveis, pendência antiga demais, ou job que aparenta rodar mas não entrega resultado.
- `erros de job operacional`: falhas de scheduler, retry, sync, e-mail, IMAP, Google Sheets ou integração externa executadas em segundo plano. Elas podem ser importantes, mas devem aparecer como operação afetada, não como "usuário clicou e quebrou".
- `ruído/informativo`: health check, warn esperado, tentativa inválida prevista, log de fallback explícito ou retry temporário sem impacto confirmado.
- `inconclusivo`: evento sem mensagem suficiente, sem timestamp confiável ou sem relação clara com fluxo operacional.

Regra de contagem:

- `eventos brutos`: quantidade de linhas de evento com timestamp que batem no fingerprint.
- `grupos únicos`: quantidade de fingerprints distintos após sanitização.
- `erros novos`: grupos únicos ainda não vistos desde a última verificação, ou grupos vistos antes com aumento relevante e ainda ativos.

O resumo principal deve priorizar `grupos únicos` e listar `eventos brutos` como volume. Não dizer "4681 erros" se isso mistura retries e jobs recorrentes; dizer, por exemplo, "10 grupos únicos, 4681 eventos brutos".

Deduplicar por fingerprint sanitizado:

```text
<categoria>|<natureza>|<serviço>|<cliente/unidade>|<rota/tela/job>|<mensagem normalizada>
```

Remover do fingerprint: UUIDs, e-mails, tokens, números de plano/nota, IDs internos longos, horário exato, path absoluto de release e contadores.

## Anomalias por Tela

Auditar estas superfícies quando houver evidência objetiva nos logs, endpoints internos, jobs ou código local. Não forçar varredura pesada em toda execução; priorizar sinais incrementais e consultas agregadas.

- `disponibilidade`: resposta de motorista recebida mas não refletida na planilha/tela, pendência de envio ao Google Sheets, snapshot desatualizado, fila de reenvio crescendo, erro de copyPaste/linha filtrada, quota estourada ou divergência entre chatbot e disponibilidade diária.
- `programação diária`: planilha vazia inesperada, batch preservada por falta de planos válidos, alteração detectada sem sync efetivo, planos recentes invisíveis, divergência entre Greenmile/planilha/cache.
- `SAC/acompanhamento`: sync retornando 503, materialização sem avançar, página/offset repetido, acompanhamento recente sem aparecer, cache antigo sendo servido.
- `ocorrências`: e-mail recebido mas ocorrência não criada/atualizada, IMAP instável, envio manual reagendado, fila de e-mail travada, custo extra sem status sincronizado.
- `webhooks/chatbot`: payload recebido sem efeito esperado, status 2xx com atualização ausente, retries acumulados, resposta aceita mas sem persistência/snapshot.
- `admin/auditoria`: RequestLog falhando, usuário do token inexistente, logs de auditoria ausentes para ações recentes.

Para cada anomalia, informar:

- tela/fluxo afetado;
- sinal observado;
- por que isso parece fora do padrão;
- evidência objetiva;
- se é erro real, job operacional, anomalia operacional ou inconclusivo;
- próxima investigação recomendada.

## Relatório

Usar este formato:

```markdown
# Auditoria de Erros VPS - ERP Jetta

Janela: <inicio> até <fim> (America/Sao_Paulo)
Resumo: <N> erros novos em <G> grupos

## Prioridade

- Criticos: <n>
- Altos: <n>
- Médios: <n>
- Baixos: <n>
- Informativos: <n>

## Erros

### <titulo curto do grupo>

Gravidade: <critica|alta|media|baixa|informativa>
Natureza provável: <tipo>
Ocorrências: <n>
Primeiro/último evento: <horarios>
Usuário(s): <sanitizado ou "não identificado">
Tela/rota: <tela/rota ou "não identificada">
Serviço: <pm2/api/webhooks/caddy/etc>
Evidência: <mensagem sanitizada e curta>
Investigação no código: <arquivos/funções/rotas relacionados>
Impacto provável: <descrição objetiva>
Recomendação: <próxima ação concreta>
Confiança: <alta|media|baixa>

## Sem Evidência Suficiente

<itens que apareceram nos logs, mas não permitiram conclusão segura>

## Execução

Relatório: <path>
E-mail: <enviado|falhou|não configurado>
Última verificação gravada: <timestamp>
Limitações: <o que não foi possível validar>
```

## E-mail

Usar a skill/conector Gmail quando disponível. Não usar SMTP da VPS nem fila operacional do ERP para enviar este relatório de auditoria, porque isso misturaria monitoramento com o próprio sistema auditado. Se Gmail não estiver disponível, gerar o relatório e informar que o envio ficou bloqueado.

Assunto sugerido:

```text
[ERP Jetta] Auditoria VPS: <G> grupos novos desde <data/hora>
```

Corpo sugerido:

```text
Foram encontrados <G> grupos únicos desde a última verificação, com <N> eventos brutos nos logs.

Críticos: <n>
Altos: <n>
Médios: <n>
Baixos: <n>
Informativos: <n>

Principais pontos:
1. <grupo mais grave>
2. <segundo grupo>
3. <terceiro grupo>

Relatório completo: <path ou anexo>
```

## Finalização

Responder ao usuário com: total de erros novos, grupos principais, caminho do relatório, status do envio de e-mail, timestamp salvo como última verificação e qualquer bloqueio. Se executado por automação, manter a resposta curta e priorizar diferenças desde a execução anterior.
