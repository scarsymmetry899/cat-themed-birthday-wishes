"""Export the current four-state Blender foundation as a browser-ready GLB."""

from pathlib import Path
import sys

import bpy


def main():
    args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    if len(args) != 1:
        raise RuntimeError("Pass the output GLB after --")
    output = Path(args[0]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    # The experimental overlay shells failed visual QA. They are intentionally
    # omitted from the web preview; the underlying weighted production mesh is
    # preserved so reviewers see the real remaining paw-topology limitation.
    for obj in list(bpy.data.objects):
        if obj.name.startswith("Marmalade_PawShell_"):
            bpy.data.objects.remove(obj, do_unlink=True)

    for action in bpy.data.actions:
        if action.name.startswith("Marmalade_"):
            action.use_fake_user = True

    allowed = {
        "Marmalade_ProductionRig_v01",
        "Marmalade_WeightedCandidate_v01",
        "Marmalade_FaceRoot",
    }
    face = bpy.data.objects.get("Marmalade_FaceRoot")
    if face:
        allowed.update(child.name for child in face.children_recursive)

    bpy.ops.object.select_all(action="DESELECT")
    for name in allowed:
        obj = bpy.data.objects.get(name)
        if obj and not obj.hide_render:
            obj.hide_viewport = False
            obj.select_set(True)
    rig = bpy.data.objects.get("Marmalade_ProductionRig_v01")
    if rig:
        bpy.context.view_layer.objects.active = rig

    bpy.ops.export_scene.gltf(
        filepath=str(output),
        export_format="GLB",
        use_selection=True,
        export_animations=True,
        export_animation_mode="ACTIONS",
        export_skins=True,
        export_morph=True,
        export_apply=False,
    )
    bpy.context.scene["web_preview_glb"] = str(output)
    bpy.context.scene["web_preview_note"] = "Experimental paw shells omitted after failed visual QA"
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    print({"output": str(output), "selected": sorted(allowed)})


if __name__ == "__main__":
    main()
