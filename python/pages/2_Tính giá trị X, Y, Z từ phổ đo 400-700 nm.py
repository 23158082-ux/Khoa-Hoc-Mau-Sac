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
import pandas as pd
import streamlit as st

st.write("## Tính giá trị 3 thành phần (X, Y, Z)")

# Tải file CSV từ thanh bên (Sidebar)
csv_file = st.sidebar.file_uploader("Upload a csv file", type=["csv"])

if csv_file is not None:
    df_raw = pd.read_csv(csv_file, header=None)
    
    # Tự động lọc dữ liệu số, tự bỏ qua các dòng tiêu đề như 'lambda_nm'
    data_list = []
    for i in range(len(df_raw)):
        try:
            key = int(float(df_raw.iloc[i, 0]))
            val = float(df_raw.iloc[i, 1])
            data_list.append((key, val))
        except (ValueError, TypeError):
            continue  # Bỏ qua nếu dòng đó chứa chữ (header)

    if not data_list:
        st.error("File CSV không chứa dữ liệu phổ màu hợp lệ!")
    else:
        # Hiển thị xem trước dữ liệu
        s = ""
        n = len(data_list)
        
        # 5 dòng đầu
        for i in range(0, min(5, n)):
            s += "%3d %8.4f\n" % (data_list[i][0], data_list[i][1])
        
        s += "...\n"
        
        # 5 dòng cuối
        for i in range(max(0, n - 5), n):
            s += "%3d %8.4f\n" % (data_list[i][0], data_list[i][1])

        st.text(s)

        # Nút bấm tính toán XYZ
        if st.button("Tính XYZ"):
            dict_data = {k: v for k, v in data_list}

            # Tạo phân bố phổ và tính giá trị XYZ chuẩn D65
            sd = colour.SpectralDistribution(dict_data)
            cmfs = colour.MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
            illuminant = colour.SDS_ILLUMINANTS["D65"]

            XYZ = colour.sd_to_XYZ(sd, cmfs, illuminant)
            X = XYZ[0]
            Y = XYZ[1]
            Z = XYZ[2]

            st.write("### X = %.2f, Y = %.2f, Z = %.2f" % (X, Y, Z))