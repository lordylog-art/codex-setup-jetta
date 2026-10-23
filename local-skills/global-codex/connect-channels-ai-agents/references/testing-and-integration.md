# Teste, compilação e integração

Fontes atuais A=8492.ea311dabe5541af9.js; M=main.c1b6a1d22d66025d.js. Executar sandbox, ask, optimizer e ferramentas usa serviços de IA; não é teste local. A pesquisa inicial fez somente GETs e análise de JS; a demonstração autorizada de 14/10/2026 acrescentou escrita, upload e sandbox.

## Sandbox do agente

Serviço M módulo14824; UI A@414307:

```text
POST /ai/v1/aiagent/sandbox
{
  agentConfig: /* DTO de buildAgentConfig, incluindo isTeam e vínculos */,
  messages: [{role:"user"|"assistant",content:string}],
  userMessage: string
}
```

UI envia histórico sem mensagem system local; a pergunta atual fica em userMessage, não duplicada em messages. clearChat A@414036 apenas limpa histórico local e insere aviso visual; não possui endpoint reset recuperado. O sandbox usa config do formulário, portanto pode testar alterações ainda não salvas. Não é envio WhatsApp nem prova de execução em canal.

Na demonstração de 14/10/2026, CALL_API retornou `{status:"success",sandbox:true,skillType:"CALL_API",args:{}}`, inclusive com URL que responderia HTTP503. Isso não comprova chamada HTTP nem tratamento de falha. DATE_TOOLS produziu datas verificáveis; busca FILE retornou conteúdo indexado e horários corretos. FAQ QA salvo com READY e docsCount0 não retornou documentos: valide busca com pergunta conhecida, não apenas status. Artefatos T01-response-file-indexed.json e T02–T11-response.json ficam na pasta bakery-live-20261014 indicada na skill.

CLI explícita: `node scripts/agents.mjs sandbox <request.json> <output-novo.json>`. O marcador de tentativa é salvo antes da chamada; output existente impede a execução. O helper verifica forma, não isolamento de ferramentas no backend. Use dados fictícios/config sem habilidades que produzam efeitos, dentro da autorização para consumir IA. Backend pode possuir outras capacidades: não prometer que sandbox é livre de efeitos nem disparar API/CRM/follow-up para “só ver se funciona”.

Resposta A@415025 tolera formattedResponse como texto, array ou `{messages:[{text,content,fileUrl}]}`. Fallback usa response agrupado e toolCalls. Campos de tokens/custo da UI são estimados por comprimento/tempo/fator constante: não relatar como uso faturado pelo provedor. Sem resposta completa, toolCalls ou consumo observado, HTTP200 não certifica a conversa.

Perguntas sintéticas relevantes: cumprimento/objetivo; coleta de dados faltantes sem inventar; pedido fora do escopo; pergunta de conhecimento com fonte; transferência solicitada; contingência; escolha de subagente. Testar ferramenta executável exige escopo específico e destino de teste.

## Otimização de prompt

POST `/ai/v1/aiagent/agent-optimization` com `{agent:DTO,executionId,customRequest?}`. O cliente omite customRequest vazio. Retornos são sugestões e eventos; A@394508 monta configuração para comparar. Não aplicar automaticamente sugestões a agentes em produção. Refazer prompt não substitui teste de negócios. Esta operação não foi executada.

## Save, estados e aceitação

Serviço recuperado cria/atualiza por POST/PUT aiagent; não tem handler separado de deploy. Enum DRAFT/PUBLISHING/FAILED/READY. Após save, releia recurso até estado terminal com prazo finito. Publique/ative canais somente pelo fluxo apropriado e quando pedido incluir esse efeito. Agente READY significa compilação/status informado, não qualidade da resposta ou entrega.

Journal create/update registra inputHash, targetIds e estado de tentativa, sem payload sensível. ReadbackMatches compara hash estrutural e pode divergir por campos/defaults adicionados pelo backend; isso exige revisão semântica, não retry. Reconcile é leitura e jamais declara autorização automática para repetir. Uma correspondência de nome pode ser recurso anterior; compare identidade e conteúdo antes de adotar.

## Consumidor chatbot

Use [connect-channels-chatbots](../../connect-channels-chatbots/SKILL.md) para editar Builder. Nó IA nativo:

```text
type: "AI_AGENT" | "AI_TEAM"
aiAgentConfig: {
  aiAgentId, aiAgentName, aggregation,
  customTargets: {targets:[/* flowId e destino nativo */]},
  isAgentActive,
  subAgentsConfig: {configs:[{aiAgentId,clientGeneratedId,positionX,positionY}]}
}
```

AI_TEAM reutiliza **aiAgentId**, não aiTeamId inventado. subAgentsConfig deriva de promptConfig.subAgents. Nos targets do supervisor a chave pode ser `${aiAgentId}:${flowId}`; consulte contrato do Builder antes de gerar edge. Grafo e campos de target devem concordar. Mesmo nome não substitui ID.

Agregação do nó controla espera/inatividade/saída de contingência; messageInterval do agente controla atraso de resposta. Follow-up exige compatibilidade com inatividade calculada em skills.md. Canal pode ter indicador digitando próprio. Não corrigir inconsistência ativando/desativando canal ou publicando chatbot fora do pedido.

## Limites e roteiro de prova

| Superfície | O que comprova |
|---|---|
| plan/testes locais | Forma mínima, transporte simulado, preservação, journals/paginação; sem fornecedor |
| GET autenticado | Sessão/base autorizadas para leitura, recurso/shape atual |
| POST/PUT + readback | Persistência da mudança e identidade; não conversa |
| READY | Estado de compilação informado; não comportamento integrado |
| Sandbox | Resposta do simulador com config/histórico definidos; não canal real |
| ask knowledge | Consulta de uma base; não agente completo |
| Conversa sintética em canal | Caminho real daquele cenário, efeitos/logs/transferências/entrega observados |

Prova de habilidade requer ação efetiva no destino autorizado e log correspondente, não só objeto configurado. Concorrência com humano, arquivamento, retorno de MCP, multimídia, supervisor aninhado e erros dependem de cenários próprios. Não declarar “tudo aceito” usando apenas mocks, JS ou menu de opções.
