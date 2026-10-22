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

import colour
import streamlit as st

st.set_page_config(layout="wide")

st.markdown("<h2 style='text-align: center; color: white;'>8. Tính toán & Phân tích sai lệch màu Delta E (ΔE)</h2>", unsafe_allow_html=True)
st.write("Công cụ so sánh khoảng cách màu giữa 2 mẫu màu theo các tiêu chuẩn **CIE 1976** và **CIEDE2000** (chuẩn công nghiệp in ấn & hiển thị).")

col_left, col_right = st.columns(2)

with col_left:
    st.write("### 🎨 Chọn mẫu màu 1 (Màu chuẩn - Reference)")
    color1_hex = st.color_picker("Chọn màu mẫu 1", "#00FF00", key="c1")
    
    st.write("### 🎨 Chọn mẫu màu 2 (Màu đo - Sample)")
    color2_hex = st.color_picker("Chọn màu mẫu 2", "#8000FF", key="c2")

# Quy đổi Hex -> RGB (0..1) -> XYZ -> Lab
def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return np.array([int(hex_str[i:i+2], 16) for i in (0, 2, 4)], dtype=float) / 255.0

rgb1 = hex_to_rgb(color1_hex)
rgb2 = hex_to_rgb(color2_hex)

XYZ1 = colour.sRGB_to_XYZ(rgb1)
Lab1 = colour.XYZ_to_Lab(XYZ1)

XYZ2 = colour.sRGB_to_XYZ(rgb2)
Lab2 = colour.XYZ_to_Lab(XYZ2)

# Ép mảng Lab về float thuần
lab1_vals = np.array(Lab1, dtype=float).flatten()
L1, a1, b1 = float(lab1_vals[0]), float(lab1_vals[1]), float(lab1_vals[2])

lab2_vals = np.array(Lab2, dtype=float).flatten()
L2, a2, b2 = float(lab2_vals[0]), float(lab2_vals[1]), float(lab2_vals[2])

# Tính Delta E
try:
    de76_raw = colour.delta_E(Lab1, Lab2, method='CIE 1976')
except Exception:
    de76_raw = colour.delta_E(Lab1, Lab2)

try:
    de2000_raw = colour.delta_E(Lab1, Lab2, method='CIE 2000')
except Exception:
    try:
        de2000_raw = colour.delta_E(Lab1, Lab2, method='CIEDE2000')
    except Exception:
        de2000_raw = de76_raw

delta_e_76 = float(np.array(de76_raw, dtype=float).flatten()[0])
delta_e_2000 = float(np.array(de2000_raw, dtype=float).flatten()[0])

with col_right:
    st.write("### 📊 Kết quả tính toán sai lệch màu")
    
    # Hiển thị riêng 3 ô L*, a*, b* cho Mẫu 1
    st.write("#### 🟩 Mẫu 1 (Màu chuẩn - CIELAB):")
    m1_c1, m1_c2, m1_c3 = st.columns(3)
    m1_c1.metric("L*", f"{L1:.2f}")
    m1_c2.metric("a*", f"{a1:.2f}")
    m1_c3.metric("b*", f"{b1:.2f}")

    # Hiển thị riêng 3 ô L*, a*, b* cho Mẫu 2
    st.write("#### 🟪 Mẫu 2 (Màu đo - CIELAB):")
    m2_c1, m2_c2, m2_c3 = st.columns(3)
    m2_c1.metric("L*", f"{L2:.2f}")
    m2_c2.metric("a*", f"{a2:.2f}")
    m2_c3.metric("b*", f"{b2:.2f}")
    
    st.markdown("---")
    st.write(f"#### 🔹 $\Delta E_{{76}}$ (CIE 1976): **{delta_e_76:.2f}**")
    st.write(f"#### 🔹 $\Delta E_{{00}}$ (CIEDE2000): **{delta_e_2000:.2f}**")
    
    # Đánh giá mức độ nhận biết của mắt người
    st.write("#### 👁️ Đánh giá khả năng phân biệt của mắt người:")
    if delta_e_2000 < 1.0:
        st.success("✅ **ΔE < 1.0**: Mắt người không thể nhận ra sự khác biệt.")
    elif 1.0 <= delta_e_2000 <= 2.0:
        st.info("ℹ️ **1.0 ≤ ΔE ≤ 2.0**: Rất khó nhận biết, chỉ chuyên gia quan sát kỹ mới thấy.")
    elif 2.0 < delta_e_2000 <= 10.0:
        st.warning("⚠️ **2.0 < ΔE ≤ 10.0**: Nhìn lướt qua đã phát hiện sự chênh lệch màu.")
    else:
        st.error("❌ **ΔE > 10.0**: Hai màu hoàn toàn khác biệt nhau.")