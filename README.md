# Codex Setup Jetta

Configurações portáteis do Codex e do ERP Jetta. O repositório não inclui código do ERP, credenciais, sessões, `.env`, logs ou configurações locais do aplicativo.

## Instalação no outro PC

1. Instale o Codex Desktop e entre na mesma conta.
2. Clone este repositório em qualquer pasta.
3. No PowerShell, execute:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install.ps1 -JettaPath 'C:\Projetos\Jeta Move' -InstallRtk
```

4. Reinicie o Codex Desktop e abra uma nova task.

Para integrar um vault do Obsidian já existente, execute separadamente:

```powershell
.\scripts\install.ps1 -InstallObsidian
# Se houver mais de um vault: -ObsidianVaultPath 'C:\caminho\do\vault'
```

Essa opção preserva o setup Codex/Jetta existente. Ela instala Obsidian pelo `winget` se necessário, exige a CLI oficial habilitada, reutiliza o vault e configura `obsidian-local-rest-api` e o MCP global. Se a CLI ou os plugins comunitários ainda estiverem desabilitados, ative-os no Obsidian e execute novamente. Reinicie o Codex Desktop para herdar `OBSIDIAN_API_KEY`. O endpoint só é aceito em loopback.

O instalador salva uma cópia dos arquivos globais que forem substituídos em `~\.codex-backup`. Ele instala as instruções globais, skills pessoais, referência Connect, RTK e as instruções/Spec Kit do Jetta no caminho informado. O projeto ERP precisa já existir nesse caminho. A referência do RTK no `AGENTS.md` é criada pelo próprio RTK com o caminho correto do novo usuário.

## O que não é transportado

- Login, tokens, `.env`, sessões e bancos locais.
- `config.toml` do Codex: contém integrações e caminhos específicos da máquina.
- Chave da API do Obsidian, dados do vault e configurações locais do plugin.
- Código e dados do ERP Jetta.

## Serena

Não é instalado automaticamente: a configuração atual apresentou `KeyError: 'languages'`. Corrija a configuração do Serena antes de adicioná-lo ao `config.toml` do novo PC.

## Atualização

No novo PC, execute `git pull` dentro deste repositório e rode novamente o instalador. Revise o diff antes de aplicar mudanças.
