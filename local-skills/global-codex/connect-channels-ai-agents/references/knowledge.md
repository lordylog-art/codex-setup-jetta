# Bases de conhecimento

Fonte atual: A@8492.ea311dabe5541af9.js e M@main.c1b6a1d22d66025d.js na pasta técnica. Serviço M@3644148–3652577/módulo37244. Até50 knowledgeIds por agente. GUI implementa **FILE, TABLE, QA**; URL existe em enum/rota, mas A@646732 contém só placeholder. Não criar crawler por inferência.

## Recursos e metadata

Metadata `{name:name.trim(),description:description.trim(),type}`. Nome/descrição obrigatórios no formulário; limites50/500. A@86690–89000. Criação da base vazia não prova conteúdo indexado. Vincule a base pronta por `promptConfig.knowledgeIds`; fornecer array substitui lista inteira.

| Operação | Endpoint |
|---|---|
| Listar/criar | GET/POST `/ai/v1/aiKnowledge` |
| Ler/atualizar metadata | GET/PUT `/ai/v1/aiKnowledge/{id}` |
| Lote | GET `/ai/v1/aiKnowledge/batch?ids={id}&ids={id}` |
| Conteúdos | GET `/ai/v1/aiKnowledge/{id}/content?page=1&pageSize=50` |
| Conteúdo individual | GET `/ai/v1/aiKnowledge/{id}/content/{contentId}` |
| Adicionar arquivo | POST `/ai/v1/aiKnowledge/{id}/content/file`, `{name,fileId}` |
| Alterar arquivo | PUT `/ai/v1/aiKnowledge/{id}/content/{contentId}/file`, `{name,fileId}` |
| Visibilidade | PUT `/ai/v1/aiKnowledge/{id}/content/{contentId}/visibility`, `{visible}` |
| Excluir conteúdo | DELETE `/ai/v1/aiknowledge/{id}/content/{contentId}` |
| Validar arquivamento da base | GET `/ai/v1/aiKnowledge/{id}/archive-validation` (não validação de upload) |
| Arquivar/reativar/duplicar | DELETE `/ai/v1/aiKnowledge/{id}`; POST `/{id}/reactivate` ou `/{id}/duplicate` com `{}` |

Use o helper para `knowledge-read` e `knowledge-contents`. Demais contratos podem usar `new AgentClient().request(method,path,body)` exportado por scripts/agents.mjs dentro de script local específico do pedido, com journal antes de mutação, readback e sem retry cego. Não imprimir respostas brutas. O helper de agentes não implementa automaticamente todos CRUDs desta tabela.

## Arquivo e texto

A@583558 aceita `.docx,.txt,.pdf,.xls,.xlsx,.csv,.md`, múltiplos arquivos. M@4042618 rejeita>209715200 bytes (200MiB). DOC aparece em documentação histórica, mas não no accept atual. Não usar enum filetype/URL como prova de suporte.

Upload recuperado e já implementado no helper puro `C:/Scripts/ERP JETTA/tools/connect-agent-factory/extension/knowledge-upload.mjs`, função `orchestrateKnowledgeFileUpload(job,executeStep)`:

1. POST `/core/v1/file/upload`, `{name,type,mimeType}` → URL assinada/metadados.
2. PUT binário na urlUpload com Content-Type apropriado; **sem Authorization da Connect**, sem redirects.
3. PUT `/core/v1/file`, `{name,originalName,type,mimeType,extension,keyS3,generateThumb:false}` → ID.
4. POST `/ai/v1/aiKnowledge/{knowledgeId}/content/file`, `{name,fileId}`.

O executor injetado separa CONNECT_JSON e SIGNED_BINARY. Reutilizar a lógica exige adaptar os envelopes esperados pelo helper e usar arquivo/journal do pedido; não assume instalação da extensão Chrome. O módulo sozinho não certifica upload/provedor. Valide resposta HTTPS e preserve URLs/chaves assinadas fora de logs.

