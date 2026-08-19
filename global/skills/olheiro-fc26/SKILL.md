---
name: olheiro-fc26
description: Analisa o relatório mundial JSON de um save do EA SPORTS FC 26 e encontra reforços por posição, orçamento, idade, overall, potencial, pé, físico, atributos, estrelas, PlayStyles regulares e PlayStyles Plus. Use quando o usuário pedir olheiro, scouting, shortlist, indicação de contratação, promessa, substituto ou jogador com perfil específico no próprio save.
---

# Olheiro FC 26

Encontrar jogadores que realmente existem no relatório exportado do save. Não inventar nome, preço, clube, atributo nem disponibilidade.

## Localizar o relatório

Usar, nesta ordem:

1. JSON indicado/anexado pelo usuário.
2. `MUNDO_FC26_*.json` mais recente em `%OneDrive%\Desktop\FC26_OLHEIRO`.
3. Arquivo mais recente em `%USERPROFILE%\OneDrive\Desktop\FC26_OLHEIRO` ou `%USERPROFILE%\Desktop\FC26_OLHEIRO`.

Se não existir, pedir que o usuário execute `EXPORTAR_MUNDO_JOGADORES_JSON.lua` no Lua Engine com a carreira aberta. Não usar o JSON `MEU_TIME_*.json` como se fosse relatório mundial.

Validar `schema_version`, `scope`, `generated_at`, `player_count` e `players`. Alertar se `player_count` divergir do tamanho real.

## Entender o pedido

Extrair da linguagem natural, quando informado:

- posição principal e posições alternativas aceitáveis;
- orçamento máximo e se inclui salário/cláusula;
- idade mínima/máxima;
- OVR e potencial mínimos/máximos;
- PlayStyles aceitos e PlayStyles obrigatoriamente Plus;
- atributos mínimos ou características funcionais;
- pé preferido, perna ruim e fintas;
- altura, peso, clube/país/liga quando os dados permitirem;
- jogador pronto, promessa, rotação, especialista ou oportunidade;
- quantidade de opções e exclusão do clube controlado.

Perguntar somente quando uma omissão mudar materialmente a shortlist. Na ausência de limite, usar 15 opções e separar em alvo principal, alternativas e apostas.

Ler `references/schema-e-criterios.md` quando precisar mapear campos, PlayStyles, posições ou interpretar orçamento.

## Fazer a busca determinística

Executar `scripts/scout.py` com Python. Preferir o runtime retornado por `codex_app__load_workspace_dependencies`; usar Python do sistema somente se estiver disponível.

Exemplo:

```powershell
python scripts/scout.py --positions "ST,CF" --max-age 23 --min-potential 85 --budget 40000000 --plus "Quick Step" --playstyles "Finesse Shot" --attribute finishing:82 --exclude-user-team --limit 20
```

Parâmetros úteis:

- `--json <arquivo>`
- `--positions ST,CF`
- `--min-age` / `--max-age`
- `--min-overall` / `--max-overall`
- `--min-potential` / `--max-potential`
- `--budget`
- `--playstyles` para regular ou Plus
- `--plus` para exigir Plus
- `--attribute campo:mínimo` repetível
- `--min-skill-moves` / `--min-weak-foot`
- `--preferred-foot 1|2`
- `--exclude-user-team`
- `--limit`

Não ler o JSON mundial inteiro no contexto quando o ranker puder reduzi-lo primeiro. Analisar profundamente apenas os candidatos retornados.

## Tratar orçamento corretamente

Usar somente `financials.market_value` ou `financials.release_clause` quando presentes. `budget_status = unknown` significa que o relatório não forneceu valor comparável.

Nunca:

- transformar `unknown` em zero;
- inventar valor de mercado;
- afirmar que o clube aceitará o valor;
- confundir salário com taxa de transferência;
- excluir automaticamente um candidato sem preço conhecido.

Quando houver candidatos `unknown`, separá-los como “preço a verificar no jogo”.

## Avaliar encaixe

Não ordenar apenas pelo overall. Cruzar:

- posição e capacidade real de cumprir a função;
- OVR atual, potencial e margem de evolução;
- atributos focais do pedido;
- PlayStyles regulares e Plus relevantes;
- idade, físico, estrelas e pé;
- preço real disponível e risco de orçamento;
- clube atual e condição de agente livre;
- dados ausentes, tratados como incerteza, nunca como zero.

Para cada candidato final, informar:

1. nome, ID, clube e idade;
2. posição, OVR e potencial;
3. valor/cláusula/salário quando presentes;
4. PlayStyles e Plus decisivos;
5. atributos que sustentam o encaixe;
6. motivo da indicação;
7. risco, limitação ou dado ausente;
8. categoria: alvo principal, alternativa segura, promessa ou oportunidade.

## Validar antes de responder

Confirmar:

- todos os IDs pertencem ao JSON;
- filtros obrigatórios foram respeitados;
- PlayStyle regular não foi apresentado como Plus;
- nenhum preço foi estimado silenciosamente;
- agente livre não recebeu clube inventado;
- resultados sem idade/valor estão sinalizados;
- jogadores do time do usuário foram excluídos quando solicitado;
- shortlist não contém duplicatas.

## Registrar o relatório

Salvar a análise final em `%APPDATA%\Codex\FC26\Olheiro` com nome seguro:

`AAAA-MM-DD_HH-mm_<perfil>.md`

Não sobrescrever relatórios anteriores. Incluir caminho do JSON fonte, filtros aplicados, data do save, shortlist e ressalvas. Verificar a existência do Markdown antes de afirmar que foi salvo.

No chat, entregar uma tabela compacta dos melhores nomes, destacar o principal alvo e informar o caminho absoluto do relatório Markdown.
