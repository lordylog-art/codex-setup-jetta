# Annotated screenshots (vision mode)

Use `--annotate` to take a screenshot with numbered labels overlaid on interactive elements. Each label `[N]` maps to ref `@eN`. This also caches refs, so you can interact with elements immediately without a separate snapshot.

```bash
agent-browser screenshot --annotate
# Output includes the image path and a legend:
#   [1] @e1 button "Submit"
#   [2] @e2 link "Home"
#   [3] @e3 textbox "Email"
agent-browser click @e2              # Click using ref from annotated screenshot
```

Use annotated screenshots when:
- The page has unlabeled icon buttons or visual-only elements
- You need to verify visual layout or styling
- Canvas or chart elements are present (invisible to text snapshots)
- You need spatial reasoning about element positions

## Timeouts and slow pages

The default Playwright timeout is 60 seconds for local browsers. For slow websites or large pages, use explicit waits instead of relying on the default timeout:

```bash
agent-browser wait --load networkidle      # Wait for network activity to settle (best for slow pages)
agent-browser wait "#content"              # Wait for a specific element to appear
agent-browser wait @e1                     # Wait for element by ref
agent-browser wait --url "**/dashboard"    # Wait for URL pattern (useful after redirects)
agent-browser wait --fn "document.readyState === 'complete'"  # Wait for JS condition
agent-browser wait 5000                    # Wait fixed duration (milliseconds) as last resort
```

When dealing with consistently slow websites, use `wait --load networkidle` after `open` to ensure the page is fully loaded before taking a snapshot.

## Example: Form submission

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output shows: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## Example: Authentication with saved state

```bash
# Login once
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Later sessions: load saved state
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## Session persistence

```bash
# Auto-save/restore cookies and localStorage across browser restarts
agent-browser --session-name myapp open https://app.example.com/login
# ... login flow ...
agent-browser close  # State auto-saved to ~/.agent-browser/sessions/

# Next time, state is auto-loaded
agent-browser --session-name myapp open https://app.example.com/dashboard

# Encrypt state at rest
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
agent-browser --session-name secure open https://app.example.com

# Manage saved states
agent-browser state list
agent-browser state show myapp-default.json
agent-browser state clear myapp
agent-browser state clean --older-than 7
```

## Sessions (parallel browsers)

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

Always close your browser session when done to avoid leaked processes:

```bash
agent-browser close                    # Close default session
agent-browser --session test1 close    # Close specific session
```

If a previous session was not closed properly, the daemon may still be running. Use `agent-browser close` to clean it up before starting new work.

## Data extraction

```bash
agent-browser open https://example.com/products
agent-browser snapshot -i
agent-browser get text @e5           # Get specific element text
agent-browser get text body > page.txt  # Get all page text

# JSON output for parsing
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

## Connect to existing Chrome

```bash
# Auto-discover running Chrome with remote debugging enabled
agent-browser --auto-connect open https://example.com
agent-browser --auto-connect snapshot

# Or with explicit CDP port
agent-browser --cdp 9222 snapshot
```

## Local files (PDFs, HTML)

```bash
# Open local files with file:// URLs
agent-browser --allow-file-access open file:///path/to/document.pdf
agent-browser --allow-file-access open file:///path/to/page.html
agent-browser screenshot output.png
```

## iOS Simulator (Mobile Safari)

```bash
# List available iOS simulators
agent-browser device list

# Launch Safari on a specific device
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com

# Same workflow as desktop - snapshot, interact, re-snapshot
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1          # Tap (alias for click)
agent-browser -p ios fill @e2 "text"
agent-browser -p ios swipe up         # Mobile-specific gesture

# Take screenshot
agent-browser -p ios screenshot mobile.png

# Close session (shuts down simulator)
agent-browser -p ios close
```

**Requirements:** macOS with Xcode, Appium (`npm install -g appium && appium driver install xcuitest`)

**Real devices:** Works with physical iOS devices if pre-configured. Use `--device "<UDID>"` where UDID is from `xcrun xctrace list devices`.

## Debugging

```bash
agent-browser --headed open example.com   # Show browser window
agent-browser --cdp 9222 snapshot         # Connect via CDP port
agent-browser connect 9222                # Alternative: connect command
agent-browser console                     # View console messages
agent-browser console --clear             # Clear console
agent-browser errors                      # View page errors
agent-browser errors --clear              # Clear errors
agent-browser highlight @e1               # Highlight element
agent-browser trace start                 # Start recording trace
agent-browser trace stop trace.zip        # Stop and save trace
agent-browser record start ./debug.webm   # Record video from current page
agent-browser record stop                 # Save recording
agent-browser profiler start              # Start Chrome DevTools profiling
agent-browser profiler stop trace.json    # Stop and save profile
```

## HTTPS Certificate Errors

For sites with self-signed or invalid certificates:
```bash
agent-browser open https://localhost:8443 --ignore-https-errors
```

## Electron App Automation

Automate any Electron desktop app using agent-browser. Electron apps are built on Chromium and expose a Chrome DevTools Protocol (CDP) port that agent-browser can connect to, enabling the same snapshot-interact workflow used for web pages.