Texto livre A@581220/A@619375 vira File/Blob text/plain e percorre upload normal; não há endpoint “texto” deduzido. Formulário exige name/description não whitespace; conteúdo vem do texto. Após mudança de conteúdo, a UI faz PUT adicional de metadata para atualizar updatedAt (serviço `_touchKnowledgeAfterContentChange`); HTTP não deve presumir refresh automático idêntico.

Status da base: PENDING_PROCESSING, READY, FAILED. Conteúdo: DRAFT, QA_PROCESSING, QA_COMPLETED, QA_FAILED, VECTOR_PROCESSING, VECTOR_FAILED, READY. Acompanhe até estado final com prazo finito; upload200 não implica indexação. Em resultado incerto, reconcilie fileId/conteúdo antes de reenviar.

## FAQ manual e Q&A extraído

| Operação | Contrato |
|---|---|
| Criar worksheet manual | POST `/ai/v1/aiKnowledge/{id}/content/qa-worksheet`, `{}` |
| Ler | GET `/ai/v1/knowledgeContentQA/{contentId}` |
| Gravar worksheet inteira | PUT `/ai/v1/knowledgeContentQA/{contentId}/content`, `[{question,answer,keywords:[]}]` |
| Excluir linha | DELETE `/ai/v1/knowledgeContentQA/{contentId}/row/{rowId}` |
| Exportar planilha | POST `/ai/v1/knowledgeContentQA/{contentId}/export-spreadsheet`, `{totalItems}` |
| Q&A extraído do arquivo | GET `/ai/v1/aiKnowledge/qa-pairs/{knowledgeId}` → questions/answers |

A@568827 salva array completo: preserve pares existentes ao editar. Null vira string vazia no cliente; isso não prova backend aceitar linha vazia. Extratos de arquivos são somente leitura no guia, distintos da worksheet editável. Exportação cria recurso externo/artefato; só executar se pedido incluir isso.

## Tabela

GET/POST `/ai/v1/AiTable`; GET `/ai/v1/aitable/{tableId}`; PUT `/ai/v1/AiTable/{tableId}`; DELETE correspondente. Ler colunas/records com GET `/ai/v1/aitable/{tableId}/column` e `/record`, seguindo paginação.

A@638410 save:

```text
{name,description,
 columns:[{id?,name,type,active,description,order,tableId,createdAt,updatedAt}],
 records:[{id?,tableId,data,createdAt,updatedAt,active}]
}
```

Preserve IDs/linhas/ordem ao editar; excluir de um array substituído pode apagar dados. Tipos expressamente mapeados: TEXT,LONGTEXT,NUMBER,DECIMAL,CURRENCY,DATE,DATETIME,BOOLEAN,LINK,FILES,IMAGES. TIME/FILE aparecem em switch de conversão, mas não são tipos selecionáveis comprovados nesse recorte. Sem máximo comprovado de linhas/colunas; pageSize100000 não é limite de armazenamento.

O save UI converte número inválido→0 e datas inválidas/vazias→agora; não reproduza perda silenciosa quando o pedido pretende preservar dados. Peça/construa valor válido ou mantenha o existente. Boolean/multiselect/files precisam manter formato nativo. Conversões de tipo que perdem dados não são implicadas por “editar descrição da base”.

## Teste e arquivamento

Teste exclusivo da base: POST `/ai/v1/aiKnowledge/{id}/ask`, `{question,allMessages,executionId}`. Respostas podem vir por websocket AI_AGENT_KNOWLEDGE_BASE_STREAMING correlacionado por executionId. HTTP200 isolado não comprova resposta completa. Chamada consome IA; não executar nesta investigação.

Archive validation e dependências atuais devem anteceder arquivamento. Documentação inclui agentes arquivados entre vínculos que bloqueiam a base. Esta skill não usa DELETE como cleanup implícito.
