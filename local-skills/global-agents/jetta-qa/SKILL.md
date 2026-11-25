---
name: jetta-qa
description: Validar ERP Jetta por persona, com provas de API/dados/componentes e QA visual exigente de templates, acabamento, responsividade, temas e interações reais.
---

# Jetta QA

Priorize testes automatizados reproduzíveis por persona. Personas funcionais são atores, escopos e cenários de teste e não exigem agente separado. Use o modo direto de entrega; Jetta Harness, flow.py, ledger e controller V2 não são dependências desta skill.

Para inventário, impacto, integração dos testes ao agregado global e aprendizado por projeto, use também [Super QA](C:/Users/caila/.agents/skills/super-qa/SKILL.md). Mantenha as regressões no repositório e registradas em `.super-qa.json`; conferir o registro não substitui executar os testes. `npm test` deve expor provas puladas/ausentes como BLOCKED, sem transformar o recorte rápido em aprovação global. As exigências específicas de personas, fronteiras reais e QA visual desta skill continuam aplicáveis.

## Responsabilidade pelo QA visual

Quando houver QA visual ou navegação de fluxos reais necessária ao aceite, delegue essas atividades a um subagente com modelo `gpt-6.1-terra`. O Terra navega os fluxos pertinentes, compara o observado ao esperado e assume toda a execução e o veredito visual, incluindo a persona Front-end enjoado, inspeção da superfície real e capturas, critérios de `references/visual.md`, evidências, identificação de defeitos e reinspeção após correções. Passe pedido, decisões, escopo, referências e acesso às evidências; peça resultado PASS/FAIL/BLOCKED por superfície e fluxo, com estados inspecionados e limitações. Sol (`gpt-6.2-sol`) implementa e revisa código, preferencialmente com revisão independente de outro Sol; Luna (`gpt-6-luna`) pode pesquisar fontes e preparar resumos simples, encaminhando análises complexas ou de segurança ao Sol. O agente principal coordena as provas funcionais e correções autorizadas e incorpora os resultados à conclusão. Se o Terra ou a delegação estiver indisponível, registre os gates dependentes como BLOCKED e informe a causa; não substitua silenciosamente por outro modelo nem declare PASS sem a prova. Mudança somente de lógica continua sem exigir QA visual.

Com `$ponte-chatgpt` explicitamente ativada na mesma tarefa, leia `C:/Users/caila/.codex/skills/ponte-chatgpt/references/auxiliares.md` para apoio do GPT Web em requisitos, diagnóstico, cenários por persona e análise visual de capturas reais pelo MCP. No QA visual, o responsável Terra envia as imagens pertinentes conforme a seção QA visual por capturas e confere os achados antes de corrigir/reavaliar. A análise do GPT Web não substitui as provas nem o veredito visual do Terra. Sem ativação da ponte, siga o fluxo normal abaixo.

## Escolher a menor prova

1. Leia pedido/decisões atuais, diff e testes pertinentes. Reutilize provas válidas e fixtures existentes. Escolha o mecanismo que pode revelar o defeito; não crie plano/manifesto/relatório separado para uma verificação focal.
2. Comece pelos runners instalados: testes de função/serviço para regras, componentes para interações isoláveis, requests automatizados para API e banco isolado para persistência/migrations. Use scripts atuais do projeto; não adicione um framework ou runtime só para cumprir ritual.
3. Monte casos por persona relevante: ator autorizado executa o fluxo normal; ator de outro escopo tenta acesso direto; entrada inválida não produz escrita; rascunho/descarte conserva estado; gestores conferem filtro/total quando alterados. Consulte [estratégias](references/strategies.md) somente para casos pertinentes, não para gerar todas as personas/combinações.
4. Para autorização, teste permitir/negar no servidor com identidades/escopos distintos e ausência de dados/efeitos indevidos. Para persistência, salve e releia pelo mecanismo real. Mocks aceleram lógica local; não substituem a fronteira real alterada no aceite. Reutilize o mesmo percurso para vários critérios.

## Automação antes de navegador interativo

- Não abra ERP, CUA ou sessão de cliques por rotina para validar lógica que testes automatizados podem cobrir. Não navegue manualmente até um fluxo só para repetir um teste já válido.
- Quando comportamento nativo exigir browser (foco real, submit/navegação, providers ou cascata), prefira teste automatizado existente em headless, com asserções e fixtures. Isso não exige abrir uma janela interativa nem toda a aplicação se o componente real isolado reproduzir a fronteira.
- Use navegador interativo para inspecionar aparência ou uma lacuna concreta que a automação disponível não consiga observar. Antes, identifique essa lacuna em uma frase; uma falha de automação pede diagnóstico focal, não troca automática para cliques. Reuse preview, sessão e capturas válidas. Não reconstrua um E2E manual completo para conferir um modal.
- Mudança somente de lógica não exige QA visual. Aparência alterada exige a persona **Front-end enjoado**, conforme [visual](references/visual.md), e Nosso Design; Impeccable quando houver decisão visual relevante. Aprovação humana segue AGENTS e decisões da tarefa.
- Só inicie o runtime ERP quando a prova ou entrega exigir; siga [runtime](../jetta-local-runtime/SKILL.md) e AGENTS, incluindo instância isolada e acesso ADMIN próprio. Preserve integrações e ativações salvas; testes simulados usam processos próprios. [Segurança](references/safety.md) aplica-se às mutações reais, respeitando as instruções atuais do usuário. Documentação/skills dispensam servidor salvo exigência explícita de entrega do projeto.

