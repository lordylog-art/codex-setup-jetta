# Implementação com peixinhos

Use com `/peixinhos`, `//peixinhos` ou pedido explícito equivalente de supervisão. Implemente, teste, revise e integre fatias utilizáveis durante o trabalho. Golden Fish Review define a auditoria independente; Super QA seleciona/executa provas e mantém regressões nos runners nativos. Leia essas skills instaladas uma vez; para ERP, leia também `jetta-local-runtime`. Reutilize checkpoints e orçamento de tentativas do supervisor, sem outro orquestrador ou sistema de status.

A equipe usa exclusivamente os subagentes nativos deste chat, conforme SKILL.md. Não criar/usar chats, bots ou processos de agentes separados para implementação, revisão ou QA. Trabalhe pelos IDs de aceite e atualize checkboxes no ticket e na spec assim que comprovados, conforme a seção Critérios de aceite como unidade de trabalho da skill; esse acompanhamento vale para todas as etapas abaixo.

## Preparar frentes e recursos

1. Resolva projeto, feature e escopo pelo contrato existente. Identifique checkout e branch principal de entrega nas fontes atuais; não presuma o nome `main`. Registre base e alterações locais preexistentes antes de distribuir escrita. Em modo execute, o pedido de implementar e entregar no principal inclui essa integração local, sem confirmação repetida; modo somente leitura continua sem escrita. Separe essa autorização de CI, push, deploy, produção e envios externos.
2. Reserve nos checkpoints existentes, por frente: owner/agente, ticket/critério, checkout/branch/base, arquivos ou módulos exclusivos, dependências e recursos compartilhados utilizados. Inclua banco/schema/fixtures, migrações, runtime/portas e contexto/aba de navegador quando pertinentes. Propague isso no handoff; informe que outros agentes trabalham no ambiente e suas alterações devem ser preservadas.
3. Despache quantos implementadores forem úteis nas frentes elegíveis, conforme capacidade atual e modelos do Smart. Implementadores escrevem no escopo reservado; auditores Golden Fish concluem independentemente e não corrigem o código que revisam. O supervisor conserva aceite e coordenação; um executor/integrador designado realiza alterações de código e Git no alvo de integração.
4. Reutilize checkouts adequados. Use worktrees isoladas quando necessárias para escritas sobrepostas ou candidatos estáveis, pela ferramenta oficial disponível. Worktrees não isolam banco, portas, processos ou sessões de navegador. No mesmo checkout, mantenha arquivos exclusivos e serialize comandos que alterem index/branch ou dependências; ninguém troca o branch de um checkout em uso por outro agente.

## ERP ligado e navegador comprovado

Antes da primeira prova dependente, um responsável resolve ambiente e acesso:

- Use `jetta_local_status`/`jetta_local_start` com projeto absoluto conforme a skill de runtime. Reutilize instância compatível e acompanhe STARTING pela mesma operação. Confira checkout, fontes realmente servidas, URLs e saúde; servidor de outra worktree não prova o candidato. Identidade incerta bloqueia essa prova até reconciliar o alvo.
- Preserve recarga normal. O responsável pelo runtime coordena reinícios necessários com usuários das provas; evite partidas/reinícios por agente ou ticket. Deixe a instância de entrega ligada ao terminar. Queda exige diagnóstico; skill não assegura uptime após falha do host.
- Resolva o navegador interno do Codex pela ferramenta oficial disponível. O reviewer que fará a prova deve conseguir abrir a URL correta, inspecionar a página real, confirmar autenticação/papel/escopo e capturar evidência legível. Ferramenta listada ou aba aberta pelo principal não comprovam acesso do subagente. Verifique antes de depender do review; reutilize enquanto sessão, candidato e ambiente continuarem compatíveis.
- Compartilhe URLs e referências de evidência, sem tokens/senhas nos handoffs. Handles não são presumidamente transferíveis. Contextos/abas próprios permitem trabalho independente; quando houver um único controle compartilhado, reserve-o para um navegador por vez e libere após a prova. Abas no mesmo contexto não isolam cookies/login.
- Use identidades técnicas próprias e autorizadas quando disponíveis; confira permissões antes de escrever. Preserve a sessão humana: login concorrente na mesma conta pode invalidá-la. Não altere permissões para obter verde. Autenticação humana final segue runtime, por último, sem login posterior de runner na mesma conta.
- Navegação/veredito visual seguem o modelo Terra exigido pelo Smart atual e os critérios visuais aplicáveis ao ERP. Falta de acesso exige diagnóstico e bloqueia só o gate dependente. Captura cobre apenas o observado na imagem e não substitui navegação exigida. Não substitua silenciosamente navegador/modelo nem use ponte/bot externo sem pedido.

Testes isolados de lógica podem avançar sem ERP. Quando surgir fatia de API, banco ou UI, ligue/reutilize o ERP e exercite essa fronteira durante a implementação; não deixe todas as provas reais para o final.

## Testes e review incrementais

Para cada fatia verificável:

`implementar → testes focais → candidato estável → review independente + prova real pertinente → corrigir → revalidar o delta → integrar`

