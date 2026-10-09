import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Tiêu đề Web App ---
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# --- 2. Dữ liệu sinh viên ---
data = {
    "Ho_va_ten": [
        "Nguyễn văn An", "Trần văn Bình", "lê thị hoa", "Phạm minh Tuấn",
        "Võ hoàng Nam", "Nguyễn thị lan", "Trần minh Đức", "Lê quốc Huy",
        "Phạm thị Mai", "Hoàng văn Long"
    ],
    "chuyen_can": [9, 8, 10, 7, 8, 9, 6, 8, 9, 5],
    "Giua_ky": [8, 7, 9, 6, 8, 7, 5, 7, 8, 6],
    "Cuoi_ky": [9, 8, 9, 7, 7, 8, 6, 9, 10, 4]
}

df = pd.DataFrame(data)

# Tính điểm tổng kết
df["Tong_ket"] = (df["chuyen_can"] * 0.2 + df["Giua_ky"] * 0.3 + df["Cuoi_ky"] * 0.5).round(2)

# Hàm xếp loại
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# --- 3. Hiển thị Bảng điểm ---
st.subheader("📋 Bảng điểm của 10 sinh viên")
st.dataframe(df, use_container_width=True)

st.divider()

# --- 4. Thống kê thông tin ---
st.subheader("📊 Thống kê chung")
col1, col2 = st.columns(2)

with col1:
    dtb_lop = df["Tong_ket"].mean().round(2)
    st.metric("Điểm trung bình của lớp", dtb_lop)
    
    so_sv_dat = (df["Tong_ket"] >= 5.0).sum()
    st.metric("Số sinh viên đạt (>= 5.0)", f"{so_sv_dat} / {len(df)}")

with col2:
    sv_max = df.loc[df["Tong_ket"].idxmax()]
    st.success(f"**Sinh viên điểm cao nhất:** {sv_max['Ho_va_ten']} ({sv_max['Tong_ket']} điểm)")
    
    sv_min = df.loc[df["Tong_ket"].idxmin()]
    st.error(f"**Sinh viên điểm thấp nhất:** {sv_min['Ho_va_ten']} ({sv_min['Tong_ket']} điểm)")

st.divider()

# --- 5. Danh sách chọn sinh viên (Selectbox) ---
st.subheader("🔍 Xem chi tiết sinh viên")
selected_sv = st.selectbox("Chọn sinh viên:", df["Ho_va_ten"])

sv_info = df[df["Ho_va_ten"] == selected_sv].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", sv_info["chuyen_can"])
c2.metric("Giữa kỳ", sv_info["Giua_ky"])
c3.metric("Cuối kỳ", sv_info["Cuoi_ky"])
c4.metric("Tổng kết", sv_info["Tong_ket"])
c5.metric("Xếp loại", sv_info["Xep_loai"])

st.divider()

# --- 6. Biểu đồ cột điểm tổng kết ---
st.subheader("📈 Biểu đồ cột điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(df["Ho_va_ten"], df["Tong_ket"], color="skyblue")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)

# --- 7. Thông tin người tạo (Cuối trang, chữ nhỏ) ---
st.markdown("---")
st.caption("Người tạo ứng dụng: **Cao Xuân Phương** - MSSV: **[052208010025]**")
