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

# 1. TIÊU ĐỀ CHỮ MÀU TRẮNG NỔI BẬT NỀN TỐI
st.markdown("<h2 style='text-align: center; color: white;'>7. Biểu đồ dải phổ màu CIE Band (400 nm - 700 nm)</h2>", unsafe_allow_html=True)
st.write("Biểu đồ trực quan hóa dải màu phổ (Visible Spectrum Band) kết hợp với 3 đường hàm phối màu CIE 1931 Standard Observer CMFs trong khoảng bước sóng **400 nm - 700 nm**.")

# Tắt Dark Theme ngầm của colour-science & matplotlib
plt.style.use('default')
try:
    cplt.colour_style(style='light')
except Exception:
    pass

# 2. TRÍCH XUẤT CMFs CIE 1931 VÀ CẮT PHỔ NGHÊU (TRIM 400 - 700 NM)
cmfs_full = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
cmfs_trimmed = cmfs_full.copy().trim(colour.SpectralShape(400, 700, 1))

wavelengths = cmfs_trimmed.wavelengths
x_bar = cmfs_trimmed.values[:, 0]
y_bar = cmfs_trimmed.values[:, 1]
z_bar = cmfs_trimmed.values[:, 2]

# 3. TẠO KHUNG VẼ 2 ĐỒ THỊ (HÀM CMFs VÀ DẢI BĂNG MÀU PHỔ)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), gridspec_kw={'height_ratios': [3, 1]}, facecolor='white')
fig.subplots_adjust(hspace=0.35)

# --- ĐỒ THỊ TRÊN: 3 ĐƯỜNG HÀM PHỐI MÀU CMFs ---
ax1.plot(wavelengths, x_bar, 'r-', linewidth=2, label=r'$\bar{x}(\lambda)$ (Red)')
ax1.plot(wavelengths, y_bar, 'g-', linewidth=2, label=r'$\bar{y}(\lambda)$ (Green)')
ax1.plot(wavelengths, z_bar, 'b-', linewidth=2, label=r'$\bar{z}(\lambda)$ (Blue)')

ax1.set_xlim([400, 700])
ax1.set_ylim([0, max(max(x_bar), max(y_bar), max(z_bar)) * 1.05])
ax1.set_title('Đường hàm phối màu CIE 1931 Standard Observer CMFs', color='black', fontsize=11, fontweight='bold')
ax1.set_ylabel('Giá trị CMFs', color='black', fontsize=10)
ax1.tick_params(colors='black', labelsize=10)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='upper right')
ax1.set_facecolor('white')

# --- ĐỒ THỊ DƯỚI: THANH DẢI MÀU PHỔ (CIE BAND) ---
spectrum_colors = []
for wl in wavelengths:
    xyz = cmfs_full[wl]
    max_val = np.max(xyz)
    # Quy đổi XYZ về không gian màu sRGB hiển thị
    rgb = colour.XYZ_to_sRGB(xyz / max_val if max_val > 0 else xyz)
    rgb = np.clip(rgb, 0, 1)
    spectrum_colors.append(rgb)

spectrum_array = np.array(spectrum_colors).reshape(1, -1, 3)

ax2.imshow(spectrum_array, extent=[400, 700, 0, 1], aspect='auto')
ax2.set_xlim([400, 700])
ax2.set_yticks([])  # Ẩn trục dọc Y của dải màu
ax2.set_xlabel('Bước sóng $\lambda$ (nm)', color='black', fontsize=10)
ax2.tick_params(colors='black', labelsize=10)
ax2.set_title('Dải phổ màu quan sát (CIE Spectral Band: 400 - 700 nm)', color='black', fontsize=10, fontweight='bold')

# 4. ÉP MÀU NỀN TRẮNG PHẲNG CHO TOÀN BỘ KHUNG HÌNH
fig.patch.set_facecolor('white')
fig.patch.set_alpha(1.0)

# 5. XUẤT ẢNH QUA BỘ NHỚ ĐỆM BYTESIO DẠNG PNG NỀN TRẮNG PURE
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

# Hiển thị ảnh và đóng figure
st.image(buf)
plt.close(fig)