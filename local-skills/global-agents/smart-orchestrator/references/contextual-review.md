# Revisão contextual

Use junto ao protocolo especialista instalado: Implement governa execução e validade das provas; Code Review governa Standards/Spec; QA Visual, Nosso Design, Impeccable e Storybook conservam todas as obrigações aplicáveis. Esta política decide quando e qual recorte revisar, sem substituir esses protocolos.

## Momento e responsabilidade

| Situação | Ação e conclusão permitida |
|---|---|
| Implementação em andamento | Autor executa exemplos discriminantes, testes e verificações locais. Autoverificação não é revisão independente. |
| Risco antecipado de contrato, arquitetura ou segurança | Revisão focal antecipada da decisão/contrato; não declarar QA funcional nem aceite do incremento incompleto. |
| Incremento maduro | Comparar escopo concluído com maturidade e critérios planejados; convocar revisão exigida pelo risco ou contrato. |
| Baixo risco | Autoverificação/revisão focal quando o protocolo permitir; reviewer adicional só por obrigação ou risco concreto. |
| Médio risco | Revisão conjunta; separar Standards/Spec quando acoplamento, ambiguidade ou fronteiras justificar independência. |
| Alto risco | Revisão independente focal das fronteiras afetadas; Standards e Spec podem compor o mesmo parecer. Separar avaliadores apenas quando exigido explicitamente ou por riscos distintos demonstrados; provas pertinentes do mecanismo real. |
| Integração pronta | Titular único conecta incrementos conforme dependências; validar fronteiras e regressões afetadas. Aprovação local não certifica integração. |
| Gates obrigatórios válidos, integração provada, achados materiais resolvidos | Aceitar e encerrar; sugestões opcionais não reabrem a entrega. |

Sem reviewer independente disponível, registrar bloqueio da etapa que o exige. Mantenha aprovações humanas previstas, inclusive aprovação visual; seleção do workflow não autoriza implementação, CI, deploy ou publicação além do pedido.

## Ciclo conduzido pelo implementador

Ao selecionar e chamar reviewers, aplique a regra de modelo de [Delegação](../SKILL.md#delegação), inclusive nas reavaliações.

Por padrão, o implementador conduz o ticket até candidato revisado: implementa, executa provas locais, chama os reviewers exigidos como subagentes filhos somente leitura, recebe achados diretamente, corrige e pede aos mesmos reviewers a reavaliação do delta e impactos. Congele o candidato durante cada revisão; retome escritas após os pareceres. Reviewer filho continua distinto do autor; preserve os modos e a independência exigidos pelo risco/protocolo.

Conduza esse ciclo sem devolver cada achado ao principal para redistribuição. Mantenha provas, achados e transições no controlador/registro existente, com as identidades reais dos avaliadores. Retorne candidato/base, arquivos, provas por critério, pareceres e limitações quando os gates dessa etapa estiverem válidos e os achados materiais resolvidos; integração e aceite final permanecem com os responsáveis designados.

Acione o principal para decisão fora do escopo/contrato, conflito de ownership/dependências, necessidade de slots/recursos ou bloqueio sem solução dentro da autorização. Use apenas a capacidade confirmada para filhos; se a ferramenta impedir delegação pelo implementador, o principal disponibiliza o reviewer e mantém a conversa direta entre autor e avaliador. Falha repetida continua exigindo hipótese discriminante e menor prova útil, sem repetição indefinida nem aceite presumido.

## Pacote do reviewer

Entregar referências canônicas da SPEC, decisões e critérios pertinentes; escopo concluído e maturidade; obrigações futuras com ticket de destino; dependências pendentes; base/candidato e diff completo relevante (incluindo trabalho sujo/novos arquivos); contratos e consumidores afetados; riscos; provas anteriores com alcance, ambiente e validade. Congele o recorte ou suspenda conclusões atingidas por edição concorrente.

O reviewer responde por que revisa, qual superfície cobre, quem avalia, profundidade, evidências reutilizadas e condições para repetir/encerrar. Cada achado material inclui ID, critério/regra, evidência verificável, cenário, impacto e ação necessária. Separe:

- **Defeito:** obrigação desta etapa demonstravelmente incorreta.
- **Implementação futura:** obrigação atribuída a outro incremento; conferir destino e gate final, sem exigir conclusão local nem dispensar aceite final.
- **Infraestrutura:** ambiente impede a prova; registrar bloqueio/diagnóstico, sem PASS nem bug de produto presumido.
- **Lacuna de prova:** obrigação sem evidência suficiente; indicar a menor superfície necessária.
- **Sugestão opcional:** melhoria sem violação obrigatória; não bloquear encerramento.

## Correção e validade

Consolidar achados, priorizar bloqueadores e corrigir causa. Para revisão do delta, informar comportamento/causa, invariante preservada, estados/consumidores relacionados e menor cenário de regressão. Reutilizar reviewers mobilizados e provas equivalentes; revisar o delta e impactos relacionados. Uma linha pode afetar autorização ou estado compartilhado: tamanho não define risco.

| Mudança | Revalidação |
|---|---|
| Focal | Invalidar provas cujo código, configuração, ambiente, critério ou consumidores foram afetados; preservar as demais com justificativa verificável. |
| Estrutural/contrato compartilhado | Ampliar alcance a consumidores, fronteiras e integração atingidos; invalidar provas materialmente comprometidas. |
| Segurança/autorização | Preservar gate obrigatório de segurança, revisão e integração pertinentes; revalidar efeitos, identidade, revogação e caminhos alternativos atingidos. |
| Somente infraestrutura | Atualizar prova dependente do ambiente restaurado; conservar achados/provas de produto ainda válidos. |

Cada prova vincula artefato e identificador ao candidato, arquivos pertinentes, configuração, ambiente sanitizado, comando/interação, resultado e limitações. Hash detecta alteração dos arquivos declarados; agente responde pela completude da declaração e equivalência semântica. Screenshot, HTTP 2xx, mocks ou inspeção estática sozinhos não provam uma fronteira real não exercitada.

Achado resolvido só reabre com nova evidência ou mecanismo de regressão. Repetição da mesma falha sem nova informação pede consolidação, hipótese discriminante e menor teste útil; estagnação não aprova código. Ampliar revisão apenas por nova superfície, mudança estrutural, risco novo, prova invalidada ou obrigação explícita.
