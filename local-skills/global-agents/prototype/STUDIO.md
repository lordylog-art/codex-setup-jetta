# Demonstration studio

Apply this to both UI and logic prototypes by default, including single-file HTML demos. The delivered prototype itself contains the studio; an external browser script or a prerecorded animation alone does not satisfy this requirement. Reuse the [approved canonical bar](assets/floating-studio/README.md), including its HTML/JS/CSS and control order, in every project; do not rebuild or redesign it. Adapt the host product stage and demonstration data, preserving the bar. Explicit user changes to the bar take precedence.

## Controls and presentation

- Present the actual site or host application inside a product stage, preserving its surrounding UI and the component under evaluation. Mount the studio as a sibling or portal overlay with `position: fixed`, above the product in stacking order. It never reserves layout space, pushes the product down, becomes a panel in document flow, or enters a modal or its footer.
- Use a very thin, minimalist floating bar with **Play, a compact Protótipo dropdown when multiple prototypes exist, Cenário, Velocidade and a compact sun/moon icon toggle**. Play becomes Pause/Resume during playback. The Protótipo dropdown lists variants by number (1…N) and name; keep it separate from Cenário, which selects the active prototype's states and journeys. Use the prototype's language for labels. Keep additional controls contextual by default, while honoring any controls the user explicitly requests.
- The sun/moon button switches light/dark only for the prototype stage and product, with an accessible name describing the destination theme. Keep this preference in memory; never change the real application's saved theme.
- Keep Restart, Next, instructions, scenario notes and progress available contextually or through discoverable shortcuts unless the user requests otherwise. Announce the active step and completed, paused or failed states concisely; expose their details without adding a permanent panel or a second bar.
- Start only after the viewer presses Play. Keep manual exploration available; direct interaction with the demonstration pauses playback before handing over control.
- Make the bar freely draggable within the viewport, like the Codex floating chat. Drag its non-control surface; control interactions must remain clicks and selections. Clamp its position after dragging and viewport resize so it remains reachable, and support keyboard repositioning without hijacking product inputs. Move only the bar, never the OS window. Initially place it away from the primary action and fields being evaluated; the viewer can move it to uncover content. Keep controls compact and both dropdowns reachable on narrow or short screens, without reserving space in the product.
- Use accessible buttons, keyboard operation, visible keyboard focus and concise status announcements. Use `:focus-visible` for keyboard focus; do not use `:focus-within` or decorative field/card/selection outlines. Respect reduced motion by shortening cursor travel while preserving actions and readable step timing.

## Cursor and actual interactions

- Render a recognizable mouse pointer inside the prototype, with smooth travel, a visible click pulse and paced character-by-character typing. The cursor is a presentation layer with `pointer-events: none` and is hidden from assistive technology; it does not move the operating system pointer.
- Drive the same controls and handlers a person uses: open menus, focus fields, type, choose options, scroll, submit and dismiss messages as the flow requires. Rendering a moving cursor while directly replacing the final state is insufficient.
- Use stable semantic targets or explicit demo IDs. Resolve targets and their current bounds at each step, scroll them into view and wait for the expected UI state before continuing. Never rely on fixed screen coordinates.
- For typing, update the actual field and trigger its normal input/change handling, including controlled framework inputs. Call the application's interaction handlers where synthetic events cannot reproduce trusted browser behavior; clearly mark simulated file pickers or other unavailable native interactions.
- Bound waits. If a target disappears or the expected state fails to arrive, stop, identify the step and offer Restart; do not keep clicking blindly or silently mark completion.
- Pause must freeze pending actions, typing and waits. Restart, scenario/variant changes and unmount cancel the old run, timers and asynchronous continuations before resetting. Resume continues the paused step without duplicate submissions; Next executes exactly one step while paused. Permit only one run at a time.
- Keep ordered scenario steps and fixtures in one small shared definition used for both playback and manual walkthroughs. Reuse existing project mechanisms before adding a runner or dependency.

## Stress and error scenarios

Provide visible, selectable scenarios with deterministic fixtures, a known initial state, expected result and a recovery path. Show errors in the actual field, toast, list, modal or page where a user would encounter them. These are interactive states, not a static error gallery.

Cover the following categories wherever the flow supports them; adapt examples to the domain rather than inventing unrelated features:

| Category | Cases to demonstrate |
| --- | --- |
| Baseline | Successful complete journey, loading and empty state |
| Extreme content | Very long names and labels, unbroken email/URL/text, multiline descriptions, accents/emoji, missing optional values |
| Density and limits | Zero/one/many records, large counts, minimum/maximum numeric values, overflow in tables/cards/dialogs on narrow screens |
| Validation | Required field empty, invalid format, limit exceeded, conflicting fields, multiple simultaneous field errors |
| Long errors | A realistic multi-paragraph message and an unbroken technical detail; readable wrapping, scroll and accessible actions |
| Service failures | Slow response, offline/network failure, timeout and server failure where requests exist |
| Operation failures | Duplicate/conflict, stale data, permission/session failure or partial failure where the operation supports these outcomes |
| Recovery | Correct invalid data, retry after failure, cancel, return to the flow; retain entered values when appropriate and avoid duplicate submissions |

Every prototype includes a happy path, extreme content, a long error message and recovery. Add all other applicable categories for the modeled flow. If a category cannot occur in that prototype, briefly state why in the scenario notes instead of adding a fictitious capability. This catalog covers relevant failure classes, not a claim to reproduce every possible production fault.

Use synthetic, non-sensitive fixtures and in-memory adapters for failure injection. Label the studio as a simulation. Keep scenarios isolated from real writes, outbound messages, scheduled jobs and production services; preserve the host application's saved configuration. Existing read-only context may remain when authorized.

## Completion checks

Before delivery, exercise Play through completion, Pause/Resume during typing or a wait, Next, Restart during a run, and scenario/variant changes. Confirm canceled runs cannot mutate the new scenario. Check that manual use still works after playback.

Run representative extreme-content, long-error and recovery scenarios at desktop and narrow widths. Confirm the thin overlay bar exposes Play, Protótipo when applicable, Cenário, Velocidade and the sun/moon toggle, plus any explicitly requested controls. Verify every variant (1…N) is available with its name in Protótipo without entering Cenário. Dragging and viewport resize must keep the bar reachable without shifting the product, and its initial position must leave the primary action uncovered. Check both themes without changing the real saved preference. Confirm messages remain readable, actions reachable, fields usable and state reset repeatable. Use a small automated check for non-trivial runner logic where feasible; report any interaction or viewport not exercised. A simulated timeout demonstrates the prototype's UI, not real backend resilience.
