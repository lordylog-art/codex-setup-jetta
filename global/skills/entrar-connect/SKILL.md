---
name: entrar-connect
description: Abrir o Connect Channels no Chrome controlavel com Playwright/CDP, reutilizar um perfil dedicado para manter login e perguntar ao usuario o que ele quer fazer antes de operar o site. Use quando o usuario pedir para entrar, acessar, controlar, clicar, consultar, testar ou interagir com https://app.connectchannels.com.br/ pela sessao do navegador, sem expor senha, token ou 2FA.
---

# Entrar Connect

## Objetivo

Entrar no Connect Channels por uma instancia do Chrome controlavel, mantendo a sessao em um perfil dedicado e persistente. Nunca pedir, ler ou registrar senha, token, cookie ou codigo 2FA; se o site pedir autenticacao, orientar o usuario a fazer manualmente na janela aberta.

## Fluxo Padrao

1. Abrir ou reutilizar o Chrome controlavel com `scripts/Start-ConnectChannelsChrome.ps1`.
2. Confirmar que `http://127.0.0.1:9222/json/version` responde.
3. Conectar via Playwright:

```js
var pw = await import('playwright');
var browser = await pw.chromium.connectOverCDP('http://127.0.0.1:9222', { timeout: 10000 });
var context = browser.contexts()[0];
var page = context.pages().find(p => p.url().includes('connectchannels')) || context.pages()[0];
```

4. Ler apenas o necessario da tela atual: URL, titulo e texto visivel curto.
5. Se a URL estiver em `/auth/sign-in`, parar e pedir para o usuario logar manualmente na janela controlavel. Depois que ele disser que logou, reconectar e continuar.
6. Se a URL estiver em `/chat2/sessions` ou outra rota interna, informar brevemente onde esta e perguntar: "O que voce quer fazer no Connect Channels agora?"
7. Aguardar o objetivo do usuario antes de clicar, preencher, navegar para areas sensiveis ou executar qualquer acao operacional.

## Pergunta Inicial Obrigatoria

Quando o usuario pedir apenas para "entrar", "abrir" ou "usar" o Connect Channels sem objetivo especifico, nao assumir a tarefa. Depois de validar que a sessao esta aberta, perguntar de forma curta o que ele quer fazer.

Exemplos de pergunta:

- "Estou dentro do Connect Channels. O que voce quer fazer agora?"
- "Ja abriu em Atendimentos. Quer consultar conversa, responder alguem, ver relatorios, mexer em ajustes ou outra coisa?"

Se o usuario ja trouxe uma tarefa especifica, como "procura o atendimento do Joao" ou "ve os modelos de mensagem", executar essa tarefa sem fazer uma pergunta redundante.

## Perfil Dedicado

Usar por padrao o perfil que ja foi logado neste setup:

`C:\Users\Jetta\Documents\Codex\2026-06-19\consegue-usar-o-chrome-com-minha\work\chrome-connectchannels-profile`

Esse perfil existe para manter a sessao ja autenticada entre conversas. Nao apagar, copiar ou expor arquivos desse perfil. Se esse caminho deixar de existir, usar `C:\Users\Jetta\.codex\browser-profiles\connectchannels` como fallback e pedir para o usuario logar manualmente uma vez.

## Comandos Uteis

Abrir/reutilizar o navegador:

```powershell
& "C:\Users\Jetta\.codex\skills\entrar-connect\scripts\Start-ConnectChannelsChrome.ps1"
```

Checar CDP:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:9222/json/version -TimeoutSec 5
```

Listar abas via Playwright:

```js
var tabs = [];
for (var p of context.pages()) tabs.push({ url: p.url(), title: await p.title().catch(() => '') });
nodeRepl.write(JSON.stringify(tabs, null, 2));
```

## Regras de Seguranca

- Nao solicitar credenciais ao usuario.
- Nao exibir cookies, localStorage, tokens, headers sensiveis ou dados secretos.
- Nao enviar mensagens, alterar configuracoes, disparar campanhas ou executar acoes irreversiveis sem confirmacao explicita do usuario.
- Antes de enviar mensagem, mudar status, editar ajuste, criar template, alterar canal, disparar campanha ou executar acao com efeito externo, resumir a acao e pedir confirmacao.
- Para leitura de tela, limitar previews de texto ao necessario.
- Se houver logout, 2FA, CAPTCHA ou confirmacao sensivel, devolver o controle visual ao usuario e aguardar.

## Observacoes

O Chrome com perfil padrao do usuario pode nao liberar automacao mesmo com `--remote-debugging-port`. Quando isso acontecer, usar o perfil dedicado acima. O usuario ja logou no perfil padrao desta skill; se ele expirar, pedir login manual na janela controlavel e continuar depois.