### Core Workflow

1. **Launch** the Electron app with remote debugging enabled
2. **Connect** agent-browser to the CDP port
3. **Snapshot** to discover interactive elements
4. **Interact** using element refs
5. **Re-snapshot** after navigation or state changes

```bash
# Launch an Electron app with remote debugging
open -a "Slack" --args --remote-debugging-port=9222

# Connect agent-browser to the app
agent-browser connect 9222

# Standard workflow from here
agent-browser snapshot -i
agent-browser click @e5
agent-browser screenshot slack-desktop.png
```

### Launching Electron Apps with CDP

Every Electron app supports the `--remote-debugging-port` flag since it's built into Chromium.

#### macOS

```bash
# Slack
open -a "Slack" --args --remote-debugging-port=9222

# VS Code
open -a "Visual Studio Code" --args --remote-debugging-port=9223

# Discord
open -a "Discord" --args --remote-debugging-port=9224

# Figma
open -a "Figma" --args --remote-debugging-port=9225

# Notion
open -a "Notion" --args --remote-debugging-port=9226

# Spotify
open -a "Spotify" --args --remote-debugging-port=9227
```

#### Linux

```bash
slack --remote-debugging-port=9222
code --remote-debugging-port=9223
discord --remote-debugging-port=9224
```

#### Windows

```bash
"C:\Users\%USERNAME%\AppData\Local\slack\slack.exe" --remote-debugging-port=9222
"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe" --remote-debugging-port=9223
```

**Important:** If the app is already running, quit it first, then relaunch with the flag. The `--remote-debugging-port` flag must be present at launch time.

### Connecting to Electron Apps

```bash
# Connect to a specific port
agent-browser connect 9222

# Or use --cdp on each command
agent-browser --cdp 9222 snapshot -i

# Auto-discover a running Chromium-based app
agent-browser --auto-connect snapshot -i
```

After `connect`, all subsequent commands target the connected app without needing `--cdp`.

### Tab Management

Electron apps often have multiple windows or webviews. Use tab commands to list and switch between them:

```bash
# List all available targets (windows, webviews, etc.)
agent-browser tab

# Switch to a specific tab by index
agent-browser tab 2

# Switch by URL pattern
agent-browser tab --url "*settings*"
```

### Common Electron Patterns

#### Inspect and Navigate an App

```bash
open -a "Slack" --args --remote-debugging-port=9222
sleep 3  # Wait for app to start
agent-browser connect 9222
agent-browser snapshot -i
# Read the snapshot output to identify UI elements
agent-browser click @e10  # Navigate to a section
agent-browser snapshot -i  # Re-snapshot after navigation
```

#### Take Screenshots of Desktop Apps

```bash
agent-browser connect 9222
agent-browser screenshot app-state.png
agent-browser screenshot --full full-app.png
agent-browser screenshot --annotate annotated-app.png
```

#### Extract Data from a Desktop App

```bash
agent-browser connect 9222
agent-browser snapshot -i
agent-browser get text @e5
agent-browser snapshot --json > app-state.json
```

#### Fill Forms in Desktop Apps

```bash
agent-browser connect 9222
agent-browser snapshot -i
agent-browser fill @e3 "search query"
agent-browser press Enter
agent-browser wait 1000
agent-browser snapshot -i
```

#### Run Multiple Apps Simultaneously

Use named sessions **only** when you need to control multiple Electron apps at the same time. Each session spawns a separate Chromium process (~300MB RAM), so only create multiple sessions when explicitly required and close each one when done.

```bash
# Connect to Slack
agent-browser --session slack connect 9222

# Connect to VS Code
agent-browser --session vscode connect 9223

# Interact with each independently
agent-browser --session slack snapshot -i
agent-browser --session vscode snapshot -i

# Close sessions when done
agent-browser --session slack close
agent-browser --session vscode close
```

### Color Scheme

Playwright overrides the color scheme to `light` by default when connecting via CDP. To preserve dark mode:

```bash
agent-browser connect 9222
agent-browser --color-scheme dark snapshot -i
```

Or set it globally:

```bash
AGENT_BROWSER_COLOR_SCHEME=dark agent-browser connect 9222
```

### Electron Troubleshooting

#### "Connection refused" or "Cannot connect"

- Make sure the app was launched with `--remote-debugging-port=NNNN`
- If the app was already running, quit and relaunch with the flag
- Check that the port isn't in use by another process: `lsof -i :9222`

#### App launches but connect fails

- Wait a few seconds after launch before connecting (`sleep 3`)
- Some apps take time to initialize their webview

#### Elements not appearing in snapshot

- The app may use multiple webviews. Use `agent-browser tab` to list targets and switch to the right one
- Use `agent-browser snapshot -i -C` to include cursor-interactive elements (divs with onclick handlers)

#### Cannot type in input fields

- Try `agent-browser keyboard type "text"` to type at the current focus without a selector
- Some Electron apps use custom input components; use `agent-browser keyboard inserttext "text"` to bypass key events

