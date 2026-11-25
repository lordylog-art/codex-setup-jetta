# Prévia interativa de templates e protótipos

Ao compor o conteúdo, aplique a [direção visual do Estúdio](../SKILL.md#direção-visual-do-estúdio-menos-texto-mais-composição): cards úteis, ilustrações semânticas, texto essencial e interações locais com efeito observável.

Execute este fluxo após o usuário confirmar o entendimento compartilhado da skill `grilling`. Nesta skill, grooming/Gourmet são nomes usados para esse grilling; não basta iniciar a entrevista. A autorização já cobre gerar, servir e abrir a prévia; não peça confirmação adicional. Uma prévia não autoriza implementar o produto nem criar um template ausente.

Também execute por pedido explícito de protótipo/opções visuais, conforme [Protótipos visuais no Estúdio](../SKILL.md#protótipos-visuais-no-estúdio), sem exigir grilling prévio. Nesse caso, as referências ao grooming abaixo significam o pedido/spec que delimita o protótipo; preencha `grooming` com essa referência e use `prototypeOnly: true` se a implementação não estiver autorizada. A cobertura inclui todas as telas e estados desse escopo, não apenas a primeira tela. Alteração documental das skills, por si só, não dispara geração de prévia.

## Inventário e fontes verificadas

Investigação Luna em 25/10/2026, checkout `D:/newmove`: `apps/web/src/app/templates/catalogo-recursos.ts` liga 18 padrões, 54 referências e 19 imagens; `catalogo-uso-modais.ts` resolve contratos. Confirme contagens se o acervo mudar. Categorias: Montar uma tela, Resolver uma interação, Fluxos completos e Imagens e identidade. `catalogo-templates.tsx` oferece proporções; `exemplos-modais.tsx`, `exemplo-filtros.tsx`, `exemplo-acompanhamento.tsx` e `exemplos-fluxos.tsx` oferecem comportamento. O preset `regras-editor` tem Configurar regras; não existe um Configurar universal.

`ModalCenario` aceita tamanho compacto/padrao/amplo, apresentação ilustrado/conteudo, altura padrao/alta, posição esquerda/direita e escala menor/padrao/maior. `AjustesModalCenario` já implementa seletores. Larguras ilustradas 760/960/1120 px; conteúdo 1000/1240/1400 px. Conteúdo usa personagem menor fixo. Abaixo de 760 px, a imagem se oculta. O HTML deve exercitar o CSS real, inclusive dark; encolher screenshot não valida mobile.

## Gerar tudo que será visto

1. Faça uma lista completa de telas, modais, confirmações/checks, dropdowns, botões, cores alteradas, estados e transições do grooming. Cada item recebe ID estável e referência ao trecho aprovado do grooming e ao template/componente real. Não omita alterações pequenas por economia de tokens. Mostre os elementos compatíveis encontrados.
2. Sem compatibilidade, marque `gap: true`, exiba **Não tem um template** em vermelho e explique que é necessário criar um template. Aguarde autorização específica; não renderize um substituto, não copie sugestões de outros repositórios do Obsidian. Itens compatíveis continuam disponíveis. Uma autorização anterior só vale quando cobre explicitamente a capacidade ausente.
3. Escreva um consumidor React `preview.tsx` com export default, importando os componentes e CSS reais do checkout. Não clone o desenho em HTML/CSS nem use screenshot como interação. Inclua todas as superfícies inventariadas. O shell oferece Anterior/Próximo, contador e lista, mostrando um item por vez. O consumidor lê `new URLSearchParams(location.search).get("surface")` e renderiza o ID escolhido; publique esse mesmo ID no hook. Cada troca recarrega o consumidor, restaura os ajustes salvos e mantém comentários/decisões por item. Não use estado transitório do consumidor como persistência de dados reais. Use dados fictícios identificáveis e handlers locais para padrão, carregamento, sucesso, falha, alerta, vazio e demais estados pertinentes; não altere configurações ou agendas do ERP para simular.
4. Exponha todos os ajustes numa barra sempre visível acima da prévia, sem depender de Configurar ou fechar o modal. Use `useReviewControls(surfaceId, controls, onChange)` de `scripts/review-controls.ts`: surfaceId corresponde ao manifesto; cada controle declara `id`, `label`, `value`, `options: [{value,label}]` e opcionalmente `disabled`/`hint`. Publique apenas capacidades reais do item ativo e atualize a barra ao trocar de item. Controles incompatíveis ficam desabilitados com motivo. O hook valida origem e opções; o shell guarda a configuração no feedback. Inclua seletores de tamanho/apresentação/altura/lado/escala/imagem, dropdowns selecionáveis, Configurar quando existir, fechar/Escape, ações e transições. Mudanças atualizam a renderização imediatamente. Modais secundários também usam componentes catalogados. `ModalResultado` preserva a animação de sucesso e seus estilos globais necessários.
5. Registre `review.json`: `{"grooming":"caminho/nota#decisão","surfaces":[{"id":"confirmacao","title":"Confirmar alteração","grooming":"nota#trecho","template":"pattern_id / reference_id / componente / arquivo","gap":false}]}`. Inclua variantes, estados e descrição da alteração como campos adicionais para manter o contexto da IA. Nenhuma credencial ou dado pessoal real.

## Compilar e servir

### Variacoes do mesmo item

As versões seguem [Alternativas de composição interna](../SKILL.md#alternativas-de-composição-interna): corpos estruturalmente distintos, quantidade determinada pelas possibilidades úteis do item, sem teto fixo. Dimensões e Jotinha são ajustes de cada versão, não substituem essa exploração. Use títulos descritivos da organização interna; registre a diferença e as referências dos componentes no manifesto. Compare os mesmos dados e requisitos em todas as versões, confira a diferença renderizada e a navegação de todas as opções. Uma combinação solicitada pelo usuário recebe novo ID e revisão própria, preservando o histórico das versões de origem.

Mantenha IDs únicos em `surfaces`; versões alternativas recebem o mesmo `variantGroup` e `variantGroupTitle`. Exemplo: `{ "id": "m07-a", "variantGroup": "m07", "variantGroupTitle": "Registrar ocorrência", "title": "Formulário contínuo", ... }`. Cada versão mantém suas referências, estados, comentários e composição. Itens sem grupo mantêm o fluxo anterior.

O shell conta grupos como um item e oferece barra inferior 1/2/3…, nome da versão e Escolher esta opção. `?variant=<surfaceId>` abre a versão; o consumidor continua recebendo `surface=<surfaceId>`. Navegar não escolhe. A preferência fica em `variantChoices: { "m07": "m07-a" }`, junto a `items` no feedback. Concordo na versão ativa também a escolhe; trocar de escolha retorna o aceite anterior a Pendente, conservando observações/configuração. O servidor rejeita aceite de alternativa não escolhida. Alternativas pendentes/recusadas não impedem concluir a versão escolhida aprovada; todos os itens continuam no JSON.

Após entrega confirmada, o grupo sai da fila somente se a escolha e os snapshots de todas as versões ainda correspondem ao enviado. Falha de entrega conserva a revisão; mudança posterior reabre o grupo. Gravação, replay e envio bloqueiam troca de versão.

No manifesto, `prototypeOnly: true` mantém escopo exclusivamente visual. Aceite completo retorna `stage: prototype`, sem instrução de implementar; incompleto continua `review`. O padrão sem essa flag mantém `implementation` para escopo previamente autorizado. O cliente não decide o estágio. Registros de decisões incluem a escolha e a restrição de protótipo.

Regressões: `node --test tools/templates-studio.test.mjs`, registrado no agregado Super QA como `templates-studio`. Inclui contratos Python, fila, inicialização DOM, escolha sem aceite e navegação após entrega parcial, sem chamar voz/IA reais.

Os helpers ficam em `scripts/` desta skill. `build-review.mjs` usa Vite/React já instalados no checkout; não instala dependências e recusa sobrescrever um destino existente:

```powershell
node <skill>/scripts/build-review.mjs D:/newmove <preview.tsx> <review.json> <diretorio-novo>
python <skill>/scripts/serve-review.py <diretorio-novo> --checkout D:/newmove --mcp C:/Users/caila/Documents/Codex/2026-10-24/ins-2/outputs/codex_mcp.py --port 43187
```

O resultado contém `index.html`, `review.json`, bundle React em `preview/` e assets. Preserve o diretório completo. O adaptador de `next/image` mantém posicionamento e imagem, mas não reproduz otimização de entrega do Next. Para consumidores que dependam de router/providers do Next ou assets adicionais, use o harness real do projeto ou forneça esses recursos explicitamente; não finja equivalência com um mock genérico. O build não certifica a UI.

Inicie o Python em processo separado oculto (`Start-Process -WindowStyle Hidden`), com logs locais, sem encerrar servidores de outros fluxos. Verifique HTTP, abra a URL no navegador e mantenha-a disponível. Porta ocupada requer outra porta, nunca matar o processo alheio. O servidor só escuta loopback e reutiliza `tools/review-voice-server.py` para OpenTypeless, configuração, dicionário e credenciais do Windows. O HTML nunca recebe chaves. Não é necessário iniciar o ERP para esse bundle local; se escolher a rota Next, siga o launcher/autenticação do projeto.

## Voz e JSON

O shell gerado inclui observação e decisão por item, microfone, web/mobile, claro/dark, botão inferior **Falar com a IA e gerar JSON**, reprodução TTS e download. O microfone transcreve via OpenTypeless/OpenAI; TTS lê a resposta pela API OpenAI, não substitui transcrição. Texto/decisões ficam no navegador; áudio com falha pode ser baixado antes de fechar a página. O usuário precisa permitir acesso ao microfone. Consulte `/voice/health` antes de gravar e respeite `maxSeconds`; não fixe um corte menor no HTML. Mostre Parar com contador durante a captura e o processamento por IA junto do campo. Preserve o áudio para download também após inserir o texto; se a revisão falhar, mostre o aviso junto da observação e mantenha a transcrição disponível. A revisão remove hesitações sem alterar termos técnicos, resumir pedidos ou inventar trechos cortados.

O botão chama o Python existente `codex_mcp.py`, que cria um chat de revisão read-only no MCP instalado. Após organizar o feedback, usa `direcionar_chat.py` para enviá-lo ao chat de origem explicitado por `--thread` ou `CODEX_THREAD_ID`. Nunca use o destino fixo histórico do helper. O botão informa o envio confirmado e abre o JSON; falha na entrega preserva o JSON e informa que o envio não foi confirmado, sem reenvio automático. Verifique a instalação com `installed_server()`; se ausente, siga a instalação documentada do MCP existente, sem inventar pacote ou servidor. Não reutilize uma chave em texto no HTML. Fora de `prototypeOnly`, enviar todos os itens ou variantes escolhidas em Concordo encerra o Estúdio e autoriza seguir diretamente à implementação do escopo aprovado, incluindo observações e configurações, sem novo aceite. Com qualquer outra decisão, o envio mantém a etapa de revisão. O servidor calcula `stage: implementation | prototype | review` a partir das decisões validadas; a IA não decide o aceite.

O JSON final mantém literalmente observações/decisões originais e a configuração experimentada por superfície (experimentar não significa aprovar), referências ao grooming e templates, mudanças sugeridas pela IA, resumo e threadId. Valide IDs e estrutura; pendente nunca vira concordância. Resposta inválida ou timeout aparece como falha, preservando o rascunho, sem reenvio automático. Mostre andamento imediatamente, mas não prometa latência instantânea do GPT. O transporte espera até três minutos; o aceite total enviado aprova implementação apenas fora de `prototypeOnly`; apenas editar o rascunho não envia nem encerra a etapa. Permissões específicas para CI, push, deploy, produção, envios externos e criação de template ausente permanecem exigidas.

TTS usa `gpt-4o-mini-tts`, voz coral, MP3, conforme [documentação oficial](https://developers.openai.com/api/docs/guides/text-to-speech). Informe na interface que a voz é gerada por IA. Não faça chamadas externas de teste sem autorização específica; testes de contrato usam processos isolados e não alteram a configuração funcional.

## Verificar e entregar

O acabamento visual é requisito explícito, não uma etapa opcional: cada HTML deve parecer um produto pronto para revisão. Reutilize o shell `review-client.html` com fonte Inter local, hierarquia tipográfica, controles consistentes, prévia protagonista e comentários próximos. Preserve o azul/identidade do Move e os templates reais. Não entregue botões sem estilo, campos desalinhados, espaços vazios arbitrários ou aparência de página de depuração. Temas claro/escuro e mobile devem ter o mesmo nível de cuidado. Aplique Impeccable quando disponível, inspecione capturas reais e corrija problemas antes da entrega; não declare beleza ou aprovação humana apenas porque o build passou.

`scripts/example-preview.tsx` é uma demonstração técnica executável, com Configurar, todos os eixos de composição, dropdown e resultados simulados. Não o use como substituto do inventário específico do grooming.

Confira completude contra o grooming e manifeste cada lacuna. Teste controles reais e estados, teclado/foco, fechamento e ausência de diálogos sobrepostos; inspecione renderização clara/escura em web/mobile. Verifique `/voice/health`, persistência do rascunho, rejeição de origem externa e de JSON/IDs inválidos. Teste envio/voz reais quando autorizados e diferencie teste de contrato de uso real. Entregue URL ativa, arquivo HTML com assets e referências. Não encerre como concluído se faltarem superfícies compatíveis ou interações solicitadas.


## Cenários de automação e replay

Para cada superfície compatível, inventarie os caminhos previstos no grilling e publique `useReviewScenarios(surfaceId, scenarios, reset)` de `scripts/review-scenarios.ts`. Cada cenário tem `id`, `title` e `steps` com `label`, `action` (`fill`, `select`, `click`, `assert`), `selector` e, quando pertinente, `value`/`text`. Use seletores estáveis no consumidor real e verificações de resultados visíveis, incluindo preservação dos campos em falha. `reset(id)` prepara somente fixtures/estado da demonstração e cancela timers anteriores. Não altere banco, agendas ou serviços operacionais para simular sucesso/erro.

O shell executa `scenario-player.mjs` (servido como JS), aciona os campos e handlers do consumidor, destaca o elemento ativo e mostra etapa/resultado. Reproduzir reinicia o cenário; Executar todos do item percorre seus cenários e para na primeira falha. Pausar suspende as ações do player; callbacks da interface já iniciados podem terminar. Parar interrompe as ações seguintes e reinicia a fixture do cenário. Navegação, ajustes e voz ficam bloqueados durante a execução para evitar interferência. Histórico local guarda até 30 resultados entre os itens, com horário e motivo, e mostra as últimas seis execuções do item atual; não registra vídeo nem recupera uma execução em andamento após reload. Comentários/decisões não são alterados pelo replay.

A cobertura acompanha o inventário do grilling; não declare que dois cenários genéricos cobrem qualquer tela. Os três itens clonados desta demonstração têm sucesso e falha com correção apenas para mostrar o mecanismo. Teste também erro de seletor/resultado, botão bloqueado, pausa e cancelamento. Cenário concluído significa que as verificações declaradas passaram no consumidor simulado; teste real de API, persistência e efeitos exige o ambiente e autorização correspondentes.

O builder importa os estilos canônicos de ConfirmationIcon e seus keyframes de globals.css via PostCSS já instalado, para manter o check de sucesso completo no bundle sem duplicar o desenho. Se a fonte mudar, confirme novamente a seleção dos estilos e o resultado visual.


## Composição independente por estado

O consumidor mantém um mapa de layouts por estado, em vez de compartilhar tamanho/apresentação/altura/lado/escala entre Cadastro, Sucesso, Falha e Alerta. Passe o ID estável do estado como quarto argumento de `useReviewControls(surfaceId, controls, onChange, scope)`. Renderize cada modal com seu próprio layout, inclusive quando o formulário de origem permanece montado. Escala menor fixa em conteúdo expandido e imagens próprias de resultado continuam respeitando o template.

O shell salva e restaura configurações por item/estado; o JSON inclui chaves como `sucesso.posicao` e `erro.apresentacao`, além dos valores do estado ativo. Configuração legada sem prefixos migra apenas para o estado em que foi salva. Alterar a composição de Sucesso não copia essa escolha para Cadastro ou Falha. O replay restaura a composição do estado visitado mesmo com os controles bloqueados. Verifique ao menos sucesso ilustrado à direita, falha expandida à esquerda, cadastro independente e persistência após reload.


Após `delivery.status: sent`, o helper review-queue.mjs oculta apenas snapshots enviados em Concordo e ainda iguais ao rascunho atual. A fila mostra recusados, pedidos de ajuste e pendências. Aceites ficam salvos localmente e seguem no JSON completo para não perder a aprovação total em envios posteriores. Falha de entrega não oculta; alteração posterior do snapshot torna o item revisável novamente. Ao atualizar a prévia para corrigir itens recusados, preserve os IDs e o manifesto da mesma revisão para manter os aceites anteriores. Novo escopo exige uma nova revisão.

## Memória persistente

Após envio confirmado, `serve-review.py` chama `review-memory.py` e grava `D:/Obsidian/Obsidian/New move/Projetos/Templates interativos/Decisões de templates.md`. A nota contém blocos JSON legíveis com contexto, superfície, decisão, observações, configuração por estado, chat e data UTC. Reenvios iguais não duplicam o último registro; mudanças mantêm o histórico. Escrita com trava exclusiva e substituição atômica preserva o arquivo anterior em falha. Falha de memória não repete envio: o JSON e a mensagem na tela permitem recuperar o registro. A skill consulta a nota antes de compor e aplica os estilos aprovados compatíveis no consumidor; não há treinamento de modelo nem autorização automática de escopo novo. Não grave áudios, credenciais ou dados preenchidos do formulário; apenas os dados de revisão enviados pelo usuário.
