import bpy
from . import VTFLibOperators as vtf_operator
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty
                       )
from bpy.types import (PropertyGroup)

# ------------------------------------------------------------------------
#     Property classes
# ------------------------------------------------------------------------

class Material_List(bpy.types.PropertyGroup):
    material_checkbox: BoolProperty()
    material_name: StringProperty()
    material: PointerProperty(type=bpy.types.Material)

class UI_Settings(PropertyGroup):
    path : StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')

# GUI Utility
class VTF_UIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "material_checkbox", text=item.material_name, icon='MATERIAL_DATA')

    def invoke(self, context, event):
        pass


# GUI Main
class VTFLibConverter(bpy.types.Panel):
    """Creates a Panel for streamlining material to vtf process in the scene context of the properties editor"""
    bl_label = "VTFLibConverter"
    bl_idname = "SCENE_PT_vtflibconverter"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        object = context.object
        scene = context.scene

        # Material checkbox list
        row = layout.row()
        row.label(text="Material List:")

        row = layout.row()
        row.template_list("VTF_UIList", "", scene, "mats_collection", scene, "mats_index", rows=2)

        row = layout.row()
        row.operator("object.update_materials_list")

        # VTFCMD Path textbox
        row = layout.row()
        row.label(text="VTFCmd Path *: ")
        row = layout.row()
        row.prop(scene.VTFLibCmd, "path")

        row = layout.row()
        row.label(text="Material Ouptut Path *:")
        row = layout.row()
        row.prop(scene.material_path, "path")

        # VTF parameter and settings
        row = layout.row()
        row.label(text="VTF Parameters: ")

        row = layout.row(align=True)
        row.prop(scene, "format_op")

        row = layout.row(align=True)
        row.prop(scene, "format_alpha_op")

        row = layout.row(align=True)
        row.prop(scene, "vtf_version")

        row = layout.row(align=True)
        row.prop(scene, "resize_bool", text="Resize?")

        row = layout.row(align=True)
        row.prop(scene, "resize_meth_op")

        row = layout.row(align=True)
        row.prop(scene, "resize_filter_op")

        row = layout.row(align=True)
        row.prop(scene, "clamp_op")

        row = layout.row(align=True)
        row.prop(scene, "vmt_shader_bool", text="Generate .VMT")

        row = layout.row(align=True)
        row.prop(scene, "vmt_shader_op")

        row = layout.row(align=True)
        row.prop(scene, "vmt_param_additive", text="Additive?")
        row.prop(scene, "vmt_param_translucent", text="Translucent?")
        
        row = layout.row(align=True)
        row.prop(scene, "vmt_param_nocull", text="No Cull?")

        # Convert button
        row = layout.row()
        row.operator("object.vtf_operator")





# ------------------------------------------------------------------------
#     Registration
# ------------------------------------------------------------------------
classes = (
    VTF_UIList, VTFLibConverter, Material_List, UI_Settings
)
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mats_collection = CollectionProperty(type=Material_List)
    bpy.types.Scene.mats_index = IntProperty()
    bpy.types.Scene.VTFLibCmd = PointerProperty(type=UI_Settings)
    bpy.types.Scene.material_path = PointerProperty(type=UI_Settings)
    bpy.types.Scene.resize_bool = BoolProperty(name="")
    bpy.types.Scene.vmt_shader_bool = BoolProperty(name="")
    bpy.types.Scene.vmt_param_additive = BoolProperty(default=False)
    bpy.types.Scene.vmt_param_translucent = BoolProperty(default=False)
    bpy.types.Scene.vmt_param_nocull = BoolProperty(default=False)

    bpy.types.Scene.clamp_op = EnumProperty(
        name="Clamp: ",
        description="VTF Clamp",
        items=[ ('2x2', "2x2", ""),
                ('4x4', "4x4", ""),
                ('8x8', "8x8", ""),
                ('16x16', "16x16", ""),
                ('32x32', "32x32", ""),
                ('64x64', "64x64", ""),
                ('128x128', "128x128", ""),
                ('256x256', "256x256", ""),
                ('512x512', "512x512", ""),
                ('1024x1024', "1024x1024", ""),
                ('2048x2048', "2048x2048", ""),
                ('4096x4096', "4096x4096", "")
               ]
        )

    bpy.types.Scene.format_op = EnumProperty(
        name="Format: ",
        description="VTF Normal Format",
        items=[ ('dxt1', "DXT1", ""),
                ('dxt3', "DXT3", ""),
                ('dxt5', "DXT5", ""),
               ]
    )

    bpy.types.Scene.format_alpha_op = EnumProperty(
        name="Alpha Format: ",
        description="VTF Alpha Format",
        items=[ ('dxt1', "DXT1", ""),
                ('dxt3', "DXT3", ""),
                ('dxt5', "DXT5", "")
               ]
    )

    bpy.types.Scene.vtf_version = EnumProperty(
        name="VTF Version: ",
        description="VTF version",
        items=[ ('7.2', "7.2", ""),
                ('7.3', "7.3", ""),
                ('7.4', "7.4", ""),
                ('7.5', "7.5", "")
               ]
    )

    bpy.types.Scene.resize_meth_op = EnumProperty(
        name="Resize Method: ",
        description="VTF resize method",
        items=[ ('NEAREST', "NEAREST", ""),
                ('BIGGEST', "BIGGEST", ""),
                ('SMALLEST', "SMALLEST", "")
               ]
    )

    bpy.types.Scene.resize_filter_op = EnumProperty(
        name="Resize Filter: ",
        description="VTF resize filter",
        items=[ ('TRIANGLE', "TRIANGLE", ""),
               ]
    )

    bpy.types.Scene.vmt_shader_op = EnumProperty(
        name="Shader: ",
        description="VMT Shader selector",
        items=[ ('UnlitGeneric', "UnlitGeneric", ""),
                ('VertexlitGeneric', "VertexlitGeneric", ""),
                ('LightmappedGeneric', "LightmappedGeneric", "")
               ]
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.VTFLibCmd
    del bpy.types.Scene.mats_collection
    del bpy.types.Scene.mats_index
    del bpy.types.Scene.material_path
    del bpy.types.Scene.resize_bool
    del bpy.types.Scene.clamp_op
    del bpy.types.Scene.resize_filter_op
    del bpy.types.Scene.resize_meth_op
    del bpy.types.Scene.vtf_version
    del bpy.types.Scene.format_alpha_op
    del bpy.types.Scene.format_op
    del bpy.types.Scene.vmt_shader_bool
    del bpy.types.Scene.vmt_shader_op
    del bpy.types.Scene.vmt_param_additive
    del bpy.types.Scene.vmt_param_translucent
    del bpy.types.Scene.vmt_param_nocull


