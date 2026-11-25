# Barrinha flutuante aprovada

Este é o pacote canônico global da barrinha aprovada em 11/11/2026, originada em `D:/Projetos/Plataforma-Chatbot/apps/web/app/chatbot-send-prototype-studio.tsx` e no CSS adjacente. Reutilize estes arquivos em todos os projetos; não reconstrua a barra a partir de descrição, imagem ou código novo. Preserve controles, ordem, ícones, proporções, menus e comportamento. Somente pedido explícito do usuário autoriza alterar a barrinha.

## Arquivos e uso

- `floating-studio.html`: demonstração funcional independente, com o mesmo componente/CSS e runtime embutidos; abre offline e usa somente dados sintéticos em memória.
- `floating-studio.js` + `chatbot-send-prototype-studio.css`: pacote para inserir a barrinha em HTML ou outra aplicação sem depender do framework do host.
- `chatbot-send-prototype-studio.tsx` + CSS: cópia canônica exata da implementação aprovada, para aplicações React. O nome histórico do componente não exige um produto de chatbot.
- `adapter.mjs`, `preview.js`, `build.cjs`: montagem genérica, exemplo isolado e geração dos artefatos. O preview é um exemplo de integração, não um layout obrigatório para o produto.
- `SHA256SUMS`: hashes do snapshot e dos artefatos derivados.

Em React, copie ambos os arquivos canônicos e importe `ChatbotSendPrototypeStudio` do TSX. Preserve a implementação: adapte dados e callbacks no host. O tipo `ChatbotSendPrototypeStudioProps` documenta o contrato completo. O componente recebe `variant`, `onVariantChange`, `scenario`, `onScenarioChange`, `scenarios`, `steps`, `scope`, `onReset` e callbacks opcionais de status, tema e velocidade. `scope.current` aponta para a área de produto usada para localizar os alvos e desenhar o cursor. Monte a barra fora do modal; os ancestrais devem permitir que ela fique acima da interface.

Em HTML, inclua o CSS canônico e `floating-studio.js`, crie um contêiner irmão da área de produto e use:

```js
const studio = PrototypeFloatingStudio.mount(container, props);
studio.update({scenario: novoCenario, steps: novosPassos});
studio.unmount();
```

O adapter mantém o componente original sem alterar sua lógica. O host fornece fixtures, ações e referências DOM; seletores de `steps` são resolvidos dentro de `scope.current`. Os callbacks devem atualizar as props via `update`, pois a API é controlada pelo host. Estilos do host não devem sobrescrever as classes `chatbot-send-demo-*`; tokens `--wa-*` precisam preservar a paleta aprovada. O HTML demonstra a configuração desses tokens. A barra mantém o dropdown original com cinco variantes e seus nomes aprovados; não invente rótulos/quantidade novos sem tratar a alteração solicitada no contrato.

Nunca conecte esta demonstração a envios, agenda, persistência, serviços ou credenciais reais por padrão. Reusar a barra não autoriza efeitos externos. O bundle inclui React próprio; aplicações React podem preferir o TSX para usar seu runtime existente.

## Atualização autorizada

Após um pedido explícito de alteração da barrinha, valide a implementação, atualize os dois arquivos canônicos sem mudar seus bytes e gere novamente os derivados usando uma instalação existente de TypeScript, React, React DOM e o webpack compilado do Next:

```powershell
node C:/Users/caila/.agents/skills/prototype/assets/floating-studio/build.cjs D:/Projetos/Plataforma-Chatbot
```

O build não baixa pacotes e não altera o projeto usado como toolchain. O HTML e o bundle entregues dispensam essa instalação para uso. Confira os hashes e teste o HTML gerado antes de registrar a atualização em memória.
