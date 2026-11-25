# Fluxo de entrega para novas execuções

## Preparar uma vez

No ticket existente, fixe resultado autorizado, decisões aprovadas, interfaces/consumidores, ownership, dependências técnicas, critérios e comandos de prova. Reutilize referências; entregue ao executor somente este recorte. O principal resolve decisões entre frentes; cada executor resolve implementação e correções. Evite retransmitir o histórico completo.

Escolha a menor equipe útil dentro dos slots reais. Reutilize executor e reviewer da frente; mantenha independência entre autor e revisão. Custo de tokens não justifica criar mais camadas de coordenação. Paralelismo depende de arquivos, builds, portas, banco e sessões separados. Na ausência disso, serialize o recurso conflitante.

Antes de escrever, identifique os helpers e testes existentes que atendem ao contrato. Reutilize-os após conferir pertinência; inclua regressões já conhecidas da fronteira e acrescente testes para lacunas reais, e execute as provas exigidas sobre o novo candidato. Código legível e validações completas prevalecem sobre reduzir bytes. Em correções, altere o delta em vez de reemitir arquivos inteiros; após chamada interrompida, confira o estado dos arquivos e o handle antes de repetir somente o trabalho não aplicado.

## Entregar continuamente

1. Implemente o menor caminho que prova o contrato. Execute a prova focal assim que ele existir; em UI confira a composição aprovada antes da réplica e em IA exercite cedo os critérios semânticos autorizados.
2. Quando houver recorte estável revisável, disponibilize-o ao reviewer enquanto o executor avança em arquivos independentes. Reserve slot de revisão quando houver candidato pronto; evite acumular candidatos sem capacidade de validá-los. Dependência real bloqueia só a etapa que a consome.
3. Autor e reviewer tratam achados diretamente. Reavalie delta e impactos; gates de segurança/dados e visuais pertinentes permanecem. O principal confere cobertura, identidade, resultados e bloqueios, sem repetir a revisão inteira.
4. Agrupe build/integração compatíveis, preservando prova por critério/ticket. Execute a regressão integrada exigida no marco e pare após cumprir critérios. Fila, métricas ou contrato novos não exigem V2.

## Prioridade dos gates prontos

Ao receber candidato estável, confira o handoff e inicie revisão/QA exigidos na primeira capacidade disponível, antes de relatórios narrativos opcionais ou novos experimentos. Quando os gates terminarem, confira identidade, critérios e bloqueios e registre o aceite permitido antes de tarefas opcionais. Produza os relatórios e artefatos exigidos pelos próprios gates. Preserve revisão independente e decisões humanas pendentes; prioridade não dispensa nenhuma prova. Mantenha o identificador de cada execução: timeout de observação ou saída truncada pede consultar a mesma execução, não relançá-la.

Entre alterações, execute testes focais do comportamento e dos consumidores afetados; mantenha a regressão integrada exigida no candidato final. Após mudança somente na anotação da fila, reaproveite a prova nativa se código, testes, configuração, fixtures e ambiente relevantes continuarem equivalentes e a nota não alimentar nenhum teste ou gerador. Registre a equivalência; o pacote conservador de identidade continua invalidado por qualquer arquivo inventariado alterado, sem exceções artificiais, edição do pacote ou alteração de ignores. Se essa equivalência não puder ser comprovada, revalide a parte afetada.

## Conferências mecânicas pela ferramenta

Quando a entrega tiver resultado Super QA e conferir identidade manualmente for trabalho repetido, use `scripts/delivery.py --help`. O helper funciona no modo direto e não altera tickets, inicia agentes, executa runners ou aceita trabalho. Use a fonte instalada deste pacote; não reimplemente hashing no chat.

```text
python scripts/delivery.py capture --project ROOT --out ROOT/.local/candidate-01.json
# Execute os runners revistos pelo Super QA; aguarde result.json concluído.
python scripts/delivery.py seal --project ROOT --candidate ROOT/.local/candidate-01.json --report ROOT/.super-qa/RUN/result.json --suite SUITE --out ROOT/.local/delivery-01.json
python scripts/delivery.py check --project ROOT --packet ROOT/.local/delivery-01.json
```

Confirme que `.local/` já é ignorado, ou grave fora do checkout. Cada arquivo de saída é novo; preserve pacotes anteriores. Capture depois de concluir alterações de código/testes/configuração e antes da execução que sustentará a entrega. Use a lista de suítes exigidas pelos critérios; preserve as provas não automatizadas e o parecer independente no ticket.

O inventário cobre arquivos Git tracked e untracked não ignorados, inclusive binários; mudanças invalidam este pacote conservador. Não altere ignores nem remova dependências para obter CURRENT. Se houver trabalho concorrente fora do recorte, use checkout/candidato isolado ou preserve as provas seletivamente com equivalência demonstrada pelo protocolo existente. O helper não infere fechamento de dependências nem valida dados/runtime ignorados.

`CURRENT` significa somente candidato, relatório e ambiente local registrado equivalentes; `REVIEW_REQUIRED`/`MANUAL_REVIEW_REQUIRED` mantêm o aceite semântico com o responsável. Complete a equivalência de ambiente externo, banco, navegador, fixtures ignoradas e configurações relevantes; hash não prova suficiência nem autenticidade de um relatório editável. Falha da ferramenta pede investigar a diferença, sem rerun automático nem enfraquecer critérios.

## Tempo e proteção de execuções

Para comparar fluxos, registre despacho, candidato, revisão, correções, QA e aceite usando timestamps reais. Compare os mesmos critérios/modelos/recursos; reporte retrabalho, falhas/skips e tempo total, além do tempo de teste. Uma amostra não sustenta promessa de dobrar velocidade.

Esta política vale para novas invocações. Chats ativos conservam contratos/checkpoints e pacotes carregados; não reinicie processos, migre estados ou envie mensagens a esses chats para ativar a mudança.
