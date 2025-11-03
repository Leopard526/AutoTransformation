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

from mathutils import Vector, Euler

import bpy

from . import add_on_preference
from .constants import (
    # Search Settings
    OBJECT_COLLECTION, 
    SEARCH_OPTION, 
    APPLY_ALL_OPTION,
    SEARCH_AND_APPLY_ALL,
    SHOW,
    SETTING_ALL,
    SETTINGS_SCALE,
    SETTING_LOCATION,
    SETTING_ROTATION,
    OPEN_SETTING_MENU,

    # icons
    SETTING_DISPLAY_VIEWPORT,
    TRIA_DOWN,
    TRIA_RIGHT,
    RESTRICT_VIEW_OFF, 
    RESTRICT_VIEW_ON,
    EMPTY_AXIS,
    CANCEL,
    EMPTY_SINGLE_ARROW,
    DRIVER_ROTATIONAL_DIFFERENCE,
    RESTRICT_SELECT_OFF
)


class Setting(bpy.types.Operator):
    """
    VIEWPORT: If object(s) is hidden in viewport, and has not received transformation it search or apply it. 
    LOCATION: Apply location of object(s).
    ROTATION: Apply rotation of object(s).
    SCALE: Apply scale of object(s).
    SELLECT ALL: Location, rotation, and scale will change to the opposite value 
    """

    bl_label = "Settings"
    bl_idname = "wm.settings"

    to_enable: bpy.props.StringProperty()

    def execute(self, context) -> None:
        if self.to_enable == OPEN_SETTING_MENU:
            context.scene.S_settings = not context.scene.S_settings

        elif self.to_enable == SETTING_DISPLAY_VIEWPORT:
            context.scene.S_viewport = not context.scene.S_viewport

        elif self.to_enable == SETTING_LOCATION:
            context.scene.S_location = not context.scene.S_location
            
        elif self.to_enable == SETTING_ROTATION:
            context.scene.S_rotation = not context.scene.S_rotation

        elif self.to_enable == SETTINGS_SCALE:
            context.scene.S_scale = not context.scene.S_scale

        else:
            context.scene.S_sellect_all = not context.scene.S_sellect_all
            context.scene.S_location = context.scene.S_sellect_all
            context.scene.S_rotation = context.scene.S_sellect_all
            context.scene.S_scale = context.scene.S_sellect_all

        return {'FINISHED'}
        

class SearchObject(bpy.types.Panel):
    bl_label = "Search Objects"
    bl_idname = "OBJECT_PT_SEARCH_OBJECTS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context) -> None:
        layout = self.layout
        prefs = add_on_preference.prefs() 
 
        obj_collection = bpy.data.collections.get(OBJECT_COLLECTION)
        if obj_collection is None:
            obj_collection = bpy.data.collections.new(OBJECT_COLLECTION)

        # ------------------------- Initilizer ----------------------------- #
        col = layout.column() 
        col.operator(CollectionOperator.bl_idname, text="Search and Apply").action_type = SEARCH_AND_APPLY_ALL

        row = layout.row(align=True)
        icon_tria = TRIA_DOWN if context.scene.S_settings else TRIA_RIGHT
        # ------------------------- Settings ----------------------------- #
        row.operator(Setting.bl_idname, text= "Settings", icon=icon_tria).to_enable = OPEN_SETTING_MENU

        icon_viewport = RESTRICT_VIEW_OFF if context.scene.S_viewport else RESTRICT_VIEW_ON
        icon_location = EMPTY_AXIS if context.scene.S_location else CANCEL
        icon_rotation = DRIVER_ROTATIONAL_DIFFERENCE if context.scene.S_rotation else CANCEL
        icon_scale = EMPTY_SINGLE_ARROW if context.scene.S_scale else CANCEL

        # ------------------------- Buttons or Label ----------------------------- #
        if prefs.use_label_for_button_operator:
            row.operator(Setting.bl_idname, text="", icon=icon_viewport).to_enable = SETTING_DISPLAY_VIEWPORT
            row.operator(Setting.bl_idname, text="", icon=icon_location).to_enable = SETTING_LOCATION
            row.operator(Setting.bl_idname, text="", icon=icon_rotation).to_enable = SETTING_ROTATION
            row.operator(Setting.bl_idname, text="", icon=icon_scale).to_enable = SETTINGS_SCALE
        else:
            row.label(icon=icon_viewport)
            row.label(icon=icon_location)
            row.label(icon=icon_rotation)
            row.label(icon=icon_scale)

        # ------------------------- settings drop down ----------------------------- #
        if context.scene.S_settings:
            col = layout.column()
            col.operator(Setting.bl_idname, text="Viewport", icon=icon_viewport).to_enable = SETTING_DISPLAY_VIEWPORT

            box = layout.box()
            col = box.column(align=True)

            col.operator(Setting.bl_idname, text="Select All").to_enable = SETTING_ALL
            col.operator(Setting.bl_idname, text="Location", icon=icon_location).to_enable = SETTING_LOCATION
            col.operator(Setting.bl_idname, text="Rotation", icon=icon_rotation).to_enable = SETTING_ROTATION
            col.operator(Setting.bl_idname, text="Scale", icon=icon_scale).to_enable = SETTINGS_SCALE

        # ------------------------- Search Object ----------------------------- #
        row = layout.row(align=True)
        row.operator(CollectionOperator.bl_idname, text="Search").action_type = SEARCH_OPTION
        row.operator(CollectionOperator.bl_idname, text="Apply").action_type = APPLY_ALL_OPTION

        box = layout.box().column()
        row = box.row()

        if obj_collection.objects:
            for obj in obj_collection.objects:
                row.label(text=obj.name)
                row.operator(CollectionOperator.bl_idname, text="Apply").action_type = obj.name
                row.operator(CollectionOperator.bl_idname,text="", icon=RESTRICT_SELECT_OFF).action_type = f"{SHOW}/{obj.name}"

                box = box.column()
                row = box.row()
        else:
            row.alignment = 'CENTER' 
            row.label(text="Nothing found")

