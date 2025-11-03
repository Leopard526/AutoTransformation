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


bl_info = {
    "name": "Auto Transformation",
    "author": "Shuai Oppers",
    "version": (1, 1, 0),
    "blender": (4, 2, 0),
    "location": "VIEW_3D > Item > Apply Transform & Search Object",
    "description": "Search and apply objects, if transformation is not applied",
    "warning": "",
    "doc_url": "",
    "category": "Automation",
    
}


import bpy

from . import transform 
from . import search_apply
from . import add_on_preference

# ------------------------- properties ----------------------------- #
CLASSES = [
        transform.AutoTransformationPanel,
        transform.TransformationButtons,
        add_on_preference.AddOnPreference,
        search_apply.CollectionOperator,
        search_apply.SearchObject,
        search_apply.Setting,
    ]

PROPERTIES = {
        #transform.py
        "T_select_all": bpy.props.BoolProperty(name="Select All Transform", default=False),
        "T_apply_location": bpy.props.BoolProperty(name="Location Transform", default=False),
        "T_apply_rotation": bpy.props.BoolProperty(name="Rotation Transform", default=False),
        "T_apply_scale": bpy.props.BoolProperty(name="Scale Transform", default=False),
        
        #search_object.py
        "S_settings": bpy.props.BoolProperty(name="Setting Search", default=False),
        "S_viewport": bpy.props.BoolProperty(name="Setting Viewport", default=True),
        "S_sellect_all": bpy.props.BoolProperty(name="Setting Sellect All", default=True),
        "S_location": bpy.props.BoolProperty(name="Setting Location", default=True),
        "S_rotation": bpy.props.BoolProperty(name="Setting Rotation", default=True),
        "S_scale": bpy.props.BoolProperty(name="Setting Scale", default=True),

    }

# ------------------------- Initilizer ----------------------------- #
def unregister_properties():
    for prop in PROPERTIES.keys():
        delattr(bpy.types.Scene, prop)

def register_properties():
    for prop, value in PROPERTIES.items():
        setattr(bpy.types.Scene, prop, value)

def register() -> None:
    register_properties()

    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister() -> None:
    unregister_properties()

    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
