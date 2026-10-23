#!/usr/bin/env python3
"""Copy the rendered Mermaid SVGs used by the decks into presentations/assets/ with short names.
Run after re-rendering diagrams:  python3 presentations/tools/copy_assets.py"""
import pathlib, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
MMD = ROOT / "diagrams/mermaid/mmd"
REND = ROOT / "diagrams/mermaid/rendered"
OUT = pathlib.Path(__file__).resolve().parents[1] / "assets"
S5 = "scrum-existing/S5-scrum-mermaid-artifacts"
A = {  # alias: (folder, 1-based index, keyword that must appear in the file name)
    "scrum-workflow": (S5, 4, "scrum-workflow"), "epic-dependency": (S5, 2, "epic-dependency"),
    "story-lifecycle": (S5, 5, "story-lifecycle"), "demo-path": (S5, 7, "demo-path"),
    "delivery-map": ("07-scrum-release-risks", 11, "epic-delivery"), "rollout": ("07-scrum-release-risks", 7, "rollout"),
    "gantt": ("06-sprints", 3, "gantt"),
    "system-context": ("01-architecture", 1, "system-context"), "deployables": ("01-architecture", 3, "deployable"),
    "module-deps": ("01-architecture", 9, "combined"),
    "turn-overview": ("03-ai-engine", 1, "pipeline-overview"), "turn-state": ("03-ai-engine", 6, "state-machine"),
    "trust-levels": ("03-ai-engine", 7, "trust"), "escalation": ("03-ai-engine", 8, "escalation"),
    "agent-lifecycle": ("03-ai-engine", 11, "agent-version"),
    "webhook": ("02-cross-cutting-flows", 1, "webhook"), "outbox": ("02-cross-cutting-flows", 2, "outbox"),
    "delivery-states": ("02-cross-cutting-flows", 3, "delivery"), "retry": ("02-cross-cutting-flows", 4, "retry"),
    "tool-auth": ("02-cross-cutting-flows", 5, "validation"), "tool-exec": ("02-cross-cutting-flows", 6, "execution"),
    "tenant-resolution": ("02-cross-cutting-flows", 8, "tenant"), "degradation": ("02-cross-cutting-flows", 10, "degradation"),
    "three-layer": ("epics/E06-safe-business-tools", 2, "three-layer"),
    "adapter-boundary": ("epics/E11-integrations-and-channels", 2, "adapter"),
    "integration-config": ("epics/E11-integrations-and-channels", 3, "configure"),
    "integration-health": ("epics/E11-integrations-and-channels", 4, "health"),
    "second-channel": ("epics/E11-integrations-and-channels", 6, "second-channel"),
    "voice-lifecycle": ("04-voice-multimodal", 1, "lifecycle"), "voice-opt-a": ("04-voice-multimodal", 2, "option-a"),
    "voice-opt-b": ("04-voice-multimodal", 3, "option-b"), "voice-barge-in": ("04-voice-multimodal", 6, "barge"),
    "voice-modality": ("04-voice-multimodal", 8, "modality"),
    "data-aggregates": ("05-data-model", 1, "aggregate"),
    "seq-intake": ("uml/U3-sequence-diagrams", 1, "intake"), "seq-turn": ("uml/U3-sequence-diagrams", 2, "ai-turn"),
    "seq-injection": ("uml/U3-sequence-diagrams", 4, "injection"), "seq-approval": ("uml/U3-sequence-diagrams", 5, "approval"),
    "seq-handoff": ("uml/U3-sequence-diagrams", 6, "handoff"), "seq-circuit": ("uml/U3-sequence-diagrams", 11, "circuit"),
    "components": ("uml/U5-component-package-deployment-object", 1, "component"),
    "package": ("uml/U5-component-package-deployment-object", 3, "package"),
    "deployment": ("uml/U5-component-package-deployment-object", 4, "deployment"),
    "class-conversation": ("uml/U2-class-diagrams", 2, "conversation"), "class-engine": ("uml/U2-class-diagrams", 4, "turn-orchestration"),
    "class-tools": ("uml/U2-class-diagrams", 7, "tools"), "class-connectors": ("uml/U2-class-diagrams", 8, "connectors"),
    "usecases": ("uml/U1-use-cases", 1, "system-level"),
    "handoff-ownership": ("epics/E07-human-handoff", 2, "ownership"),
    "conversation-lifecycle": ("epics/E02-conversation-core", 2, "lifecycle"),
    "ingestion-pipeline": ("epics/E04-knowledge-and-rag", 3, "pipeline"),
    "tech-stack": ("08-technology", 1, "stack-map"), "tech-request": ("08-technology", 2, "message-through"),
    "tech-voice": ("08-technology", 3, "voice-stack"), "tech-delivery": ("08-technology", 4, "delivery"),
    "tech-release": ("08-technology", 5, "when-each"),
}
OUT.mkdir(exist_ok=True)
for f in OUT.glob("*.svg"):
    f.unlink()
bad = 0
for alias, (folder, idx, kw) in A.items():
    files = sorted((MMD / folder).glob("*.mmd"))
    f = files[idx - 1]
    if kw not in f.name:
        print("KEYWORD MISMATCH", alias, f.name); bad += 1; continue
    shutil.copy2(REND / folder / (f.stem + ".svg"), OUT / (alias + ".svg"))
print("copied", len(A) - bad, "svg files; mismatches:", bad)
sys.exit(1 if bad else 0)
