import bpy, bmesh, subprocess, collections, re, os, shutil
from . import GUI
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )

# To-Do
class find_objects_by_selected_material(bpy.types.Operator):
    bl_idname = "object.find_objects_by_selected_material"
    bl_icon = 'ANIM_DATA'
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
       # for object in context.scene.objects:
        #    for material_slot in object.material_slots:
        return {'FINISHED'}


class update_materials_list(bpy.types.Operator):
    bl_idname = "object.update_materials_list"
    bl_label = "Refresh Materials List"

    @classmethod
    def poll(cls, context):
        return len(bpy.data.materials) != 0

    def add_all_materials_to_set(self, context):
        mats_set = set()
        mats_to_be_used_for_processing = list()
        mats_collection = bpy.context.scene.mats_collection
        print("Executing add all materials")
        for object in context.scene.objects:
            for material_slot in object.material_slots:
                if not material_slot.name in mats_set and material_slot.material.users != 0:
                    mats_set.add(material_slot.name)
                    mats_to_be_used_for_processing.append(material_slot)


        for material_slot in mats_to_be_used_for_processing:
            item = mats_collection.add()
            item.material_checkbox = True
            item.material_name = material_slot.name
            item.material = material_slot.material

        if not mats_collection:
            self.report({'ERROR'}, "No materials found")
            return False
        else:
            return True

    #def tag_redraw(context, space_type="PROPERTIES", region_type="WINDOW"):
    #   for window in context.window_manager.windows:
    #       for area in window.screen.areas:
    #           if area.spaces[0].type == space_type:
    #               for region in area.regions:
    #                   if region.type == region_type:
    #                       region.tag_redraw()

    def execute(self, context):
        # Clean collection first
        bpy.context.scene.mats_collection.clear()
        if self.add_all_materials_to_set(context):
            print("Stuff")
            #self.tag_redraw(context)
        return {'FINISHED'}

class vtf_operator(bpy.types.Operator):
    bl_idname = "object.vtf_operator"
    bl_label = "Convert"

# ------------------------------------------------------------------------
#     custom methods
# ------------------------------------------------------------------------


    @classmethod
    def poll(cls, context):
        return context.scene.VTFLibCmd != "" and context.scene.material_path != ""

    def execute(self, context):
        #main(context)
        scene = context.scene
        
        image_path_list = list()
        image_name_to_material_name = dict()
        for mat_object in scene.mats_collection:
            material = mat_object.material
            if material.node_tree.nodes["Principled BSDF"] is None:
                self.report({'ERROR'}, "Please change your material type to Principled BSDF")
                return {'CANCELLED'}

            # Get Principled BSDF node
            # and check if a link exists
            if material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].is_linked:
                node = None

                # if a link exists, then there is a image texture, presumably
                linked_nodes = material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].links

                for node_link in linked_nodes:
                    node = node_link.from_node
                    if "Image Texture" == node.bl_label:
                        print(node.bl_label)
                        break
                if node is None:
                    self.report({'ERROR'}, "No Image Texture node is found")
                    return {'CANCELLED'}

                if node.image is None:
                    self.report({'ERROR'}, "No source image found")
                    return {'CANCELLED'}

                if node.image.is_dirty:
                    self.report({'ERROR'}, "There are unsaved changes to your source image. Please save it first")
                    return {'CANCELLED'}

                image_path_raw = node.image.filepath_raw

                # Convert to readable abs path
                full_abs_path = bpy.path.abspath(image_path_raw)
                real_abs_path = os.path.realpath(full_abs_path)
                image_path_list.append(real_abs_path)
                image_name_to_material_name[real_abs_path] = mat_object.material_name

            else:
                # No img texture found
                # bake color?
                print()
                self.report({'ERROR'}, "Unsupported operation. Base color isn't linked to a TEX_IMAGE")
                return {'CANCELLED'}
                #print(color[0], color[1], color[2], color[3])


        # Get VTFLibCmd
        VTFLibCmdFilePath = scene.VTFLibCmd.path + "VTFCmd.exe"
        MaterialOutputPath = scene.material_path.path
        if not os.path.exists(VTFLibCmdFilePath) or not os.path.exists(MaterialOutputPath):
            self.report({'ERROR'}, "Path to VTFCmd or material output folder is missing")
        else:
            self.report({'INFO'}, "Starting material vtf conversion process...")
            command_line = list()
            command_line.append(VTFLibCmdFilePath)
            
            file_count = 0
            # Get all materials and add to a args list
            # Requires cleanup later
            for image_path in image_path_list:
                file_count += 1
                # Copy image first, keeping the original
                (image_root, image_ext) = os.path.splitext(image_path)
                new_image_tex_file = shutil.copy(image_path, os.path.dirname(image_path) + "\\" + image_name_to_material_name[image_path] + "" + image_ext)
                command_line.append("-file")
                command_line.append("\"" + new_image_tex_file + "\"")

            # Add all other parameters to command_line
            command_line.append("-format")
            command_line.append("\"" + context.scene.format_op + "\"")

            command_line.append("-alphaformat")
            command_line.append("\"" + context.scene.format_alpha_op + "\"")

            command_line.append("-version")
            command_line.append("\"" + context.scene.vtf_version + "\"")

            if context.scene.resize_bool:
                command_line.append("-resize")

                command_line.append("-rmethod")
                command_line.append("\"" + context.scene.resize_meth_op + "\"")

                command_line.append("-rfilter")
                command_line.append("\"" + context.scene.resize_filter_op+ "\"")

                clamp_value = context.scene.clamp_op[:context.scene.clamp_op.index("x")]
                command_line.append("-rclampwidth")
                command_line.append(clamp_value)

                command_line.append("-rclampheight")
                command_line.append(clamp_value)

            if context.scene.vmt_shader_bool:
                command_line.append("-shader")
                command_line.append("\"" + context.scene.vmt_shader_op + "\"")
            
            # Define output folder
            command_line.append("-output")
            command_line.append("\"" + MaterialOutputPath[:-1] + "\"")

            self.report({'INFO'}, ' '.join(command_line))
            # Continue with execution with subprocess
            VTFLibCmd_subprocess = subprocess.Popen(' '.join(command_line), stdin=subprocess.DEVNULL, stderr=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
            (out, error) = VTFLibCmd_subprocess.communicate()
            print(out, error)

            if VTFLibCmd_subprocess.returncode == 0:
                self.report({'INFO'}, "Done processing " + str(file_count) + " files")


            ##VTFLibCmd_subprocess.stdout.close()
            ##VTFLibCmd_subprocess.wait()
        return {'FINISHED'}

classes = (
    update_materials_list, vtf_operator, find_objects_by_selected_material
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


