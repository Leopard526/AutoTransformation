#  █████╗ ██╗   ██╗████████╗ ██████╗                                             
# ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗                                            
# ███████║██║   ██║   ██║   ██║   ██║                                            
# ██╔══██║██║   ██║   ██║   ██║   ██║                                            
# ██║  ██║╚██████╔╝   ██║   ╚██████╔╝                                            
# ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝                                             
#                                                                                
# ████████╗██████╗  █████╗ ███╗   ██╗███████╗███████╗ ██████╗ ██████╗ ███╗   ███╗
# ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔════╝██╔═══██╗██╔══██╗████╗ ████║
#    ██║   ██████╔╝███████║██╔██╗ ██║███████╗█████╗  ██║   ██║██████╔╝██╔████╔██║
#    ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║
#    ██║   ██║  ██║██║  ██║██║ ╚████║███████║██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║
#    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝
# 
# Copyright (c) 2025, <Shuai Oppers>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials or any kind of commercial use mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by Shuai Oppers.
# 4. Neither the name of the copyright holder nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import bpy
from . import add_on_preference
from . import search_apply

from .constants import (
    # Settings
    SCALE,
    ROTATION,
    LOCATION,
    T_select_all,

    # Keyboard
    LEFTMOUSE,
    RELEASE,
    
    # Icon
    ENABLED_ICON,
    DISABLED_ICON,
)


class AutoTransformationPanel(bpy.types.Panel):
    bl_label = "Apply Transform"
    bl_idname = "OBJECT_PT_AUTO_TRANSFORM_UI"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI" 
    bl_category = "Item"


    def draw(self, context) -> None:
            # ------------------------- Initilizer ----------------------------- #
            layout = self.layout
            col = layout.column()

            col.operator(TransformationButtons.bl_idname, text="select all").transformation_type = T_select_all
            box = layout.box()
            col = box.column(align=True)

            scale_icon = ENABLED_ICON if context.scene.T_apply_scale else DISABLED_ICON
            rotation_icon = ENABLED_ICON if context.scene.T_apply_rotation else DISABLED_ICON
            location_icon = ENABLED_ICON if context.scene.T_apply_location else DISABLED_ICON
            # ------------------------- button ----------------------------- #
            col.operator(TransformationButtons.bl_idname, text=LOCATION,  icon = location_icon).transformation_type = LOCATION
            col.operator(TransformationButtons.bl_idname, text=ROTATION,  icon = rotation_icon).transformation_type = ROTATION
            col.operator(TransformationButtons.bl_idname, text=SCALE, icon = scale_icon).transformation_type = SCALE
        
           

class TransformationButtons(bpy.types.Operator):
    """
    LOCATION: Apply location of object(s).
    ROTATION: Apply rotation of object(s).
    SCALE: Apply scale of object(s).
    SELLECT ALL: Location, rotation, and scale will change to the opposite value 
    """

    bl_label = "Transformation Buttons"
    bl_idname = "object.transformation_button"
    bl_options = {'REGISTER', 'UNDO'}

    transformation_type: bpy.props.StringProperty()

    def toggle_transformation(self, context) -> None:
        if self.transformation_type == SCALE:
            context.scene.T_apply_scale = not context.scene.T_apply_scale
            
        elif self.transformation_type == ROTATION:
            context.scene.T_apply_rotation = not context.scene.T_apply_rotation

        elif self.transformation_type == LOCATION:
            context.scene.T_apply_location = not context.scene.T_apply_location

        else:
            context.scene.T_select_all = not context.scene.T_select_all
            context.scene.T_apply_scale = context.scene.T_select_all
            context.scene.T_apply_rotation = context.scene.T_select_all
            context.scene.T_apply_location = context.scene.T_select_all
            
    def apply_transform(self, context, obj) -> None:
        scene = context.scene
       
        obj = bpy.data.objects[obj.name]

        obj.select_set(True)
        bpy.ops.object.transform_apply(
            scale = scene.T_apply_scale,
            rotation = scene.T_apply_rotation,
            location = scene.T_apply_location
            
        )
        obj.select_set(False)

    def modal(self, context, event) -> dict[str]:
        active_obj = bpy.context.active_object

        if (event.type == LEFTMOUSE and 
            event.value == RELEASE and 
            active_obj is not None):

            self.apply_transform(context=context, obj=active_obj)
           
        return {"PASS_THROUGH"}
    
    def invoke(self, context, event) -> dict[str]:
        self.toggle_transformation(context)
        scene = context.scene
        wm = context.window_manager
            
        if (scene.T_apply_scale or 
            scene.T_apply_location or
            scene.T_apply_rotation):

            wm.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        
        self.report({'WARNING'}, "No transformations are currently applied.")
        return {'CANCELLED'}

        
