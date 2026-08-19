---
name: treinador-fc26
description: Analisa um elenco exportado do EA SPORTS FC 26 e cria, a partir do nome de um treinador real ou fictício, um plano completo com identidade tática, formações, escalação titular, banco, alternativas de time, funções individuais, bolas paradas, substituições e justificativas. Use quando o usuário pedir para montar, escalar, organizar ou registrar um time no estilo de um treinador e quiser o resultado salvo em Markdown no AppData.
---

# Treinador FC 26

Crie um plano de treinador aplicável ao elenco real do usuário, sem inventar jogadores ou atributos. Entregue a resposta no chat e registre a versão completa em Markdown.

## Entradas

Obtenha o nome do treinador na mensagem do usuário. Se estiver ausente ou houver dois treinadores plausíveis com o mesmo nome, peça somente a informação indispensável.

Use como elenco, nesta ordem:

1. JSON indicado ou anexado pelo usuário.
2. JSON `MEU_TIME_*.json` mais recente encontrado em `%USERPROFILE%\OneDrive\Desktop`, `%USERPROFILE%\Desktop`, `%USERPROFILE%\OneDrive\Área de Trabalho` ou `%USERPROFILE%\Área de Trabalho`.
3. Se nenhum JSON existir, peça ao usuário para executar o exportador do time ou anexar o arquivo. Não monte uma escalação nominal sem dados do elenco.

Antes de analisar, confira `schema_version`, clube, data do arquivo, `player_count` e a lista `players`. Considere especialmente:

- posição principal e alternativas;
- overall, potencial, idade/data de nascimento quando disponível e reputação internacional;
- atributos técnicos, físicos, mentais e de goleiro;
- pé preferido, perna ruim, fintas, altura e peso;
- PlayStyles regulares e Plus;
- vínculo com o elenco, lesões, suspensão e demais estados quando presentes.

Não trate campo ausente como valor zero. Marque-o como indisponível e reduza a confiança da conclusão relacionada.

## Pesquisa do treinador

Para treinador real, pesquise informações atuais na web porque clube, ideias e sistemas podem mudar. Priorize entrevistas do treinador, materiais do clube e análises táticas reputadas. Registre links e datas das fontes.

Separe claramente:

- características documentadas do treinador;
- adaptação feita ao elenco do usuário;
- inferências ou escolhas criativas.

Para treinador fictício, histórico alternativo ou versão definida pelo usuário, use a descrição fornecida e marque as suposições. Não atribua fatos inventados a uma pessoa real.

## Montagem do plano

Leia integralmente `references/perfil-treinador-template.md` e siga sua estrutura.

### Identidade tática

Defina formação-base e até duas alternativas coerentes. Explique:

- organização com bola, largura, altura da linha, ritmo, saída e criação;
- organização sem bola, bloco, pressão, encaixes e proteção da área;
- transição ofensiva e defensiva;
- funções-chave e comportamentos por setor.

Traduza a ideia do treinador para o elenco disponível. Não force uma cópia literal quando os jogadores não oferecem o perfil necessário; explique a adaptação.

### Escolha dos jogadores

Escolha exatamente 11 titulares, sem IDs duplicados e com goleiro. Para cada jogador, informe posição, função, motivo e eventual risco.

Não escolha apenas pelo overall. Cruze encaixe posicional, atributos relevantes, pé, físico, PlayStyles, potencial, experiência e complementaridade. Exemplos:

- zagueiro de saída precisa de passe, compostura e perfil defensivo compatível;
- ponta por dentro precisa combinar pé, lado, condução, criação/finalização e PlayStyles;
- lateral invertido precisa sustentar decisões por dentro;
- goleiro-líbero precisa de atributos de goleiro e distribuição, não atributos irrelevantes de linha.

Respeite lesões e suspensões presentes no JSON. Se a informação não existir, declare que disponibilidade médica e disciplinar não pôde ser confirmada.

### Alternativas

Inclua, quando o elenco permitir:

- time de força máxima;
- time mais ofensivo;
- time de controle/defensivo;
- time de rotação ou desenvolvimento de promessas;
- banco priorizado e substitutos por função.

Cada alternativa deve ter 11 jogadores ou ser apresentada apenas como mudanças explícitas sobre o time-base. Explique quando usar.

### Gestão de jogo

Defina capitão, cobradores e plano de substituições com base nos dados disponíveis. Crie cenários para vencer, empatar e perder, sem prometer instruções que não existam no FC 26.

## Validação obrigatória

Antes de salvar, confirme:

- 11 titulares e um goleiro;
- nenhum jogador repetido no mesmo time;
- todos os nomes e IDs pertencem ao JSON;
- posição/função é plausível ou a improvisação está declarada;
- banco não repete titulares;
- alternativas respeitam o elenco disponível;
- conclusões não contradizem atributos ou PlayStyles;
- fontes, suposições e campos indisponíveis estão identificados.

Se o número de jogadores do JSON não coincidir com `player_count`, avise e use os registros efetivamente carregados.

## Registro no AppData

Salve o documento final em:

`%APPDATA%\Codex\FC26\Treinadores`

Crie a pasta se necessário. Use nome de arquivo seguro no formato:

`AAAA-MM-DD_HH-mm_<treinador>_<clube>.md`

Remova caracteres inválidos do nome, não sobrescreva relatórios anteriores e grave em UTF-8. Não crie CSV, JSON auxiliar ou arquivo na Área de Trabalho. O JSON do elenco é somente leitura.

No final da resposta, informe o caminho absoluto do Markdown criado e resuma formação, treinador e titular principal. Se não for possível salvar, entregue o conteúdo no chat e explique o erro real; nunca afirme que o arquivo foi criado sem verificar sua existência.