## Reinício e recuperação de efeitos externos

Em fluxos persistidos que escrevem em serviços externos, cubra a interrupção após o provedor aceitar a escrita e antes de salvar o recibo local. Use processo próprio, banco isolado e transporte controlado com contador: encerre esse escritor e inicie outro processo pelo bootstrap/worker real. Alterar status por SQL pode preparar casos, mas não substitui essa prova de reinício.

- Recuperação automática confere a intenção persistida por leitura, na operação exata, e não repete escrita incerta. Prove ausência de novos despachos, bloqueio de escritor ainda ativo e concorrência entre recuperadores; idade do registro ou lock livre sem protocolo de posse não provam interrupção. Revalide a posse na fronteira externa, inclusive após espera por quota.
- Leitura parcial, ambígua, indisponível ou de outro escopo mantém a tentativa bloqueada. Preserve registros legados sem prova de propriedade; não force sucesso, limpe o ledger ou reinicie uma ação para obter verde.
- Quando corrigir defeitos estiver autorizado, implemente a recuperação ausente no mecanismo compartilhado e mantenha suas regressões no runner oficial. Reconciliação manual de uma massa de QA resolve aquela massa; não comprova recuperação automática do produto.

Preserve ativações, credenciais e permissões existentes. Não provoque reinício do ambiente em uso nem efeitos externos reais sem autorização específica; o processo de teste e o provedor controlado devem ser próprios. Relate qual fronteira foi demonstrada e o que continuou bloqueado.

## Adequação visual dos templates

Avalie separadamente **moldura e conteúdo do consumidor**. Em revisão/lista/lote, um corpo feito de títulos e parágrafos repetidos, sem resumo útil nem estrutura visual para identificar, comparar e agir, reprova mesmo com Jotinha, template correto e testes verdes. Aplique [Conteúdo operacional escaneável](references/visual.md#conteúdo-operacional-escaneável) antes do aceite; quantidade de testes e capturas não substitui esse julgamento.

Em UI alterada, leia e execute [Front-end enjoado](references/visual.md): inspecione pixels, composição, acabamento, estados interativos, celular/tablet/desktop e claro/escuro na superfície afetada. Testes verdes, screenshot apenas salvo e uso de template não aprovam estética. Escolha curta (por exemplo, dois alcances de exportação) não justifica automaticamente modal de conteúdo extenso/altura alta ou painel de contexto. Espaço vazio dominante, resumo lateral sem informação nova e opções distantes das ações impedem o aceite visual.

Se a composição não servir, ajuste tamanho/apresentação/altura dentro do catálogo e confira novamente apenas a superfície afetada, preservando escopo e restrições explícitas do usuário. Uma escolha anterior, inclusive aprovada no planejamento, não substitui julgamento sobre o resultado renderizado. Use os critérios de proporção de `templates-new-move`; não imponha compacto a todo modal. Registre a composição final e a captura inspecionada, sem transformar testes verdes em aprovação estética.

O gate de conteúdo visual vale também para **um único registro**, confirmações, alertas, erros e formulários. Reprove modal dominado por prosa quando identidade, estado e consequência poderiam ser apresentados pelo cartão canônico, rótulos, SVG semântico ou comparação antes/depois. Caixas contendo os mesmos parágrafos não resolvem a falha. Inspecione todos os diálogos alcançáveis, inclusive secundários e legados; não aprove a jornada se Cancelar carga ou outro passo ainda usar a moldura antiga. Registre qual informação pode ser identificada/comparada visualmente na captura aberta. Texto explicativo necessário continua legível; não esconder bloqueios, inventar indicadores ou reduzir informação de segurança.

## Executar e concluir

Em modais com formulário ou componente incorporado, confira o tema de **cada camada**, não apenas o shell: cabeçalho, corpo, formulário, seções, campos, estados e rodapé. Abra a captura individual e role início/meio/fim. Um fundo preto/branco legado ou superfície destoante do catálogo reprova o visual mesmo com contraste legível e sem overflow. Aplique [Temas por camada](references/visual.md#temas-por-camada-em-componentes-incorporados) antes do PASS.

Execute um lote coerente dos testes afetados e consolide os achados. Review independente segue risco e protocolo local; testes por persona não exigem um reviewer por persona. Depois de correção, repita apenas casos e impactos invalidados. Após duas tentativas equivalentes sem informação nova, mude hipótese/método; impedimento sem ação útil é registrado uma vez com condição de retomada.

Conclua com comando/interação, personas/casos cobertos, resultado e limitações no ticket/registro existente. PASS só para comportamento demonstrado; defeito confirmado é FAIL; prova necessária indisponível é BLOCKED/INCONCLUSIVE. Sugestões e cenários extras não ampliam o aceite. Pare quando os critérios pertinentes estiverem satisfeitos e os defeitos materiais resolvidos.

Para auditoria abrangente explicitamente solicitada, use [contratos](references/contracts.md), manifestos/helpers e estratégias combinatórias pertinentes. Fora desse modo, fórmulas, percentuais de orçamento, matrizes de personas, pairwise/3-way e relatórios formais são opcionais. CI, push, deploy, produção e envios externos continuam sujeitos à autorização específica.
