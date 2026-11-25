# Validação operacional

Execute `python -B -m unittest discover -s tests -v` na pasta da skill. O runner permanente usa Python padrão e o adaptador instalado, em diretórios temporários isolados. Não invoca agentes nem comprova a integração nativa sozinho.

Para repetir integração nativa, use uma fixture nova criada a partir de `tests/native_fixture.py`; preserve a execução anterior. Invoque esta skill sobre o Index da fixture, limite escrita a ela e despache T01, T02 e T03 com contextos novos. Verifique artefato esperado, persista checkpoint/aceite, e só então despache o sucessor. Guarde IDs reais, comandos e resultados em `tests/evidence`. Teste retomada com um agente novo que recebe apenas caminhos e contrato, sem histórico.

O helper não implementa tickets, não despacha modelos e não julga semântica. Aceite mecânico exige checkboxes, evidências existentes e imutáveis, validadores PASS e revisão declarada; o supervisor deve realizar a revisão antes de registrá-la. Não converta resultados mecânicos em prova semântica.

Capacidades e matriz T01–T15 observadas nesta instalação ficam em [relatório](../REPORT.md). NOT_TESTED não é PASS. Atualize o relatório após execução real, sem apagar limites anteriores que ainda se apliquem.

## Operação

`$feature-supervisor Projeto D:/newmove; feature <caminho absoluto do Index Obsidian>; modo somente leitura. Reconstrua estado e mostre a próxima ação elegível.`

Depois de reconciliar incompatibilidades e obter escopo de execução: `$feature-supervisor Supervise os tickets autorizados da mesma feature em modo direto, retomando checkpoints existentes.`

O helper suporta Index com `[[Tickets/stem]]`, bloqueadores YAML em lista de `[[Tickets/stem]]`, estados canônicos e seção `## Critérios de aceite` ou `## Acceptance Criteria`. Outros formatos permanecem legíveis pelo agente para diagnóstico, mas não são convertidos automaticamente. Evidências do helper ficam dentro da workspace sintética/canônica; para código fora dela, use um manifesto sanitizado de hashes e revalide suas fontes antes de aceitar. Não copie código/segredos para o vault.

`tests/test_isolation.py` executa helper e adaptador reais em subprocessos auditados: escritas Python fora da sandbox são recusadas, incluindo tentativas contra arquivos protegidos sintéticos. É isolamento verificável desse fluxo Python, não sandbox de segurança do sistema operacional. `tests/test_v2_integration.py` exercita Controller, checkpoints, recuperação em novo processo e sincronização pelos primitivos do adaptador. Atores/revisões de cenário são sintéticos; a prova nativa de agentes é separada.

A instalação mantém uma única fonte em `~/.codex/skills/feature-supervisor` e uma junction Windows em `~/.agents/skills/feature-supervisor`, para descoberta no diretório pessoal atual. Não copie ou mantenha versões divergentes. Política explícita permanece `allow_implicit_invocation: false`.

Não há promessa de execução 24/7. Um despertar após fechar o chat exigiria um mecanismo externo de agendamento ou nova invocação humana; nenhum foi instalado. Compactação é do runtime. A lista de skills de um chat aberto pode ser um snapshot: validar os arquivos não prova que o seletor da interface já os atualizou.
