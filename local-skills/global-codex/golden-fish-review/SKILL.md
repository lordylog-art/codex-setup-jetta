---
name: golden-fish-review
description: Auditoria multidisciplinar exigente com peixinhos reais independentes, provas práticas e memória de gaps. Use para Golden Fish Review, auditoria com peixinhos ou revisão abrangente de uma tela e suas jornadas; não para revisão rotineira de um diff pequeno.
---

# Golden Fish Review

O chat principal é o **elefante**: conserva contexto, autorização e responsabilidade. Os **peixinhos** são subagentes reais independentes, com especialidade de auditoria ou missão de uso por uma persona concreta; entregam evidências ao elefante e não alteram código de produção. A auditoria descobre problemas além dos relatos do usuário, sem fabricar críticas ou exigir quantidade mínima.

## Escopo e autorização

Reutilize a tela, requisitos, decisões e relatos já conhecidos. Identifique apenas o que faltar para localizar o alvo. Invocação permite coordenar esta auditoria no chat atual; não cria chats visíveis, bots ou pontes externas.

Sem restrição de análise, o padrão é **revisão prática**. A invocação desta skill inclui registrar achados, testes e aprendizado no ai-memory do projeto, conforme o pedido do usuário que a criou. Uma proibição atual de salvar ou de qualquer escrita prevalece; registro de memória não autoriza mutar o produto.

- **Somente analisar/leitura/relatório:** mantenha observação não mutante do produto: preserve código, dados operacionais, configurações e integrações. Entregue relatório e registro de memória sem executar correções; se o usuário proibir qualquer escrita ou persistência, entregue somente no chat. Uma navegação que dispara escrita no produto não é somente leitura.
- **Revisão prática:** comece com provas práticas desde a primeira rodada, dentro da autorização vigente. Fixtures persistentes exigem ambiente explicitamente designado para testes; efeitos externos, destinos e custos exigem escopo vigente. Localhost pode executar integrações reais.
- **Implementação autorizada:** o elefante pode corrigir os gaps dentro do pedido já autorizado, preservando contratos e comportamentos, e revalidar o delta nos runners/QA nativos. Sugestões de arquitetura ou performance não ampliam automaticamente esse pedido.

Autonomia máxima significa completar o escopo autorizado, respeitando AGENTS e controles. Preserve autorizações da sessão sem perguntar novamente; quando o usuário ampliar o escopo, atualize-o com cronologia, sem perpetuar limitações antigas. Pergunte somente pela fronteira realmente indefinida, continuando as provas independentes. Produção, destruição, custos e destinatários não ganham autorização por invocar a skill.

## Executar

1. **Reconhecer e recuperar.** Consulte instruções locais e memória focal de gaps/prevenção antes de decidir; use [registro e memória](references/records-memory.md). Mapeie superfície real, regiões/componentes, estados, jornadas, personas, operações/tenants e configurações pelo inventário autoritativo. Construa a matriz de cobertura; um caminho bloqueado não prova o restante.
2. **Distribuir com independência.** Leia [perfis](references/profiles.md). Selecione especialidades e personas de uso pela dúvida ou risco do alvo; cubra as dimensões relevantes, justificando N/A, sem quota de perfis. Crie subagentes reais com alvo, critérios, contratos, ferramentas e autorização mínima; preserve modelo/contexto escolhidos pelo usuário. Nomeie cada agente, inclusive o cético, com **ação + alvo + foco**, por exemplo “Revisar atribuição de motoristas — endpoints e persistência”; o identificador técnico pode usar a mesma informação em snake_case. O nome visível deve permitir reconhecer a revisão sem abrir o agente. A primeira conclusão usa contexto isolado, sem hipóteses, relatos de defeitos ou achados dos outros. O elefante mantém esses relatos para reconciliação posterior. Distribua frentes independentes elegíveis sem teto numérico artificial; use lotes apenas pela capacidade real e recursos compartilhados. Se delegação faltar, declare a limitação, sem simular especialistas.
3. **Provar desde o começo.** Cada peixinho exercita os componentes e estados pertinentes na superfície real. Auditores técnicos podem inspecionar o código ativo; personas de uso fazem, quando viável, a primeira tentativa pela interface antes de ler código, conforme [perfis](references/profiles.md). Leia [provas práticas](references/practical-proof.md) antes de operar UI/API/dados/integrações/carga. Resolva browser/auth uma vez e compartilhe acesso operacional seguro, sem induzir conclusões. Após as conclusões independentes, a fase prática pode compartilhar fixtures, sessões e contratos para integrar as provas.
4. **Confrontar.** Consolide IDs e evidências segundo [registro](references/records-memory.md). Só então convoque o peixinho 14 cético com os achados: confirmar caminho ativo e contrato, contestar severidade, procurar contraprovas, separar erro de fixture/harness, deduplicar preservando problemas distintos e achados únicos válidos. Investigue lacunas relevantes restantes, ou registre o impedimento.
5. **Entregar e aprender.** Entregue relatório e matriz com o alcance realmente exercitado, contagens reconciliadas e pendências explícitas. Se houve correção autorizada, prove o delta e atualize o status; em modo análise, mantenha recomendações informativas. Registre conhecimento verificado somente com autorização de memória vigente, conforme [registro e memória](references/records-memory.md).

## Encerramento

Encerre quando os auditores disponíveis e o cético concluírem, as dimensões aplicáveis estiverem cobertas ou limitadas explicitamente, as duplicatas estiverem reconciliadas e o relatório/matriz estiverem prontos. Falha de uma ferramenta bloqueia apenas a prova dependente. Não declare PASS global, produção validada, entrega externa ou resolução de gap além das fronteiras comprovadas. Não crie tickets, commits ou publicações sem pedido.