- Super QA: em delta pequeno com suíte conhecida, analise arquivos afetados uma vez, execute suítes registradas pertinentes e consulte o resultado da mesma execução. Inventário/plano separado somente para seleção incerta ou lacuna, conforme AGENTS. Registre novas regressões nos runners nativos e em `.super-qa.json`; comprove que revelam a falha que pretendem prevenir. Teste temporário não substitui cobertura mantida.
- Para persistência, execute o caminho ativo de API/serviço, grave e releia no banco real de teste. SQL/seed prepara fixture, mas não comprova escrita pelo produto. Para UI, execute a ação e confira estado após reload; quando pertinente, correlacione request, job, banco e integração até a última fronteira observada. Cubra permitir/negar e escopos relevantes quando acesso mudar.
- Prepare dados fictícios identificáveis no ambiente já designado para testes, com responsável e IDs/namespace por frente, respeitando constraints e contratos. ERP normal conserva integrações/agendas reais. Simulações, falhas e reinícios destrutivos usam processo/banco/portas próprios e transporte controlado. Sem ambiente autorizado para mutação necessária, bloqueie a escrita e continue provas independentes. QA não autoriza envios externos ou mudança global de ativações.
- Golden Fish: distribua perfis aplicáveis entre auditores reais, com critérios/fontes e candidato, sem induzir primeiras conclusões com achados alheios. N/A exige razão; ferramenta indisponível é limitação. Inspecione superfície real desde a primeira rodada executável. Após conclusões independentes, o cético confronta evidências conforme a skill. Reutilize revisão suficiente e independente, sem outra camada automática.
- Review/QA pode acompanhar implementação em arquivos independentes se o candidato observado permanecer estável. No ambiente de aceite, pause escritores que possam mudar candidato, dependências ou fixtures durante a prova. Mudança relevante exige revalidar a parte atingida; resultado de outra branch não é PASS integrado.
- Registre no ticket existente candidato/base, comandos/run IDs, resultado bruto, ambiente/fixtures, evidências, achados e critérios provados. Separe PASS, FAIL, BLOCKED e não executado. Verde isolado não demonstra cobertura total, aprovação visual ou integração externa não exercitada.

## Evitar atropelamentos e loops

Um titular controla cada recurso mutável compartilhado durante a operação: arquivo/módulo, integração Git, migração, fixture, configuração, processo/porta ou controle do navegador. Leituras e namespaces comprovadamente independentes continuam paralelos. Migrações no mesmo schema são sequenciais; compatibilidade/rollback seguem o projeto.

Sobreposição inesperada suspende só escritores envolvidos; preserve diffs e reconcilie ownership/ordem antes de retomar. Não reverta, faça stash, limpe ou inclua em commit alterações alheias para liberar o fluxo. Edição humana concorrente exige reconciliação: ownership documental não é lock do sistema operacional.

Timeout de observação não significa execução encerrada: consulte o mesmo run/agente/processo antes de relançar. Travamento real exige etapa, assinatura e evidência de progresso; diagnóstico/cancelamento atinge apenas processo de teste próprio e identificado. Preserve resultado parcial e verifique parada antes de substituir; não mate ERP compartilhado para destravar suíte.

Use orçamento/recuperação existentes. Nova tentativa precisa de hipótese discriminante sustentada por evidência ou delta pertinente; trocar agente não zera contador. Crash após claim/dispatch exige reconciliar owner/agente antes de redisparar. Sem ação útil, registre BLOCKED e condição de retomada enquanto frentes independentes avançam, evitando repetição/polling indefinido.

## Integrar e entregar para o humano

1. O integrador único confere candidato revisado, base, dependências e ausência de escritores conflitantes. Integre candidatos compatíveis na ordem técnica, por merge ou mecanismo local do projeto. O modo exige chegar ao checkout/branch principal definido na entrada quando a execução autorizar integração local. Branch de trabalho pronta é resultado parcial.
2. Preserve alterações preexistentes. Se impedirem integração segura, prepare-a em checkout adequado e registre o impedimento de levar ao principal; não esconda dirty state com reset/clean/stash nem adicione arquivos alheios a commits. Integrador resolve conflitos, com autores quando necessário; reavalie review/testes atingidos pela resolução.
3. Valide resultado combinado final no principal: build e suítes Super QA exigidas pelos critérios/risco compartilhado, consumidores e jornadas atingidas, com runtime servindo esse resultado. Provas anteriores equivalentes podem ser reutilizadas com equivalência demonstrada; ainda é necessária prova da integração combinada exigida. Agregado completo só quando pedido, marco ou risco concreto exigir. Inspecione o resultado e mantenha falhas/skips explícitos.
4. Deixe fontes integradas no principal, ERP saudável e ligado, banco/configuração preservados e jornada acessível no navegador Codex. Confira autenticação humana esperada conforme runtime e deixe aba aberta. Limpe/restaure apenas fixtures próprias que devam ser removidas; preserve dados de demonstração autorizados para teste humano e informe como identificá-los, sem expor informações sensíveis.
5. Entregue branch/checkout e identificação do candidato integrado, URL clicável, jornada curta para humano, provas e limitações. Pronto para teste humano não significa aceite humano: mantenha pendente critério que exigir confirmação. Gate obrigatório bloqueado, achado material ou integração incompleta impede COMPLETE; apresente resultado parcial com causa concreta.

O modo é interpretado pela skill, não registra comando no Codex nem mantém processos vivos após falha do host. Exige evidência em vez de prometer ausência absoluta de defeitos. CI, push, deploy, produção e envios externos conservam autorização específica.
