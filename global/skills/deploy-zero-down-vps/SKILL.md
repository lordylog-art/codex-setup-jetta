---
name: deploy-zero-down-vps
description: Auditar commits locais já commitados e ainda sem push no ERP Jetta, avaliar risco de deploy zero downtime na VPS, pedir autorização antes de agir, e executar apenas push, git pull, migrations seguras e restart/reload mínimo quando o deploy for simples e reversível. Use quando o usuário pedir para ver se pode subir, publicar, dar push e deploy, atualizar a VPS, deploy zero down, deploy sem derrubar Caddy/portas, ou avaliar commits locais antes de produção/staging.
metadata:
  short-description: Audita e sobe deploy mínimo na VPS
---

# Deploy Zero Down VPS

## Regra de Ouro

Esta skill é um gate de deploy, não um autopiloto. Primeiro audite os commits locais que já estão commitados e ainda não foram enviados. Depois diga claramente se o deploy parece simples o bastante para zero downtime. Só execute `git push`, `git pull` na VPS, migrations ou restart/reload depois de autorização explícita do usuário.

Nunca derrube Caddy, firewall, portas, banco, PM2 inteiro ou serviços críticos para tentar "fazer funcionar". Se o deploy exigir mais do que update rápido, migration segura e restart/reload mínimo do processo afetado, pare e peça para o usuário rodar `deploy.ps1` manualmente.

## Preconditions

- Trabalhe no repo `C:\Scripts\ERP JETTA`, na branch `main`.
- Não crie branch.
- Não execute `pull`, `merge`, `rebase`, `reset`, `push` ou deploy antes da decisão e autorização.
- Não exponha secrets, tokens, senhas, `.env`, dumps, backups ou dados reais.
- Use a skill `hacker-safado` antes de qualquer push/deploy quando houver chance de dado sensível, dump, config, SQL, integração externa, `.env` ou credencial no diff.
- Se houver alterações não commitadas relacionadas ao deploy, pare e reporte; esta skill avalia itens já commitados e sem push.

## Auditoria Obrigatória

Execute leitura objetiva e registre achados:

1. Estado Git:
   - `git status --short --branch`
   - identificar upstream de `main`
   - `git log --oneline @{u}..HEAD`
   - `git diff --stat @{u}..HEAD`
   - `git diff --name-status @{u}..HEAD`
2. Escopo dos commits:
   - ler diffs relevantes dos arquivos alterados;
   - separar frontend, backend, Prisma/migrations, scripts de deploy, env examples, package/lock, infra, Caddy, PM2, SQL e integrações.
3. Risco de dados sensíveis:
   - verificar se entrou `.env`, token, chave, log, dump, backup, export, `.sql` fora de `apps/api/prisma/migrations/**/migration.sql`, arquivo temporário ou dado real.
4. Necessidades de deploy:
   - precisa instalar dependências?
   - precisa rodar build?
   - precisa rodar `prisma migrate deploy`?
   - precisa restart/reload de API, web, worker ou outro processo?
   - mudou porta, Caddy, systemd, PM2 ecosystem, Docker, firewall ou env?
5. Compatibilidade:
   - backend novo aceita frontend antigo durante alguns segundos?
   - frontend novo aceita backend atual?
   - migration é aditiva e segura?
   - existe risco de schema quebrar processo ainda rodando?

## Classificacao

Classifique antes de pedir autorização:

### Pode Fazer Com Autorização

Somente quando todos forem verdadeiros:

- commits estão limpos, pequenos e entendidos;
- working tree não tem alterações relevantes não commitadas;
- não há secrets/dumps/dados reais;
- não há alteração em Caddy, portas, firewall, SSH, `.env` real ou credenciais;
- migrations, se existirem, são aditivas e não destrutivas;
- não há mudança que exija ordem complexa entre backend/frontend;
- deploy cabe em: `git push`, `git pull`/checkout na VPS, instalar dependências se lock mudou, rodar migration segura, build necessário e reload/restart mínimo do processo afetado;
- há health check claro para validar depois.

### Não Fazer Automaticamente

Pare e peça para o usuário rodar `deploy.ps1` manualmente quando houver qualquer item:

- migration destrutiva, rename/drop de coluna/tabela, backfill grande ou alteração com lock relevante;
- mudança em Caddy, portas, firewall, systemd, PM2 global, proxy ou certificado;
- alteração de `.env` real, segredo, credencial ou dependência de variável ainda não configurada;
- schema/API com risco de incompatibilidade entre versões;
- alteração ampla, multi-serviço ou sem health check confiável;
- conflito entre local e remoto;
- falha em teste, lint, build ou auditoria de segredo;
- necessidade de downtime planejado.

## Pedido De Autorização

Se for seguro, responda antes de agir:

```text
Encontrei estes commits sem push: ...
Deploy necessário: ...
Risco avaliado: ...
Parece apto para deploy rápido sem mexer em Caddy/portas.
Posso fazer o push, atualizar a VPS e reiniciar/recarregar apenas os processos necessários?
```

Só continue se o usuário responder claramente que sim.

## Execução Autorizada

Depois do "sim":

1. Rodar revisao final curta:
   - `git status --short --branch`
   - checagem de secrets/dumps no diff;
   - testes/build/lint focados quando aplicável e rápido.
2. Fazer `git push` da `main`.
3. Na VPS, usar apenas o caminho ja existente do projeto:
   - descobrir comando de SSH/script existente no repo ou docs locais;
   - executar `git fetch`/`git pull` da `main` no diretório correto;
   - instalar dependências somente se `package.json`, lockfile ou equivalente mudou;
   - rodar migrations somente se houver migrations Prisma novas e seguras;
   - rodar build somente dos apps afetados, seguindo scripts reais do projeto;
   - usar `pm2 reload <processo>` quando suportado; se não, `pm2 restart <processo>` somente no processo afetado.
4. Não reiniciar Caddy, portas, firewall ou servidor.
5. Validar:
   - status do processo afetado;
   - health endpoint/API/web;
   - logs recentes sem erro obvio;
   - smoke test rápido do fluxo afetado quando praticável.

## Saida Final

Use este formato:

```markdown
## Arquivos Alterados
- Nenhum arquivo alterado localmente pelo deploy, ou lista se houve ajuste autorizado.

## O Que Mudou
- Commits enviados: ...
- VPS atualizada para: ...
- Processos atualizados: ...

## Validação Executada
- ...

## O Que Não Foi Validado
- ...

## Riscos/Observações
- ...
```

Se a decisão for "não fazer", explique o motivo concreto e o menor próximo passo seguro.
