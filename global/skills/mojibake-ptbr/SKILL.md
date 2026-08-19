---
name: mojibake-ptbr
description: Localizar, auditar e corrigir mojibake/encoding corrompido em texto humano em português do Brasil, usando ftfy e heurísticas conservadoras. Use quando o usuário invocar $mojibake-ptbr, pedir para procurar/corrigir mojibake, UTF-8 quebrado, acentos corrompidos como Ã/Â/â€™/�, ou quiser revisar o projeto inteiro, um contexto da conversa, arquivos, pastas ou trechos específicos.
---

# Mojibake PT-BR

## Escopo

Determinar o alvo antes de rodar:

- Se o usuário invocar a skill sem detalhe e não houver contexto útil, analisar o projeto inteiro a partir do diretório atual.
- Se o usuário invocar sem detalhe, mas a conversa tiver arquivos, trechos ou erro específico em foco, analisar apenas esse contexto.
- Se o usuário especificar arquivo, pasta, trecho, diff, componente, rota ou mensagem, analisar somente o alvo especificado.
- Se houver trecho literal no prompt, usar modo texto e não varrer o projeto inteiro.

## Ferramenta

Usar o script bundled:

```powershell
python C:\Users\Jetta\.codex\skills\mojibake-ptbr\scripts\mojibake_ptbr.py scan --path .
python C:\Users\Jetta\.codex\skills\mojibake-ptbr\scripts\mojibake_ptbr.py fix --path apps\web\src
python C:\Users\Jetta\.codex\skills\mojibake-ptbr\scripts\mojibake_ptbr.py scan --text "ProgramaÃ§Ã£o"
```

Opções úteis:

- `scan`: auditar sem modificar.
- `fix`: aplicar correções seguras e gravar arquivos em UTF-8.
- `--path`: repetir para vários arquivos ou diretórios.
- `--text`: analisar um trecho literal.
- `--stdin`: ler trecho pelo stdin.
- `--json-out tmp\mojibake-report.json`: salvar relatório estruturado.
- `--include-tests`: incluir arquivos de teste.
- `--include-docs`: incluir Markdown e documentação.

## Fluxo

1. Rodar `scan` no escopo correto.
2. Ler o resumo e os itens encontrados.
3. Se o usuário pediu correção, rodar `fix` no mesmo escopo.
4. Conferir o diff dos arquivos modificados.
5. Procurar sinais remanescentes com `rg "Ã|Â|â€™|â€œ|â€|�" <escopo>`.
6. Rodar testes próximos quando a correção alterar texto usado em fluxo, UI, API pública, snapshot ou comparação.
7. Responder com total de arquivos analisados, arquivos alterados, linhas problemáticas encontradas, linhas corrigidas e pendências.

## Política de Correção

Corrigir automaticamente apenas quando houver evidência forte de mojibake:

- Caracteres/sinais como `Ã`, `Â`, `â€™`, `â€œ`, `â€`, `�`.
- Correção do `ftfy` que remove sinais de mojibake e melhora texto em português.
- Texto humano em UI, mensagens, documentação, fixtures textuais ou respostas públicas.

Não corrigir automaticamente:

- Arquivos gerados, build output, `node_modules`, `.git`, `.next`, `dist`, `coverage`, logs e caches.
- Contratos técnicos, slugs, rotas, enums, IDs, chaves de payload, nomes de colunas/abas externas e valores esperados por integração, salvo se o usuário pedir explicitamente.
- Dados externos legados quando a forma corrompida puder ser parte do contrato.

Quando houver dúvida, reportar como pendência manual em vez de alterar.

## Resposta Final

Entregar um resumo estruturado em português do Brasil:

- Escopo analisado.
- Total de arquivos analisados.
- Total de linhas com problema encontradas.
- Total de linhas corrigidas.
- Arquivos alterados, com contagem por arquivo.
- Exemplos curtos de antes/depois, sem expor segredos.
- Pendências manuais, se houver.
- Validações executadas e qualquer teste não executado.
