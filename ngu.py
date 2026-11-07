import kagglehub

# Tải phiên bản mới nhất của dataset
path = kagglehub.dataset_download("paultimothymooney/chest-xray-pneumonia")
print("Đường dẫn lưu dữ liệu:", path)