# Skills locais

Snapshot atualizado em 25/11/2026. Inclui skills próprias e de terceiros, inclusive Matt Pocock.

| Pasta | Origem |
| --- | --- |
| `global-codex` | `~/.codex/skills` (inclui `.system`) |
| `global-agents` | `~/.agents/skills` |
| `newmove-agents` | `D:/newmove/.agents/skills` |
| `newmove-codex` | `D:/newmove/.codex/skills` |
| `jetta-agents` | `C:/Scripts/ERP JETTA/.agents/skills` |

Para restaurar uma skill, copie a pasta inteira que contém o `SKILL.md` para o diretório correspondente na tabela. Se houver uma versão local, faça um backup antes de substituí-la. Reinicie o Codex ou abra um novo chat para carregar as skills. Para baixar o pacote, use **Code → Download ZIP** na página inicial do repositório.

As versões por contexto foram mantidas separadas, mesmo quando têm o mesmo nome. Recursos, scripts, testes e licenças presentes nas pastas acompanham cada skill. `installation-locks` preserva os registros de origem disponíveis; `manifest.json` registra SHA-256 de cada arquivo copiado.

A atualização preserva as cópias históricas de skills ausentes na instalação atual. Capturas internas do ERP, backups locais e evidências de execução ficam fora da atualização. Referências a caminhos e documentos externos às pastas das skills continuam dependendo dos projetos e ferramentas correspondentes. Este snapshot não muda o instalador legado na pasta `scripts/` nem instala ou executa as skills automaticamente.
