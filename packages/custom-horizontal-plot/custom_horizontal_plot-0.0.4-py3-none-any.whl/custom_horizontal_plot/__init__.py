import os
import streamlit.components.v1 as components

_RELEASE = True 

if not _RELEASE:
    _horizontal_plot = components.declare_component(

        "horizontal_plot",

        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _horizontal_plot = components.declare_component("horizontal_plot", path=build_dir)


def horizontal_plot(data=None, titlesForChart=None, widthSet=None, useImg=None, includeBarFreq=None, styles=None, key=None, default=None):

    component_value = _horizontal_plot(data=data, titlesForChart=titlesForChart, widthSet=widthSet, useImg=useImg, includeBarFreq=includeBarFreq, styles=styles, key=key, default=default)

    return component_value
