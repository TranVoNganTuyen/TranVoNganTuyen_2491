so_gio_lam = float(input("Nhập số giờ làm mõi tuần:"))
luong_gio =float (input("Nhập thù lao trên mỗi giờ làm tiêu chuẩn :"))
gio_tieu_chuan =44 # số giờ làm chuẩn mỗi tuần 
gio_vuot_chuan =max (0,so_gio_lam - gio_tieu_chuan) # số giờ làm vượt chuẩn mỗi tuần
thuc_lich = gio_tieu_chuan * luong_gio + gio_vuot_chuan * luong_gio *1.5 #tính tổng thu nhập
print(f"số tiền thực lĩnh của nhân viên :{thuc_lich}")
