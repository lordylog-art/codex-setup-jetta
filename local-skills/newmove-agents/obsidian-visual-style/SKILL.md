---
name: obsidian-visual-style
description: "Style the Mega Brain vault when organizing folders or setting colors, icons, and evidence-based status cues."
---

# Obsidian Visual Style

Apply this skill only to `Mega Brain/Mega Brain`, the Obsidian vault. It does not govern ERP product UI or application code.

## Visual rules

- Use the installed **Iconocolor** plugin for folder colors and icons. Its settings live in `Mega Brain/Mega Brain/.obsidian/plugins/iconocolor/data.json`.
- Keep category colors and icons in that settings file. Use the existing `Jetta Pastel` palette and extend it when adding a new top-level category.
- Use green `#3F9A67` only for work explicitly marked complete; red `#C94F5C` for explicit pending or blocked work; amber `#D4A64A` for explicit in-progress work; muted gray `#87919B` for archived work.
- Determine status from clear note content, frontmatter, or an explicit status marker. Do not infer completion from age, folder name, or silence. Leave mixed or unclear folders with their category color; color a narrower folder only when all its relevant items share that status.
- Apply status colors only while the corresponding folder exists and its current notes still support that status. No folder is green until completion is recorded.
- Use distinct Lucide icons for top-level categories and feature areas. Prefer a restrained, readable explorer: small icons, subtle folder backgrounds, and no automatic rainbow assignment.
- Do not add a second plugin that styles the same file tree. **File Color** is retained as a disabled rollback option; **Iconocolor** is the active styling source.

## Safe updates

1. Read the current vault instructions and inspect the affected notes/folders before assigning status styles.
2. Preserve note content and unrelated Obsidian settings. Change appearance settings only for a visual request or when a folder's organization changes.
3. On a fresh install before Iconocolor has loaded, seed `data.json` before the first reload. For later updates, confirm Obsidian is closed or use its UI/connected API. Preserve existing settings, use the installed plugin's supported schema, and validate the JSON plus every referenced vault-relative path.
4. After installing or changing plugin configuration, reload Obsidian. Report when visual rendering still needs that reload.

Done means the intended folders have clear, evidence-based statuses; their color/icon settings are saved without changing note content; and the config parses with valid vault-relative paths.
