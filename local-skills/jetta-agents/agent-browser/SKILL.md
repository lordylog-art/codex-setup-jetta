---
name: agent-browser
description: Automates browser and Electron app interactions for user-flow validation.
---

# Browser Automation with agent-browser

## One-time setup (fresh machines)

If you see an error like "Executable doesn't exist ... chrome-headless-shell", install the bundled Chromium:

```bash
agent-browser install
```

## Quick start

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Core workflow

1. Navigate: `agent-browser open <url>`
2. Snapshot: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes

## Command chaining

Commands can be chained with `&&` in a single shell invocation. The browser persists between commands via a background daemon, so chaining is safe and more efficient than separate calls.

```bash
# Chain open + wait + snapshot in one call
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i

# Chain multiple interactions
agent-browser fill @e1 "user@example.com" && agent-browser fill @e2 "password123" && agent-browser click @e3

# Navigate and capture
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser screenshot page.png
```

**When to chain:** Use `&&` when you don't need to read the output of an intermediate command before proceeding (e.g., open + wait + screenshot). Run commands separately when you need to parse the output first (e.g., snapshot to discover refs, then interact using those refs).

## Ref lifecycle (important)

Refs (`@e1`, `@e2`, etc.) are invalidated when the page changes. Always re-snapshot after:

- Clicking links or buttons that navigate
- Form submissions
- Dynamic content loading (dropdowns, modals)

```bash
agent-browser click @e5              # Navigates to new page
agent-browser snapshot -i            # MUST re-snapshot
agent-browser click @e1              # Use new refs
```

## Required checks and cleanup
1. Screenshots are required for UI testing. Text snapshots do not catch layout issues, styling problems, alignment, z-index issues, etc. Always use `agent-browser screenshot --annotate` to get numbered element labels overlaid on the screenshot, which enables both visual verification and immediate interaction via refs.
2. **Use a single browser session.** Do not create multiple `--session` names — each spawns a separate Chromium process (~300MB RAM). Use one session and call `agent-browser open <new-url>` to navigate between pages within it. If you must create a new session, close the previous one first with `agent-browser --session <name> close`. **Exception:** When controlling multiple Electron apps simultaneously on different CDP ports, multiple named sessions are acceptable — but only when the user explicitly needs it, and each session must be closed when no longer needed.
3. When done, close your browser with `agent-browser close` (or `agent-browser --session <name> close`) to free resources.
4. **Electron apps: quit first.** If the Electron app is already running, you must quit it completely before relaunching with `--remote-debugging-port`. The flag only takes effect at launch time.

## On-demand details

- For command syntax, selectors, navigation, network, storage, settings, JavaScript, configuration or options, read the relevant heading in [references/commands.md](references/commands.md).
- For annotated screenshots, waits, authentication/state, persistence, debugging, HTTPS, local files, iOS or Electron/CDP automation, read the relevant heading in [references/advanced.md](references/advanced.md).
- Before session/auth operations, read their persistence/cleanup rules; before Electron launch or CDP connection, read its launch and color-scheme rules. Keep the required checks above active.
