# Provas práticas desde a primeira rodada

## Preparar acesso e fixtures

Resolva capacidade de browser, autenticação e ferramentas uma vez. Respeite preferência de navegador; use alternativas oficiais isoladas quando autorizadas, sem recorrer a perfil pessoal ou integração rejeitada. Preserve uma sessão técnica dedicada sem invalidar a humana. Compartilhe capacidade operacional após resolver; não repita logins ou partidas concorrentes por peixinho. Para a primeira tentativa de uma persona de uso, compartilhe acesso e tarefa sem antecipar a solução ou explicar a implementação; registre qualquer assistência necessária conforme [perfis](profiles.md).

Observe o ambiente real antes de operar: localhost pode manter envios, integrações e agendadores reais. Para cada mutação de teste, identifique autorização vigente, ambiente explicitamente de teste, mutator responsável, namespace/IDs próprios e snapshots antes/depois. Coordene concorrência por recurso. Limpe/restaure apenas o que pertence à fixture; preserve alterações concorrentes, constraints, grants e ativações salvas. Não habilite permissões ou configurações só para obter verde.

Use dados fictícios para campos; envios só aos destinos e custos autorizados, verificando CC/cópias e destinatários derivados. A autorização de um teste anterior não vira autorização permanente da skill. Em resultado incerto, consulte tentativa/correlação antes de reenviar; limite retries para não duplicar efeitos nem custos. Bloqueio numa integração não suspende provas independentes.

## Cobrir o universo correto

Use inventário autoritativo de todas as operações/tenants/configurações aplicáveis. Registre cada uma na matriz, incluindo acesso negado esperado, configuração ausente, integração protegida, skip e impedimento. Uma amostra feliz não vale como cobertura do universo; se o conjunto for grande ou houver bloqueio, declare o restante sem prova.

Cruze regiões/estados/personas/operações com ações/endpoints e configurações relevantes. Inspecione cards, campos, botões, filtros, tabelas, gráficos, modais e mensagens, sem se limitar ao primeiro render. Inclua dados curtos e longos, campos faltantes/completos, formatos locais de telefone/placa/data, datas impossíveis, volume e documentos regulares/vencidos/incompletos. Para documento, o fluxo começa no arquivo/upload/análise quando essa é a jornada; seed de linha pronta só prova etapas posteriores.

## Evidência por fronteira

Exercite a ação de usuário e correlacione o resultado entre camadas autorizadas:

`ação esperada → clique/UI → request/resposta → fila/journal → DB → integração/provedor → estado final/reload`

Marque cada camada observada, simulada, inspecionada ou não verificada. Guarde request/correlation IDs, timestamps, resultados e capturas com dados sensíveis removidos. HTTP 200 prova somente o contrato observado: aceito não equivale a enfileirado, persistido, integração escrita, envio, entrega ou leitura. CLI/API não prova clique/UI; mock não prova integração real; seed não prova upload. Helper exercitado isoladamente não prova o consumidor: identifique o endpoint, componente ou job ativo que realmente o chama e se esse caminho foi executado antes de ampliar a conclusão. Se uma fronteira não puder ser testada, encerre a afirmação na última camada comprovada.

Observe invariantes além do sucesso: rejeição de data impossível antes da persistência, tabelas com texto extenso, universo correto dos KPIs, janela pós-commit/pré-dispatch, replay de eventos e invalidação após reconexão. São exemplos de investigação, não requisitos universais nem endpoints fixos.

## Carga e falhas

Comece por leitura de código, contratos e limites. Carga/injeção de falhas só onde ambiente, recursos e efeitos estiverem autorizados; mantenha produção e terceiros fora sem escopo específico. Defina recursos, duração, concorrência, volume e condição de parada antes de executar. Meça percentis, erros, vazão e consumo quando as ferramentas permitirem. Registre o que faltou medir. Uma suíte isolada e GETs seriados não provam carga sustentada, concorrência ou aceitação global.

## Validar o próprio teste

Antes de confirmar um bug, confira fonte/rota/CSS realmente ativos, fixture válida, precondições, permissão e contrato vigente, sequência temporal e dados antes/depois. Um estado posterior mais avançado que o esperado pode refutar a interpretação de falha. Separe bug do produto, problema de harness/fixture e impedimento ambiental. Reteste somente por falha, delta invalidante ou nova evidência; mantenha resultados brutos e explique diferenças de escopo.
