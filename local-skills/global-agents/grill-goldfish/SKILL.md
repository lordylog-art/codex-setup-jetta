---
name: grill-goldfish
description: "Coordenar grill com peixinhos para fechar decisões e revisar blocos, specs e tickets após aprovação. Use somente por pedido explícito de grill-goldfish ou grill com peixinhos; grill sozinho mantém o fluxo original."
---

# Grill com peixinhos

Coordene as skills instaladas, sem editá-las ou copiá-las. Esta skill é um fluxo híbrido de planejamento, não execução integral do protocolo EGM. Grill conduz perguntas; Goldfish revisam documentos com contexto novo; o usuário decide produto, arquitetura e artefatos. Termine na documentação aprovada, sem implementar.

## Entrada e preparação

Ative somente por seleção de `grill-goldfish` ou pedido inequívoco de combinar grill e peixinhos. A autorização vale para a tarefa atual; menção informativa ou grill simples não ativa o fluxo. Reutilize decisões e respostas da conversa em vez de reiniciar entrevista.

Leia [adaptadores](references/adapters.md) para localizar e carregar o `SKILL.md` real de cada capacidade usada. Resolva uma vez: projeto, origem se houver, destinos comprovados e capacidades de subagentes. Consulte somente contexto pertinente. Dependência ausente bloqueia sua etapa; não substitua silenciosamente a skill nem instale ferramentas.

Durante o planejamento, mantenha um registro compacto no chat e, quando autorizado, na origem existente: fase, versão atual, decisões confirmadas, hipóteses, perguntas abertas, achados tratados/pendentes, artefatos selecionados e aprovação vinculada à versão. Não crie ledger, banco ou daemon. Sem origem gravável autorizada, conserve no chat até a escolha do destino. Rascunhos técnicos de revisão usam o diretório EGM configurado no projeto atual, quando houver; sem configuração, use a pasta de trabalho atual conforme a integração Codex incluída. São insumos não aprovados, nunca pastas novas no vault nem arquivos na instalação global da skill.

## 1. Grill acompanhado por Goldfish

Carregue `grill-with-docs`, `grilling` e `domain-modeling`. Siga a árvore e as rodadas da fronteira de decisões de `grilling`; não troque por entrevista própria. Investigue fatos no código/documentação; leve ao usuário decisões com contexto e recomendação, aguardando respostas.

Classifique antes de perguntar: decisão aberta, fato investigável, requisito obrigatório ou preferência opcional. Pergunte apenas decisões que mudam a entrega; não reabra respostas, pergunte se o usuário “quer” proteção obrigatória nem transforme erro documental em nova decisão. Para visual, acessibilidade, qualidade, testes e escala, use o [mapa por risco](references/quality-map.md), sem recitar um questionário universal.

Assim que houver hipótese concreta suficiente, registre um rascunho factual curto com objetivo, atores, regras, limites, decisões e dúvidas. Use [Goldfish](references/goldfish.md), modo **grooming**, para desafiar esse documento enquanto o grill avança. Não espere o usuário lembrar de pedir a revisão. Tampouco lance uma revisão para cada resposta: revise ao fechar um conjunto de decisões ou quando nova informação mudar um contrato relevante.

Correção mecânica sem decisão aberta ou risco alterado permite conferência focal, sem entrevista nem Goldfish. Preserve a confirmação antes de criar entregas novas. Só ofereça blocos/spec/tickets se houver trabalho a decompor ou o usuário pedir; não transforme texto já definido em feature formal.

Os revisores recebem o documento e referências selecionadas, não a transcrição ou respostas ocultas. Consolidar, verificar contra fontes, deduplicar e transformar achados materiais em novas decisões na próxima fronteira do grill. Fato verificável volta à investigação; dúvida de produto volta ao usuário. Um parecer não é decisão nem requisito novo.

Não prometa “nenhuma lacuna possível”. Pronto para consolidar significa: sem pergunta material desbloqueada e sem achado material aplicável pendente, ou risco adiável expressamente aceito e registrado pelo usuário. Falha/ausência de revisor deixa a revisão dependente incompleta, não limpa. Preserve requisitos obrigatórios de dados, acesso e segurança.

## 2. Escolher entregas e negociar a proposta

Quando a fronteira estiver vazia, mostre entendimento compartilhado, pontos de revisão e limites, e pergunte o que o usuário quer preparar. Ofereça **blocos, spec e tickets conforme necessidade**, inclusive só blocos ou somente registrar decisões. Explique a recomendação sem escolher pelo usuário ou produzir os três por rotina. Tickets podem vir apenas para os blocos prontos para execução; blocos posteriores permanecem definidos sem decomposição prematura.

