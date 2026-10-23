import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from spec_workspace import ResolutionError, resolve


class SpecWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.vault = self.base / "Vault"
        self.vault.mkdir()
        self.config = self.base / "obsidian.json"
        self.write_json(self.config, {"vaults": {"vault-id": {"path": str(self.vault)}}})
        self.plugin("folder-status", {"version": 1, "folders": {}})
        self.plugin("iconocolor", {"folderConfigs": {}})
        self.plugin("obsidian-file-color", {"palette": [{"id": "especificacoes", "value": "#729BCB"}], "fileColors": []})

    def tearDown(self):
        self.temp.cleanup()

    def write_json(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    def plugin(self, name, data):
        self.write_json(self.vault / ".obsidian" / "plugins" / name / "data.json", data)

    def test_no_reference_keeps_original_mode_and_creates_nothing(self):
        result = resolve("", self.config)
        self.assertEqual(result["mode"], "default")
        self.assertFalse((self.vault / "Spec Driven").exists())

    def test_obsidian_state_does_not_leak_into_next_default_invocation(self):
        note = self.vault / "Feature" / "Feature.md"
        note.parent.mkdir()
        note.write_text("# Feature\n", encoding="utf-8")
        first = resolve(str(note), self.config)
        second = resolve("", self.config)
        self.assertEqual(first["mode"], "obsidian")
        self.assertEqual(second["mode"], "default")
        self.assertIsNone(second["specDrivenDirectory"])

    def test_all_artifact_types_route_lazily(self):
        from spec_workspace import CATEGORIES, artifact_path

        workspace = self.vault / "Feature" / "Spec Driven"
        for kind, category in CATEGORIES.items():
            self.assertEqual(artifact_path(workspace, kind, "Sample"), workspace / category / ("Map.md" if kind == "map" else "sample.md"))
        self.assertFalse(workspace.exists())

    def test_integration_manifest_covers_every_installed_upstream_skill(self):
        root = Path(__file__).resolve().parents[4]
        lock = json.loads((root / "skills-lock.json").read_text(encoding="utf-8"))
        manifest = json.loads((root / ".agents/skills/spec-workspace/integration.json").read_text(encoding="utf-8"))
        installed = {name for name, data in lock["skills"].items() if data.get("source") == "mattpocock/skills"}
        classified = set(manifest["integratedSkills"]) | set(manifest["untouchedByDesign"])
        self.assertEqual(len(installed), 38)
        self.assertEqual(manifest["installedMattSkillCount"], len(installed))
        self.assertEqual(installed, classified)

    def test_every_integrated_skill_points_to_the_shared_adapter(self):
        root = Path(__file__).resolve().parents[4]
        manifest = json.loads((root / ".agents/skills/spec-workspace/integration.json").read_text(encoding="utf-8"))
        for name in manifest["integratedSkills"]:
            with self.subTest(skill=name):
                skill = (root / ".agents/skills" / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("spec-workspace/SKILL.md", skill)

    def test_note_path_creates_workspace_at_note_parent_and_registers_metadata(self):
        note = self.vault / "Projetos" / "Jetta Move" / "Disponibilidade.md"
        note.parent.mkdir(parents=True)
        note.write_text("# Disponibilidade\n", encoding="utf-8")
        result = resolve("Projetos/Jetta Move/Disponibilidade.md", self.config)
        self.assertEqual(result["rootDirectory"], "Projetos/Jetta Move")
        self.assertTrue((note.parent / "Spec Driven").is_dir())
        index = (note.parent / "Spec Driven" / "Index.md").read_text(encoding="utf-8")
        self.assertIn('source: "[[Projetos/Jetta Move/Disponibilidade.md]]"', index)
        status = json.loads((self.vault / ".obsidian/plugins/folder-status/data.json").read_text())
        self.assertEqual(status["folders"]["Projetos/Jetta Move/Spec Driven"], "pending")

    def test_folder_path_uses_the_folder_as_root(self):
        folder = self.vault / "Projetos" / "Jetta Move" / "Disponibilidade"
        folder.mkdir(parents=True)
        result = resolve(str(folder), self.config)
        self.assertEqual(result["rootDirectory"], "Projetos/Jetta Move/Disponibilidade")
        self.assertTrue((folder / "Spec Driven").is_dir())

    def test_obsidian_uri_resolves_spaces_and_reuses_legacy_workspace(self):
        root = self.vault / "Features" / "E-mail"
        note = root / "Feature.md"
        note.parent.mkdir(parents=True)
        note.write_text("# Feature\n", encoding="utf-8")
        legacy = root / "Specdriven"
        legacy.mkdir()
        result = resolve("obsidian://open?vault=Vault&file=Features%2FE-mail%2FFeature.md", self.config)
        self.assertEqual(result["specDrivenDirectory"], "Features/E-mail/Specdriven")
        self.assertFalse((root / "Spec Driven").exists())

    def test_uri_embedded_in_skill_invocation_is_detected(self):
        note = self.vault / "Projetos" / "Jetta Move" / "Disponibilidade.md"
        note.parent.mkdir(parents=True)
        note.write_text("# Feature\n", encoding="utf-8")
        uri = "obsidian://open?vault=Vault&file=Projetos%2FJetta%20Move%2FDisponibilidade.md"
        result = resolve(f"/spec {uri}\nCrie uma especificacao", self.config)
        self.assertEqual(result["sourcePath"], "Projetos/Jetta Move/Disponibilidade.md")

    def test_wikilink_without_markdown_extension_resolves(self):
        note = self.vault / "Projetos" / "Feature.md"
        note.parent.mkdir()
        note.write_text("# Feature\n", encoding="utf-8")
        result = resolve("[[Projetos/Feature]]", self.config)
        self.assertEqual(result["sourceType"], "note")
        self.assertEqual(result["sourcePath"], "Projetos/Feature.md")

    def test_artifact_inside_workspace_recovers_origin_and_does_not_duplicate(self):
        workspace = self.vault / "Projetos" / "Jetta Move" / "Spec Driven"
        workspace.mkdir(parents=True)
        (self.vault / "Projetos/Jetta Move").mkdir(exist_ok=True)
        (self.vault / "Projetos/Jetta Move/Disponibilidade.md").write_text("# Feature\n", encoding="utf-8")
        (workspace / "Index.md").write_text('---\nsource: "[[Projetos/Jetta Move/Disponibilidade.md]]"\n---\n', encoding="utf-8")
        spec = workspace / "Specs" / "Availability.md"
        spec.parent.mkdir()
        spec.write_text("# Spec\n", encoding="utf-8")
        result = resolve(str(spec), self.config)
        self.assertEqual(result["sourceType"], "artifact")
        self.assertEqual(result["sourceNote"], "Projetos/Jetta Move/Disponibilidade.md")
        self.assertEqual(len(list(workspace.parent.glob("Spec*"))), 1)

    def test_existing_style_customization_is_preserved(self):
        config = self.vault / ".obsidian/plugins/iconocolor/data.json"
        self.write_json(config, {"folderConfigs": {"Projetos/Feature/Spec Driven": {"icon": "custom-icon", "baseColor": "#123456"}}})
        folder = self.vault / "Projetos/Feature"
        folder.mkdir(parents=True)
        resolve(str(folder), self.config)
        stored = json.loads(config.read_text())
        self.assertEqual(stored["folderConfigs"]["Projetos/Feature/Spec Driven"]["icon"], "custom-icon")

    def test_existing_icon_color_and_folder_status_plugins_are_reused(self):
        from spec_workspace import register_style

        paths = ["Features/CSC/Spec Driven", "Features/CSC/Spec Driven/Diagnostics", "Features/CSC/Spec Driven/Validation", "Features/CSC/Spec Driven/Validation/Review.md"]
        register_style(self.vault, paths, status="production")
        status = json.loads((self.vault / ".obsidian/plugins/folder-status/data.json").read_text(encoding="utf-8"))
        icons = json.loads((self.vault / ".obsidian/plugins/iconocolor/data.json").read_text(encoding="utf-8"))
        colors = json.loads((self.vault / ".obsidian/plugins/obsidian-file-color/data.json").read_text(encoding="utf-8"))
        self.assertEqual(status["folders"][paths[0]], "production")
        self.assertEqual(icons["folderConfigs"][paths[1]]["icon"], "lucide:bug")
        self.assertEqual(icons["folderConfigs"][paths[2]]["icon"], "lucide:badge-check")
        self.assertIn({"path": paths[3], "color": "especificacoes"}, colors["fileColors"])

    def test_reference_outside_vault_is_rejected(self):
        outside = self.base / "outside.md"
        outside.write_text("# Outside\n", encoding="utf-8")
        with self.assertRaises(ResolutionError):
            resolve(str(outside), self.config)

    def test_duplicate_workspace_aliases_are_not_silently_selected(self):
        root = self.vault / "Feature"
        root.mkdir()
        (root / "Spec Driven").mkdir()
        (root / "Specdriven").mkdir()
        note = root / "Feature.md"
        note.write_text("# Feature\n", encoding="utf-8")
        with self.assertRaises(ResolutionError):
            resolve(str(note), self.config)

    def test_windows_markdown_link_with_spaces_accents_and_brackets_resolves(self):
        note = self.vault / "Features" / "[CSC] Operação" / "Decisão (XML).md"
        note.parent.mkdir(parents=True)
        note.write_text("# Decisão\n", encoding="utf-8")
        reference = "[decisão](<" + str(note).replace("/", "\\") + ">)"
        result = resolve(reference, self.config)
        self.assertEqual(result["sourcePath"], "Features/[CSC] Operação/Decisão (XML).md")

    def test_explicit_obsidian_folder_path_embedded_in_instruction_resolves(self):
        folder = self.vault / "Features" / "CSC [Operação]"
        folder.mkdir(parents=True)
        instruction = "Use this Obsidian folder: " + str(folder)
        result = resolve(instruction, self.config)
        self.assertEqual(result["rootDirectory"], "Features/CSC [Operação]")

    def test_artifact_routes_are_lazy_and_use_stable_names(self):
        from spec_workspace import artifact_path

        workspace = self.vault / "Feature" / "Spec Driven"
        first = artifact_path(workspace, "research", "Resolver atual de Linha")
        again = artifact_path(workspace, "research", "Resolver atual de Linha")
        self.assertEqual(first, again)
        self.assertEqual(first, workspace / "Research" / "resolver-atual-de-linha.md")
        self.assertFalse((workspace / "Diagnostics").exists())

    def test_index_updates_only_generated_pointer_section(self):
        from spec_workspace import update_index

        workspace = self.vault / "Feature" / "Spec Driven"
        workspace.mkdir(parents=True)
        index = workspace / "Index.md"
        index.write_text(
            "# Feature\n\nManual note stays.\n\n"
            "<!-- spec-workspace:generated:start -->\nold\n"
            "<!-- spec-workspace:generated:end -->\n",
            encoding="utf-8",
        )
        update_index(workspace, {"Specs": ["Specs/Feature Spec.md"], "Tickets": ["Tickets/01 Build.md"]})
        update_index(workspace, {"Specs": ["Specs/Feature Spec.md"], "Tickets": ["Tickets/01 Build.md"]})
        content = index.read_text(encoding="utf-8")
        self.assertEqual(content.count("[[Specs/Feature Spec]]"), 1)
        self.assertEqual(content.count("[[Tickets/01 Build]]"), 1)
        self.assertIn("Manual note stays.", content)
        self.assertNotIn("old", content)

    def test_tracker_frontier_claim_and_resolution_are_persistent(self):
        from spec_workspace import frontier, transition_ticket, update_index

        workspace = self.vault / "Feature" / "Spec Driven"
        tickets = workspace / "Tickets"
        tickets.mkdir(parents=True)
        (tickets / "01-base.md").write_text(
            "---\ntype: ticket\nstatus: pending\ntriage_role: ready-for-agent\nticket_status: open\nblocked_by: []\n---\n# Base\n",
            encoding="utf-8",
        )
        (tickets / "02-followup.md").write_text(
            "---\ntype: ticket\nstatus: pending\ntriage_role: ready-for-agent\nticket_status: open\nblocked_by:\n  - [[01-base]]\n---\n# Follow up\n",
            encoding="utf-8",
        )
        update_index(workspace, {"Tickets": ["Tickets/01-base.md", "Tickets/02-followup.md"]})
        self.assertEqual([p.name for p in frontier(workspace)], ["01-base.md"])
        transition_ticket(tickets / "01-base.md", "claimed")
        self.assertEqual([p.name for p in frontier(workspace)], [])
        transition_ticket(tickets / "01-base.md", "resolved")
        self.assertEqual([p.name for p in frontier(workspace)], ["02-followup.md"])

    def test_triage_roles_and_comments_remain_distinct_from_ticket_and_folder_status(self):
        from spec_workspace import append_comment, transition_triage_role

        ticket = self.vault / "ticket.md"
        ticket.write_text("---\ntype: ticket\nstatus: pending\ntriage_role: needs-triage\nticket_status: open\n---\n# Ticket\n", encoding="utf-8")
        transition_triage_role(ticket, "needs-info")
        append_comment(ticket, "Please confirm the operation code.")
        content = ticket.read_text(encoding="utf-8")
        self.assertIn("triage_role: needs-info", content)
        self.assertIn("ticket_status: open", content)
        self.assertIn("status: pending", content)
        self.assertIn("## Comments\n\nPlease confirm", content)

    def test_concurrent_ticket_writer_is_rejected_without_losing_state(self):
        from spec_workspace import ResolutionError, transition_ticket

        ticket = self.vault / "ticket.md"
        ticket.write_text("---\ntype: ticket\nstatus: pending\ntriage_role: ready-for-agent\nticket_status: open\n---\n# Ticket\n", encoding="utf-8")
        lock = ticket.with_name(ticket.name + ".lock")
        lock.write_text("pid=other\n", encoding="ascii")
        with self.assertRaises(ResolutionError):
            transition_ticket(ticket, "claimed")
        self.assertIn("ticket_status: open", ticket.read_text(encoding="utf-8"))
        lock.unlink()

    def test_workspace_status_changes_only_after_explicit_transition(self):
        from spec_workspace import workflow_status

        self.assertEqual(workflow_status([]), "pending")
        self.assertEqual(workflow_status(["claimed"]), "production")
        self.assertEqual(workflow_status(["resolved", "resolved"], validated=False), "production")
        self.assertEqual(workflow_status(["resolved", "resolved"], validated=True), "implemented")

    def test_wayfinder_map_and_decision_frontier_persist_in_ticket_notes(self):
        from spec_workspace import frontier, transition_ticket, write_artifact

        workspace = self.vault / "Effort" / "Spec Driven"
        map_note = write_artifact(workspace, "map", "Map", "## Destination\nDeliver the feature.\n\n## Decisions so far\n")
        first = write_artifact(workspace, "ticket", "01 research operation", "## Question\nWhich operation source is authoritative?")
        second = write_artifact(workspace, "ticket", "02 confirm behavior", "## Question\nHow do users confirm?",
                                {"blocked_by": ["[[01-research-operation]]"]})
        self.assertEqual(map_note, workspace / "Wayfinder" / "Map.md")
        self.assertEqual(frontier(workspace), [first])
        transition_ticket(first, "claimed")
        transition_ticket(first, "resolved")
        self.assertEqual(frontier(workspace), [second])

    def test_artifact_write_is_idempotent_and_preserves_manual_sections(self):
        from spec_workspace import write_artifact

        workspace = self.vault / "Feature" / "Spec Driven"
        note = write_artifact(workspace, "research", "Operation source", "First findings.")
        with note.open("a", encoding="utf-8") as stream:
            stream.write("\n## Human note\nKeep this.\n")
        again = write_artifact(workspace, "research", "Operation source", "Updated findings.")
        content = note.read_text(encoding="utf-8")
        self.assertEqual(note, again)
        self.assertEqual(len(list((workspace / "Research").glob("*.md"))), 1)
        self.assertIn("Updated findings.", content)
        self.assertIn("## Human note\nKeep this.", content)

    def test_semantic_artifact_id_survives_title_changes(self):
        from spec_workspace import write_artifact

        workspace = self.vault / "Feature" / "Spec Driven"
        first = write_artifact(workspace, "decision", "Resolve by XML", "First decision.", {"artifact_id": "decision-csc-operation"})
        second = write_artifact(workspace, "decision", "Resolve CSC operation from XML", "Updated decision.", {"artifact_id": "decision-csc-operation"})
        self.assertEqual(first, second)
        self.assertEqual(len(list((workspace / "Decisions").glob("*.md"))), 1)
        self.assertIn("# Resolve CSC operation from XML", first.read_text(encoding="utf-8"))

    def test_resolver_does_not_read_unrelated_markdown(self):
        note = self.vault / "Feature" / "Feature.md"
        note.parent.mkdir()
        note.write_text("# Feature\n", encoding="utf-8")
        unrelated = self.vault / "Other"
        unrelated.mkdir()
        for i in range(1000):
            (unrelated / f"{i}.md").write_text("# unrelated\n", encoding="utf-8")
        read_paths = []
        original_read_text = Path.read_text

        def tracking_read_text(path, *args, **kwargs):
            read_paths.append(path)
            return original_read_text(path, *args, **kwargs)

        with patch.object(Path, "read_text", tracking_read_text):
            result = resolve(str(note), self.config)
        self.assertEqual(result["specDrivenDirectory"], "Feature/Spec Driven")
        self.assertLessEqual(len(read_paths), 5)
        self.assertFalse(any(path.is_relative_to(unrelated) for path in read_paths))

    def test_end_to_end_workflow_uses_only_fixture_and_completes(self):
        from spec_workspace import frontier, transition_ticket, workflow_status, write_artifact

        source = self.vault / "Features" / "CSC" / "CSC.md"
        source.parent.mkdir(parents=True)
        source.write_text("# CSC\n", encoding="utf-8")
        workspace = source.parent / "Spec Driven"
        resolve(str(source), self.config)

        context = write_artifact(workspace, "context", "CSC Context", "## Operation\nXML identifies the operation.")
        decision = write_artifact(workspace, "decision", "Resolve operation from XML", "Use the XML operation code.",
                                  {"context": "[[Context/CSC Context]]", "source": "[[../CSC]]"})
        spec = write_artifact(workspace, "spec", "CSC by operation", "## Acceptance Criteria\nResolve CSC configuration by operation.\n\n## Testing Decisions\nTest the public resolver seam.",
                              {"source": "[[../CSC]]", "decisions": ["[[Decisions/Resolve operation from XML]]"]})
        first = write_artifact(workspace, "ticket", "01 resolve operation", "Implement the resolver.",
                               {"spec": "[[Specs/CSC by operation]]", "context": "[[Context/CSC Context]]"})
        second = write_artifact(workspace, "ticket", "02 preview", "Show the resolved configuration.",
                                {"spec": "[[Specs/CSC by operation]]", "blocked_by": ["[[01-resolve-operation]]"]})
        self.assertEqual(frontier(workspace), [first])

        implementation = self.base / "implementation_repo"
        tests = implementation / "tests"
        tests.mkdir(parents=True)
        (tests / "__init__.py").write_text("", encoding="utf-8")
        (implementation / "operation.py").write_text("def resolve_operation(xml):\n    raise NotImplementedError\n", encoding="utf-8")
        test_file = tests / "test_operation.py"
        test_file.write_text(
            "import unittest\nfrom operation import resolve_operation\n\n"
            "class OperationTests(unittest.TestCase):\n"
            "    def test_resolves_operation_code_from_xml(self):\n"
            "        self.assertEqual(resolve_operation('<Operation><Code>CSC01</Code></Operation>'), 'CSC01')\n",
            encoding="utf-8")
        command = [sys.executable, "-m", "unittest", "discover", "-s", "tests"]
        red = subprocess.run(command, cwd=implementation, capture_output=True, text=True)
        self.assertNotEqual(red.returncode, 0, red.stdout + red.stderr)
        self.assertIn("NotImplementedError", red.stderr)

        transition_ticket(first, "claimed")  # implementation starts
        (implementation / "operation.py").write_text(
            "import xml.etree.ElementTree as ET\n\n"
            "def resolve_operation(xml):\n"
            "    code = ET.fromstring(xml).findtext('Code')\n"
            "    return code\n", encoding="utf-8")
        green = subprocess.run(command, cwd=implementation, capture_output=True, text=True)
        self.assertEqual(green.returncode, 0, green.stderr)
        self.assertEqual(workflow_status(["claimed", "open"]), "production")
        transition_ticket(first, "resolved")  # TDD and implementation complete
        self.assertEqual(frontier(workspace), [second])

        with test_file.open("a", encoding="utf-8") as stream:
            stream.write(
                "\n    def test_rejects_missing_operation_code(self):\n"
                "        with self.assertRaises(ValueError):\n"
                "            resolve_operation('<Operation><Name>CSC</Name></Operation>')\n")
        for cached in tests.rglob("*.pyc"):
            cached.unlink()
        red = subprocess.run(command, cwd=implementation, capture_output=True, text=True)
        self.assertNotEqual(red.returncode, 0, red.stdout + red.stderr)
        self.assertIn("AssertionError", red.stderr)
        transition_ticket(second, "claimed")
        (implementation / "operation.py").write_text(
            "import xml.etree.ElementTree as ET\n\n"
            "def resolve_operation(xml):\n"
            "    code = ET.fromstring(xml).findtext('Code')\n"
            "    if not code:\n        raise ValueError('operation code is required')\n"
            "    return code\n", encoding="utf-8")
        green = subprocess.run(command, cwd=implementation, capture_output=True, text=True)
        self.assertEqual(green.returncode, 0, green.stderr)
        implementation_source = (implementation / "operation.py").read_text(encoding="utf-8")
        test_source = test_file.read_text(encoding="utf-8")
        self.assertIn("ET.fromstring", implementation_source)
        self.assertIn("raise ValueError", implementation_source)
        self.assertIn("test_resolves_operation_code_from_xml", test_source)
        self.assertIn("test_rejects_missing_operation_code", test_source)
        transition_ticket(second, "resolved")
        validation = write_artifact(workspace, "validation", "CSC review", "All acceptance criteria pass.",
                                    {"spec": "[[Specs/CSC by operation]]", "ticket": "[[Tickets/02-preview]]"})
        statuses = ["resolved", "resolved"]
        final_status = workflow_status(statuses, validated=validation.is_file())
        resolve(str(source), self.config, status=final_status)

        self.assertEqual(final_status, "implemented")
        self.assertTrue(context.is_file() and decision.is_file() and spec.is_file() and first.is_file() and second.is_file())
        self.assertEqual(len(list(workspace.rglob("*.md"))), 7)
        index = (workspace / "Index.md").read_text(encoding="utf-8")
        self.assertIn("[[Decisions/resolve-operation-from-xml]]", index)
        self.assertIn("[[Specs/csc-by-operation]]", index)
        self.assertIn("[[Tickets/02-preview]]", index)
        stored_status = json.loads((self.vault / ".obsidian/plugins/folder-status/data.json").read_text(encoding="utf-8"))
        self.assertEqual(stored_status["folders"]["Features/CSC/Spec Driven"], "implemented")
        self.assertIn("status: implemented", index)


if __name__ == "__main__":
    unittest.main()
