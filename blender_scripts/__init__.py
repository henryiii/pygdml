# Blender addon __init__

#    Addon info
bl_info = {
    "name": "Geant4 GDML format",
    "author": "Henry Schreiner",
    "location": "File > Export",
    "description": "GDML export for Blender. Supports meshes with auto-triangulation. Includes a C++ code generator.",
    "version": (0, 2),
    "blender": (2, 75, 0),
    "warning": "In development",
    "category": "Import-Export"}

# To support reload properly, try to access a package var,
# if it's there, reload everything

if "bpy" in locals():
    import imp
    if 'blendertoG4' in locals():
        imp.reload(blendertoG4)
    if 'blendertoGDML' in locals():
        imp.reload(blendertoGDML)

import bpy
from bpy.props import StringProperty, BoolProperty, FloatVectorProperty
from bpy_extras.io_utils import ExportHelper


class EXPORT_OT_geant_cpp(bpy.types.Operator, ExportHelper):
    bl_idname = "io_export_scene.geant_cpp"
    bl_description = 'Export to Geant4 C++ file format (.cc)'
    bl_label = "Export Geant4 C++"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    # From ExportHelper. Filter filenames.
    filename_ext = ".cc"
    filter_glob = StringProperty(default="*.cc", options={'HIDDEN'})

    filepath = StringProperty(
        name="File Path",
        description="File path used for exporting the GDML file",
        maxlen=1024, default="")

    only_selected = BoolProperty(
        name="Export Selected",
        description="Export only selected meshes",
        default=False)

    global_coords = BoolProperty(
        name="Global Coordinates",
        description="Use global coordinates for points",
        default=True)

    def execute(self, context):
        from . import blendertoCPP
        blendertoCPP.export_cpp(self.properties.filepath,
                                self.properties.only_selected,
                                self.properties.global_coords)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class EXPORT_OT_geant_gdml(bpy.types.Operator, ExportHelper):
    bl_idname = "io_export_scene.geant_gdml"
    bl_description = 'Export to Geant4 GDML file format (.gdml)'
    bl_label = "Export Geant4 GDML"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    filename_ext = ".gdml"
    filter_glob = StringProperty(default="*.gdml", options={'HIDDEN'})

    filepath = StringProperty(
        name="File Path",
        description="File path used for exporting the GDML file",
        maxlen=1024, default="")

    only_selected = BoolProperty(
        name="Export Selected",
        description="Export only selected meshes",
        default=False)

    global_coords = BoolProperty(
        name="Global Coordinates",
        description="Use global coordinates for points",
        default=True)

    pretty = BoolProperty(
        name="Pretty output",
        description="Should the file be nicely formatted?",
        default=True)

    world = FloatVectorProperty(
        name='World size',
        description="Set the dimensions of the world box.",
        default=(5, 5, 5))

    def execute(self, context):
        from .blendertoGDML import export_gdml
        export_gdml(self.properties.filepath,
                    self.properties.only_selected,
                    self.properties.global_coords,
                    self.properties.world,
                    self.properties.pretty)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


#    Registration
def menu_func_export_gdml(self, context):
    self.layout.operator(EXPORT_OT_geant_gdml.bl_idname, text="Geant4 GDML (.gdml)...")


def menu_func_export_cpp(self, context):
    self.layout.operator(EXPORT_OT_geant_cpp.bl_idname, text="Geant4 CPP (.cc)...")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export_gdml)
    bpy.types.INFO_MT_file_export.append(menu_func_export_cpp)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_export_gdml)
    bpy.types.INFO_MT_file_export.remove(menu_func_export_cpp)


if __name__ == "__main__":
    register()