Após a escolha, monte no chat a proposta completa da versão atual: resultados, divisão em blocos se selecionada, conteúdo da spec, recorte de tickets, critérios observáveis, dependências e destinos. Para blocos, use o formato da skill original. Antes da primeira aprovação, isto é uma proposta de estrutura, não notas finais, tickets/IDs de tracker ou conteúdo publicado.

Convide o usuário a **acrescentar ideias, pedir alterações ou aprovar essa versão para criação**. Pare e aguarde. Escolher “quero blocos e spec” autoriza propor esses artefatos, não aprova uma divisão ainda desconhecida. “Faz sentido”, silêncio, pergunta ou aprovação condicional não libera criação.

Se vierem novas ideias, incorpore-as: investigue impactos, reabra somente decisões atingidas, consulte Goldfish no delta e reapresente a proposta completa. A aprovação anterior não cobre uma versão materialmente diferente. Esse mesmo ciclo vale após revisões e durante a criação.

## 3. Criar as entregas aprovadas e revisar

Com aprovação inequívoca da proposta vigente e destinos resolvidos, chame as capacidades selecionadas, no mesmo chat, passando a versão aprovada. A aprovação libera a criação descrita; não peça novamente permissão para cada escrita equivalente. Preserve gates adicionais reais da capacidade, como confirmação de fronteiras de teste ou uma decisão técnica ainda aberta.

Spec, blocos e tickets da mesma versão prontos para revisão formam **um pacote revisado uma vez com lentes complementares**, cobrindo cada artefato e suas relações. Não multiplique duas lentes por tipo de arquivo. Se só parte estiver pronta, revise-a e depois apenas o conteúdo novo e suas dependências. Não adie uma decisão bloqueante para agrupar revisões.

* **Spec:** use `to-spec` para sintetizar decisões já discutidas, sem reiniciar entrevista. Revisão Goldfish em modo **spec** verifica coerência, contratos, falhas, limites e critérios. Corrija erros de documentação dentro da aprovação; mudança de comportamento ou decisão material volta ao grill e exige aprovação da proposta revisada.
* **Blocos:** use `obsidian-feature-blocks`, preservando origem, formatos, resultados verticais e validação observável. Revisão em modo **blocos** verifica entregas funcionais, escopo, progressão e dependências. Só materialize a divisão aprovada, com links canônicos; não crie uma segunda especificação por iniciativa própria.
* **Tickets:** em etapa própria, após a etapa de blocos terminar e somente se escolhidos e aprovados, use `to-tickets`. Revise em modo **tickets** contra a spec/origem e blocos aprovados. Não invoque geração de tickets de dentro da skill de blocos, que é deliberadamente exclusiva para blocos.

Adapte a ordem às dependências: se houver spec, estabilize suas decisões antes dos tickets; se houver blocos, tickets apontam para seus blocos. Origem única no modo só-blocos; no modo combinado, a origem conserva ideia/decisões e a spec escolhida concentra contratos, vinculada sem cópias concorrentes. Nunca publique em tracker externo como fallback sem autorização específica.

Faça conferência cruzada de requisito → critério → bloco/ticket responsável, sem exigir um ticket por critério. Identifique requisito sem entrega, ticket fora do escopo, duplicação, ciclos e dependência que deveria bloquear apenas uma etapa. Se algo ficar adiado, indique destino e impacto explicitamente; não declare cobertura total com obrigação sem responsável.

## 4. Revisão final, mudanças e encerramento

Peça nova revisão fresca apenas sobre correções materiais e seus consumidores; reaproveite resultados não atingidos. Se o usuário acrescentar algo, aplique o mesmo ciclo de negociação da etapa 2, tanto antes quanto depois da primeira criação. Em arquivos existentes, releia e preserve conteúdo manual/status; mostre o impacto e aprove a atualização material antes de sobrescrever.

Associe pareceres à versão, fontes/escopos e lentes no registro existente. Reexecução sem mudança reutiliza o resultado; título/formatação sem alteração de significado pede conferência local. Mudança de regra, fonte ou fronteira invalida só os pareceres atingidos; o novo revisor recebe o contexto atual suficiente, não um diff incompreensível. Revisão pendente/falha nunca é reaproveitada como aprovada.

Se persistirem perguntas, falhas de revisão ou limites de recurso, exponha o ponto e aguarde a decisão necessária. Ao atingir duas rodadas sem progresso material, mostre achados restantes e pergunte se prefere continuar a investigação ou rever o recorte. Não converta o limite em aprovação nem aceite riscos automaticamente.

Finalize com links das entregas, alcance revisado, pendências/aceites explícitos e próximo bloco recomendado quando aplicável. Documentação pronta não é código pronto. Não inicie implementação, migração, CI, push ou deploy. Esta coordenação não muda grill, Matt ou EGM originais nem os aciona em pedidos futuros sem solicitação explícita.
