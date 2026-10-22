import numpy as np

for attr, val in [
    ("float", float),
    ("float_", np.float64),
    ("int", int),
    ("int_", np.int64),
    ("bool", bool),
    ("complex", complex),
    ("complex_", np.complex128),
    ("in1d", np.isin),
    ("asscalar", lambda a: a.item()),
    ("product", np.prod),
    ("cumproduct", np.cumprod),
]:
    if not hasattr(np, attr):
        setattr(np, attr, val)

if not hasattr(np, "sctypes"):
    np.sctypes = {
        'int': [np.int8, np.int16, np.int32, np.int64],
        'float': [np.float16, np.float32, np.float64, getattr(np, 'longdouble', np.float64)],
        'complex': [np.complex64, np.complex128],
        'bool': [bool],
        'others': [object, bytes, str, np.void]
    }
# ==============================================================================

import colour
import streamlit as st

st.write("## Chuyển đổi không gian màu")

chon_khong_gian_mau = st.sidebar.radio(
    "Chuyển đổi không gian màu", ("sRGB sang XYZ", "XYZ sang sRGB")
)

col1, col2 = st.columns(2)

if chon_khong_gian_mau == "sRGB sang XYZ":
    with col1:
        st.write("### sRGB sang XYZ")
        R = st.number_input("Nhập R:", value=255.0)
        G = st.number_input("Nhập G:", value=0.0)
        B = st.number_input("Nhập B:", value=0.0)
        if st.button("Chuyển sang XYZ"):
            r_norm = R / 255.0
            g_norm = G / 255.0
            b_norm = B / 255.0
            RGB = np.array([r_norm, g_norm, b_norm])
            XYZ = colour.sRGB_to_XYZ(RGB)
            X = XYZ[0] * 100
            Y = XYZ[1] * 100
            Z = XYZ[2] * 100
            st.write("### X = %.2f, Y = %.2f, Z = %.2f" % (X, Y, Z))

elif chon_khong_gian_mau == "XYZ sang sRGB":
    with col1:
        st.write("### XYZ sang sRGB")
        X = st.number_input("Nhập X:", value=41.24)
        Y = st.number_input("Nhập Y:", value=21.26)
        Z = st.number_input("Nhập Z:", value=1.93)
        if st.button("Chuyển sang sRGB"):
            x_norm = X / 100.0
            y_norm = Y / 100.0
            z_norm = Z / 100.0
            XYZ = np.array([x_norm, y_norm, z_norm])
            RGB = colour.XYZ_to_sRGB(XYZ)
            R = RGB[0] * 255
            G = RGB[1] * 255
            B = RGB[2] * 255
            st.write("### R = %.0f, G = %.0f, B = %.0f" % (R, G, B))