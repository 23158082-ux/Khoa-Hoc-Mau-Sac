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
import pandas as pd
import streamlit as st

# 1. HÀM CALLBACK KHI NẠP FILE MỚI
def process_file():
    if st.session_state.get("dem") == 1:
        st.session_state["dem"] = 0

st.set_page_config(layout='wide')

# 2. TIÊU ĐỀ MÀU TRẮNG NỔI BẬT NỀN TỐI
st.markdown("<h3 style='text-align: center; color: white;'>Vẽ gamut màu của thiết bị in</h3>", unsafe_allow_html=True)

# Khởi tạo Session State
if "data_point" not in st.session_state:
    st.session_state["data_point"] = None
if "dem" not in st.session_state:
    st.session_state["dem"] = 0

# 3. BỘ TẢI FILE CSV NẰM Ở THANH BÊN (SIDEBAR)
csv_file = st.sidebar.file_uploader("Upload a csv color gamut file", type=["csv"], on_change=process_file)

col1, col2 = st.columns(2)

# Xử lý Cột 2 (Hiển thị Bảng & Nút bấm Plot)
if csv_file is not None:
    try:
        df = pd.read_csv(csv_file)
        if 'ColorSpace' in df.columns:
            df = df.set_index('ColorSpace')
        elif 'Color' in df.columns:
            df = df.set_index('Color')
        elif 'CMYK' in df.columns:
            df = df.set_index('CMYK')
            
        col2.write("### Dữ liệu file Gamut CSV:")
        col2.write(df)
        
        if col2.button('Plot'):
            st.session_state["data_point"] = df
            st.session_state["dem"] = 1
            st.rerun()
    except Exception as e:
        col2.error(f"Lỗi đọc file CSV: {e}")

# 4. TẮT THEME TỐI VÀ VẼ ĐỒ THỊ MÓNG NGỰA NỀN TRẮNG (400 - 700 nm)
plt.style.use('default')
try:
    cplt.colour_style(style='light')
except Exception:
    pass

cmfs_full = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
cmfs_trimmed = cmfs_full.copy().trim(colour.SpectralShape(400, 700, 1))

fig, ax = plt.subplots(figsize=(7, 7), facecolor='white')
ax.set_facecolor('white')

cplt.plot_chromaticity_diagram_CIE1931(
    cmfs=cmfs_trimmed,
    figure=fig,
    axes=ax,
    standalone=False
)

# Chấm 2 điểm 400 và 700 ở chân móng ngựa
for wl, offset in [(400, (-25, -12)), (700, (8, 2))]:
    xyz_val = np.array(cmfs_full[wl], dtype=float).flatten()
    sum_xyz = np.sum(xyz_val)
    x_val = float(xyz_val[0] / sum_xyz)
    y_val = float(xyz_val[1] / sum_xyz)
    
    ax.plot(x_val, y_val, 'o', color='black', markersize=6)
    ax.annotate(
        f'{wl}', 
        xy=(x_val, y_val), 
        xytext=offset, 
        textcoords='offset points',
        fontsize=10, 
        fontweight='bold',
        color='black'
    )

# 5. TRÍCH XUẤT AN TOÀN L, a, b VÀ VẼ GAMUT MÁY IN (KHI ĐÃ BẤM PLOT)
if st.session_state.get("dem") == 1 and st.session_state.get("data_point") is not None:
    df_data = st.session_state["data_point"]
    
    px = np.zeros(7, dtype=np.float64)
    py = np.zeros(7, dtype=np.float64)
    
    order_keys = ['R', 'Y', 'G', 'C', 'B', 'M']

    def get_lab_val(df_in, key):
        if key in df_in.columns:
            val = df_in[key].to_numpy()
        elif key in df_in.index:
            val = df_in.loc[key].to_numpy()
        else:
            return np.array([50.0, 0.0, 0.0])
        val = np.array(val, dtype=float).flatten()
        return val[:3] if len(val) >= 3 else np.array([50.0, 0.0, 0.0])

    for idx, key in enumerate(order_keys):
        Lab = get_lab_val(df_data, key)
        XYZ = colour.Lab_to_XYZ(Lab)
        xy = colour.XYZ_to_xy(XYZ)
        px[idx] = xy[0]
        py[idx] = xy[1]
        
    px[6] = px[0]
    py[6] = py[0]
    
    ax.plot(px, py, 'k-', linewidth=2, label='Gamut Máy in')

# 6. ÉP MÀU NỀN TRẮNG TOÀN BỘ VÀ XUẤT BẢN ẢNH VÀO CỘT 1
ax.set_xlim([-0.1, 0.85])
ax.set_ylim([-0.1, 0.90])
ax.set_title('CIE 1931 Chromaticity Diagram (400nm - 700nm)\n2 Degree Standard Observer', color='black', fontsize=11, fontweight='bold')
ax.set_xlabel('CIE x', color='black', fontsize=10)
ax.set_ylabel('CIE y', color='black', fontsize=10)
ax.tick_params(colors='black', labelsize=10)

fig.patch.set_facecolor('white')
fig.patch.set_alpha(1.0)

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

col1.image(buf)
plt.close(fig)