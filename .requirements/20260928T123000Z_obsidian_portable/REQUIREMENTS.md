# Instalação portátil do Obsidian

## As Is

`scripts/install.ps1` não aceita `-InstallObsidian` e substitui instruções globais existentes. O setup portátil não configura o MCP do Obsidian.

## To Be

Uma opção instala ou reutiliza Obsidian e o vault existente, ativa o plugin Local REST API, configura o MCP global com chave fora do Git e preserva as configurações presentes.

## Requisitos e aceite

1. `-InstallObsidian` chama o instalador específico; `-ObsidianVaultPath` seleciona um vault existente. Aceite: execução real com esses parâmetros.
2. Arquivos `AGENTS.md`, skills e MCPs existentes permanecem. Aceite: bytes anteriores preservados e `codex mcp list` inclui `obsidian` e MCPs anteriores.
3. Chave fica só em variável de usuário. Aceite: nenhuma chave nos arquivos versionados ou no TOML; autenticação local funciona.
4. O plugin escuta somente em loopback e operações MCP funcionam. Aceite: bind local, leitura e escrita temporária validadas.

## Teste principal

Comando: `scripts/install.ps1 -InstallObsidian -ObsidianVaultPath <vault existente>`.
RED: o parâmetro não existe. GREEN: instalação idempotente, com Obsidian MCP configurado e instruções existentes intactas. A integração real no PC atual testa o fluxo sem mocks.

## Sequência

1. Adicionar opção e instalador.
2. Executar no vault existente e repetir para testar idempotência.
3. Validar CLI, MCP, preservação de arquivos, `git diff --check` e ausência de segredos.
