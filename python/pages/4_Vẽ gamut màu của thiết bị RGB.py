import io
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
import colour.plotting as cplt
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="centered")
st.write("## Biểu đồ Gamut màu sRGB (400 nm - 700 nm)")

# TẮT TOÀN BỘ DARK THEME CỦA COLOUR-SCIENCE & MATPLOTLIB
plt.style.use('default')
try:
    cplt.colour_style(style='light')
except Exception:
    pass

# 1. Trích xuất CMFs và cắt phổ (trim) về khoảng 400nm đến 700nm
cmfs_full = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
cmfs_trimmed = cmfs_full.copy().trim(colour.SpectralShape(400, 700, 1))

# 2. Tạo khung vẽ nền trắng ngay từ đầu
fig, ax = plt.subplots(figsize=(8, 8), facecolor='white')
ax.set_facecolor('white')

# 3. Vẽ biểu đồ móng ngựa dựa trên CMFs đã trim
cplt.plot_chromaticity_diagram_CIE1931(
    cmfs=cmfs_trimmed,
    figure=fig,
    axes=ax,
    standalone=False
)

# 4. Chấm 2 điểm 400 và 700 ở chân móng ngựa
for wl, offset in [(400, (-25, -12)), (700, (8, 2))]:
    xyz_val = np.array(cmfs_full[wl], dtype=float).flatten()
    sum_xyz = np.sum(xyz_val)
    x = float(xyz_val[0] / sum_xyz)
    y = float(xyz_val[1] / sum_xyz)
    
    ax.plot(x, y, 'o', color='black', markersize=6)
    ax.annotate(
        f'{wl}', 
        xy=(x, y), 
        xytext=offset, 
        textcoords='offset points',
        fontsize=10, 
        fontweight='bold',
        color='black'
    )

# 5. Tính toán tọa độ đỉnh tam giác Gamut sRGB (Red, Green, Blue)
R = np.array([1.0, 0.0, 0.0])
G = np.array([0.0, 1.0, 0.0])
B = np.array([0.0, 0.0, 1.0])

XYZ_R = colour.sRGB_to_XYZ(R)
xyR = colour.XYZ_to_xy(XYZ_R)

XYZ_G = colour.sRGB_to_XYZ(G)
xyG = colour.XYZ_to_xy(XYZ_G)

XYZ_B = colour.sRGB_to_XYZ(B)
xyB = colour.XYZ_to_xy(XYZ_B)

tam_giac_x = [xyR[0], xyG[0], xyB[0], xyR[0]]
tam_giac_y = [xyR[1], xyG[1], xyB[1], xyR[1]]

# Vẽ tam giác Gamut sRGB màu đen nổi bật
ax.plot(tam_giac_x, tam_giac_y, 'k-', linewidth=2, label='Gamut sRGB')

# 6. Ép tiêu đề, tên trục và các con số mốc sang MÀU ĐEN
ax.set_xlim([-0.1, 0.85])
ax.set_ylim([-0.1, 0.90])
ax.set_title('CIE 1931 Chromaticity Diagram & sRGB Gamut\n(400nm - 700nm)', color='black', fontsize=11, fontweight='bold')
ax.set_xlabel('CIE x', color='black', fontsize=10)
ax.set_ylabel('CIE y', color='black', fontsize=10)
ax.tick_params(colors='black', labelsize=10)

fig.patch.set_facecolor('white')
fig.patch.set_alpha(1.0)
ax.patch.set_facecolor('white')

# 7. Xuất ảnh qua bộ nhớ đệm BytesIO dạng PNG nền trắng tuyệt đối
buf = io.BytesIO()
fig.savefig(
    buf, 
    format="png", 
    facecolor="white", 
    edgecolor="white", 
    transparent=False, 
    bbox_inches="tight", 
    pad_inches=0.3, 
    dpi=300
)
buf.seek(0)

st.image(buf)
plt.close(fig)