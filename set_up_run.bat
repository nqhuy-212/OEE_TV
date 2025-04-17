@echo off
echo -------------------------------------
echo ✅ TẠO MÔI TRƯỜNG ẢO: my_env
echo -------------------------------------
if exist "my_env" (
    echo 🔄 Đang xóa môi trường cũ...
    rmdir /s /q my_env
)

py -3.13 -m venv my_env

echo -------------------------------------
echo ✅ KÍCH HOẠT MÔI TRƯỜNG ẢO
echo -------------------------------------
call my_env\Scripts\activate

echo -------------------------------------
echo ✅ CÀI CÁC THƯ VIỆN CẦN THIẾT
echo -------------------------------------
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo ⚠️ Không tìm thấy requirements.txt
)

