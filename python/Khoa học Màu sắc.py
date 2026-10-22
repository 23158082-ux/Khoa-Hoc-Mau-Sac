import os
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Khoa học Màu sắc - HCMUTE",
    page_icon="🎨",
    layout="wide"
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
logo_folder = os.path.join(CURRENT_DIR, "logo")


def load_equal_logo(image_path, target_height=130):
    try:
        img = Image.open(image_path)
        w, h = img.size
        new_w = int(w * (target_height / h))
        return img.resize((new_w, target_height), Image.Resampling.LANCZOS)
    except Exception:
        return image_path

st.sidebar.markdown("## 📌 THÔNG TIN NHÓM")
st.sidebar.write("**Thành viên 1:** Võ Minh Thái")
st.sidebar.write("**MSSV:** 23158141")
st.sidebar.write("**Thành viên 2:** Nguyễn Đăng Khoa")
st.sidebar.write("**MSSV:** 23158082")
st.sidebar.markdown("---")

# Tải Logo ở Sidebar
if os.path.exists(logo_folder):
    logo_files = sorted([
        os.path.join(logo_folder, f) 
        for f in os.listdir(logo_folder) 
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg'))
    ])
    for l_path in logo_files:
        st.sidebar.image(l_path, use_container_width=True)
    if logo_files:
        st.sidebar.markdown("---")

col_logo1, col_title, col_logo2 = st.columns([1, 2.8, 1], vertical_alignment="center")

if os.path.exists(logo_folder):
    logo_files = sorted([
        os.path.join(logo_folder, f) 
        for f in os.listdir(logo_folder) 
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg'))
    ])
    
    if len(logo_files) >= 2:
        col_logo1.image(load_equal_logo(logo_files[0], target_height=130))
        col_logo2.image(load_equal_logo(logo_files[1], target_height=130))
    elif len(logo_files) == 1:
        col_logo1.image(load_equal_logo(logo_files[0], target_height=130))

with col_title:
    st.markdown(
        "<h4 style='text-align: center; color: #4A90E2; font-weight: bold; margin-bottom: 2px; font-size: 18px;'>"
        "TRƯỜNG ĐẠI CÔNG NGHỆ KỸ THUẬT TP. HỒ CHÍ MINH"
        "</h4>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<h5 style='text-align: center; color: #AAAAAA; margin-top: 0px; margin-bottom: 10px; font-size: 14px;'>"
        "KHOA MỸ THUẬT VÀ TRUYỀN THÔNG"
        "</h5>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<h1 style='text-align: center; color: white; font-size: 28px; font-weight: bold; margin: 0;'>"
        "KHOA HỌC MÀU SẮC"
        "</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-size: 15px; color: #DDDDDD; font-style: italic; margin-top: 5px; margin-bottom: 0;'>"
        "Ứng dụng tính toán và trực quan hóa trong Khoa học màu sắc"
        "</p>", 
        unsafe_allow_html=True
    )

st.markdown("---")


# ==============================================================================
# 3. GIỚI THIỆU TRANG WEB & HƯỚNG DẪN SỬ DỤNG
# ==============================================================================
st.subheader("Giới thiệu trang web")
st.write(
    "Trang web được xây dựng bằng **Python** và **Streamlit** để thực hiện các bài toán trong môn **Khoa học Màu sắc**."
)

st.write("""
**Hướng dẫn sử dụng:**
Sử dụng **Menu ở thanh bên trái** để chọn các chức năng tính toán:
1. **Chuyển đổi không gian màu qua lại giữa sRGB và XYZ**
2. **Tính giá trị X, Y, Z từ phổ đo 400-700 nm**
3. **Vẽ biểu đồ CIE hình móng ngựa (400 - 700 nm)**
4. **Vẽ Gamut màu của thiết bị RGB**
5. **Vẽ Gamut màu của máy in của khoa từ file Gamut**
6. **Đặc tính hoá của máy in nửa tông**
7. **Biểu đồ CIE Band (400 - 700 nm)**
8. **Phân tích & Tính toán sai lệch màu Delta E (CIEDE2000 & CIE1976)**
""")

st.write("---")
st.caption("TRANG WEB ĐƯỢC VIẾT VÀ LẬP TRÌNH BỞI SINH VIÊN NÊN CÓ THỂ XẢY RA 1 VÀI LỖI KHÔNG MONG MUỐN.")
st.caption("Xin vui lòng sử dụng trang web để phục vụ mục đích tham khảo (không nên sử dụng vào môi trường làm việc thực tế vì có thể có sai xót).")
st.caption("GVHD: Trần Tiến Đức.")