class CollectionOperator(bpy.types.Operator):
    """
    Search: Search objects based on the user prefrence. 
    Apply: Apply the transformation on all found objects based on user prefrence.
    Search and Apply: Apply transformation on objects based on user prefrence. 
    You can't what is changed.   
    ◄: Show the object where no transformation is applied on user prefrencw

    """
    
    bl_label = "Add Selected to Collection"
    bl_idname = "wm.add_to_obj_collection"

    action_type: bpy.props.StringProperty()
    
    def search_obj(self, context) -> None:
        scene = context.scene
        prefs = add_on_preference.prefs()
        obj_collection = bpy.data.collections.get(OBJECT_COLLECTION)
        
        for obj in obj_collection.objects:
            obj_collection.objects.unlink(obj)

        for obj in scene.objects:
            scale_is_good: bool = obj.scale == Vector((1,1,1)) or not context.scene.S_scale
            location_is_default: bool = obj.location == Vector((0,0,0)) or not context.scene.S_location
            rotation_is_default: bool = obj.rotation_euler == Euler((0,0,0)) or not context.scene.S_rotation
            view_port_enabled: bool = context.scene.S_viewport
            obj_is_hidden = obj.hide_viewport
 
            if obj_is_hidden and not view_port_enabled:
                continue

            if obj.type != 'MESH':
                continue 
            

            if all((scale_is_good, location_is_default, rotation_is_default)):
                continue

            obj_collection.objects.link(obj)

    def apply_transformation(self,context, obj) -> dict[str]:
        obj_is_hidden = obj.hide_viewport
        S_obj = bpy.data.objects[obj.name]
        scene = context.scene

        if obj_is_hidden:
            obj.hide_viewport = False
        
        S_obj.select_set(True)

        bpy.ops.object.transform_apply(
                    scale = scene.S_scale,
                    rotation = scene.S_rotation,
                    location = scene.S_location
                    
        )

        if obj_is_hidden:
            obj.hide_viewport = True
        
        S_obj.select_set(False)

        return {"FINISHED"}
    
    def search_mesh_and_apply(self, context, mesh_name: str) -> dict[str]:
        obj_collection = bpy.data.collections.get(OBJECT_COLLECTION)    

        for obj in obj_collection.objects:
            if obj.name == mesh_name or mesh_name == APPLY_ALL_OPTION:
                self.apply_transformation(context, obj)

                obj_collection.objects.unlink(obj)
     
        return {"FINISHED"}

    def show_obj_for_user(self, context, mesh_name: str) -> dict[str]:
        prefs = add_on_preference.prefs()
        obj = bpy.data.objects.get(mesh_name)
        obj_is_hidden = obj.hide_viewport 

        if obj_is_hidden or obj_is_hidden is None:
            if not prefs.unhide_display_in_viewport:
                self.report({'INFO'}, F"Object is disabled in viewport")
                return {'CANNCELD'}

            obj.hide_viewport = False

        obj.select_set(True)    
        
        return {"FINISHED"}
           
    def execute(self, context) -> dict[str]:
        if self.action_type == SEARCH_OPTION:
            self.search_obj(context= context)
            return {"FINISHED"}

        if self.action_type == APPLY_ALL_OPTION:
            self.search_mesh_and_apply(
                context= context,
                mesh_name= APPLY_ALL_OPTION
            )

            return {"FINISHED"}
            
        if self.action_type == SEARCH_AND_APPLY_ALL:
            self.search_obj(context= context)
            self.search_mesh_and_apply(
                context= context,
                mesh_name= APPLY_ALL_OPTION
            )
            return {"FINISHED"}

        if self.action_type.__contains__(SHOW):
            self.show_obj_for_user(
                context= context,
                mesh_name= self.action_type[5:]
            )
            return {"FINISHED"}

        self.search_mesh_and_apply(
            context= context,
            mesh_name= self.action_type
        )

        return {"FINISHED"}

