---
name: run-deploy-vps
description: Run/rodar o deploy da VPS do ERP Jetta fazendo `git pull` primeiro e depois a sequencia oficial `deploy.ps1 -AllowDirectProductionDeploy` e `deploy-webhooks.ps1`. Use quando o usuario pedir `/run`, run deploy, rodar deploy, VPS, deploy webhooks, ou avisar apenas se deu bom ou deu ruim.
---

# Rodar Deploy VPS

## Workflow

Executar somente o script bundled `scripts/run-deploy-vps.ps1`. Ele:

1. Entra em `C:\Scripts\ERP JETTA`.
2. Confere se `deploy.ps1` e `deploy-webhooks.ps1` existem.
3. Roda `git pull`.
4. Roda `.\deploy.ps1 -AllowDirectProductionDeploy`.
5. Se o deploy principal passar, roda `.\deploy-webhooks.ps1`.
6. Retorna sucesso apenas se os tres comandos terminarem com exit code `0`.

## Regras

- Nao rodar `git push`, `merge`, migrations destrutivas ou comandos extras por conta propria.
- Nao alterar `.env`, credenciais, firewall ou servicos fora do que os scripts ja fazem.
- Se qualquer etapa falhar, parar e reportar "deu ruim" com o comando que falhou e o exit code.
- Se passar, reportar "deu bom" de forma curta.

## Comando

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Jetta\.codex\skills\run-deploy-vps\scripts\run-deploy-vps.ps1"
```
