---
name: ship-local-prod-sql
description: Executa o fluxo seguro para subir o estado do PC/local para produção no ERP Jetta, incluindo enriquecer primeiro o SQL local com dados atuais da produção, migrar o SQL local para produção, rodar deploy remoto e validar PM2, web, API, Caddy e health checks. Use quando o usuário pedir para subir local para prod, migrar SQL local para prod, publicar banco local em produção, sincronizar PC com produção, ou rodar o fluxo completo sem sobrescrever dados novos da produção.
---

# Ship Local Prod SQL

## Regra Central

Nunca migrar o SQL local para produção antes de enriquecer o SQL local com os dados atuais da produção.

Ordem obrigatória:

1. Validar scripts e estado local.
2. Rodar enriquecimento produção -> local.
3. Confirmar que o enriquecimento terminou com sucesso.
4. Rodar migração local -> produção.
5. Validar produção online por PM2, localhost e domínio público.

Se qualquer etapa falhar, parar o fluxo, preservar evidência e não avançar para a próxima etapa.

## Caminhos Fixos

Projeto local:

```powershell
C:\Scripts\ERP JETTA
```

Script de enriquecimento obrigatório:

```powershell
C:\Scripts\ERP JETTA\tools\vps-enrich-local-from-prod-routes.ps1
```

Atalho equivalente na Área de Trabalho:

```powershell
C:\Users\Jetta\Desktop\Enriquecer SQL Local com Prod.bat
```

Script de migração local -> produção:

```powershell
C:\Scripts\ERP JETTA\tools\vps-sync-local-prod-db.ps1
```

Atalho equivalente na Área de Trabalho:

```powershell
C:\Users\Jetta\Desktop\Migrar SQL Local para Prod.bat
```

Preferir chamar os `.ps1` diretamente para capturar saída e exit code. Evitar o `.bat` de migração quando estiver automatizando, porque ele usa `-NoExit`.

## Preflight

Executar no diretório do projeto:

```powershell
git status --short
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\tools\vps-enrich-local-from-prod-routes.tests.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\tools\vps-sync-local-prod-db.tests.ps1
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\tools\deploy.tests.ps1
```

Regras:

- Não alterar `.env`, `.env.vps` ou segredos durante este fluxo.
- Não expor valores de `DATABASE_URL`, tokens, senhas ou chaves no chat.
- Não reverter mudanças locais do usuário.
- Se os testes de script falharem, corrigir o script com TDD antes de operar produção.
- Se houver mudanças locais não relacionadas, ignorar; só bloquear se elas afetarem os scripts ou o deploy.

## Etapa 1: Enriquecer Local Com Produção

Rodar:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "C:\Scripts\ERP JETTA\tools\vps-enrich-local-from-prod-routes.ps1"
```

O script deve:

- Gerar backup do banco local antes do merge.
- Baixar dump da produção.
- Restaurar produção em banco auxiliar local.
- Comparar via `prod_import`.
- Inserir no local dados ausentes da produção usando `ON CONFLICT DO NOTHING`.
- Não limpar nem sobrescrever o banco local.
- Limpar schema/banco auxiliar ao final, exceto se chamado explicitamente com opção de manter.

Critério de avanço:

- Exit code `0`.
- Mensagem final de sucesso ou ausência de exceção.
- Se o script reportar backup local, guardar o caminho para o resumo final.

Se falhar:

- Não rodar migração local -> produção.
- Resumir a etapa em que falhou e o último erro relevante.
- Sugerir correção do enriquecimento antes de tentar novamente.

## Etapa 2: Migrar Local Para Produção

Só executar depois da Etapa 1 passar.

Rodar:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "C:\Scripts\ERP JETTA\tools\vps-sync-local-prod-db.ps1"
```

O script deve:

- Ler `DATABASE_URL` local do `.env`.
- Ler `DATABASE_URL` remoto do `.env` de produção na VPS.
- Bloquear alvos perigosamente iguais, exceto contexto local/remoto loopback já tratado no script.
- Fazer dump do banco local.
- Enviar dump para a VPS.
- Atualizar código remoto antes do restore destrutivo.
- Parar processos PM2 de produção.
- Resetar schema `public`.
- Restaurar o dump local em produção.
- Reconciliar migrations conhecidas já materializadas no dump quando validado estruturalmente.
- Rodar `deploy.ps1`.
- Reancorar PM2 fora da sessão SSH.
- Validar web e API locais na VPS.

Não usar `-SkipDeployAfterSync` salvo se o usuário pedir explicitamente e aceitar que produção pode não ser validada/subida pelo fluxo.

## Etapa 3: Validação Final

Depois da migração, validar em uma nova conexão SSH:

```powershell
ssh -F NUL -i "$env:USERPROFILE\.ssh\jetta_vps_serverjetta" -o IdentitiesOnly=yes -p 22 serverjetta@50.62.183.82 "powershell -NoLogo -NoProfile -Command Set-Location 'C:\Jetta ERP\JETTA-MOVE'; pm2 list; (Invoke-WebRequest -Uri 'http://localhost:3000' -UseBasicParsing -TimeoutSec 30).StatusCode; (Invoke-WebRequest -Uri 'http://localhost:3001/api/health' -UseBasicParsing -TimeoutSec 30).Content; (Invoke-WebRequest -Uri 'https://www.ciadm.com.br' -UseBasicParsing -TimeoutSec 30).StatusCode; (Invoke-WebRequest -Uri 'https://www.ciadm.com.br/api/health' -UseBasicParsing -TimeoutSec 30).Content"
```

Aceite mínimo:

- `jetta-api` online no PM2.
- `jetta-web` online no PM2.
- `osrm-local` online quando configurado.
- `http://localhost:3000` retorna `200`.
- `http://localhost:3001/api/health` retorna `status: ok`.
- `https://www.ciadm.com.br` retorna `200`.
- `https://www.ciadm.com.br/api/health` retorna `status: ok`.

Se PM2 aparecer vazio ou health local falhar, tentar uma recuperação operacional:

```powershell
ssh -F NUL -i "$env:USERPROFILE\.ssh\jetta_vps_serverjetta" -o IdentitiesOnly=yes -p 22 serverjetta@50.62.183.82 "powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command Set-Location 'C:\Jetta ERP\JETTA-MOVE'; pm2 resurrect; Start-Sleep -Seconds 10; pm2 list; (Invoke-WebRequest -Uri 'http://localhost:3000' -UseBasicParsing -TimeoutSec 30).StatusCode; (Invoke-WebRequest -Uri 'http://localhost:3001/api/health' -UseBasicParsing -TimeoutSec 30).Content"
```

Se a recuperação falhar, reportar produção como não saudável e incluir o erro principal. Não declarar sucesso parcial como deploy concluído.

## Relato Final

Informar objetivamente:

- Enriquecimento produção -> local: sucesso ou falha.
- Migração local -> produção: sucesso ou falha.
- Commit remoto deployado, se aparecer na saída.
- PM2: nomes e status dos processos principais.
- Health local web/API.
- Health público web/API.
- Backup local criado pelo enriquecimento, se a saída informar.
- Qualquer limitação de teste, por exemplo `pytest` ausente.

Não incluir segredos, URLs de banco, tokens ou conteúdo de `.env`.
