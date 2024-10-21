from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Tao bảng giao diện
root = Tk()
root.title("Hệ thống quản lý sinh viên")
root.geometry("600x800")

 #Kết nối tới db và tạo bảng nếu chưa tồn tại
#conn = sqlite3.connect('student_book.db')
#c = conn.cursor()

## Tạo bảng student với id làm khóa chính tự động tăng
#c.execute('''
 #   CREATE TABLE student(
  #      id INTEGER PRIMARY KEY AUTOINCREMENT, # tự động tăng
  #      ma_sv TEXT,
  #      ho TEXT,
  #      ten TEXT,
  #      ma_lop TEXT,
  #      nam_nhap_hoc INTEGER,
   #     diem_tb REAL
  #           )
 #''')

def them():
    # Kết nối và lấy dữ liệu
    # Nếu người nhập nhập thiếu dữ liệu thì gửi message nhập lại
    if not ma_sv.get() or not ho.get() or not ten.get() or not ma_lop.get() or not nam_nhap_hoc.get() or not diem_tb.get():
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
        return

# kết nối đến csdl
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()

    # Kiểm tra xem có ID nào đã bị xóa hay không, có thi sẽ lấp đầy
    c.execute('''
        SELECT id + 1 FROM student s  
        WHERE NOT EXISTS (
            SELECT 1 FROM student s2 WHERE s2.id = s.id + 1 # kiểm tra xem có bản ghi liền kề không, nếu không thì thì là rỗng
        ) ORDER BY id ASC LIMIT 1 # sắp xếp tăng dần, gt tối thiểu là 1
    ''')
    result = c.fetchone()

    # Lấy dữ liệu đã nhập
    ma_sv_value = ma_sv.get()
    ho_value = ho.get()
    ten_value = ten.get()
    ma_lop_value = ma_lop.get()
    nam_nhap_hoc_value = nam_nhap_hoc.get()
    diem_tb_value = diem_tb.get()

    # Nếu có khoảng trống trong chuỗi ID (ví dụ: do các bản ghi bị xóa),
    # hệ thống sẽ điền vào khoảng trống đó bằng cách
    #chèn bản ghi với ID cụ thể
    if result:
        next_id = result[0]
        c.execute('''
            INSERT INTO student (id, ma_sv, ho, ten, ma_lop, nam_nhap_hoc, diem_tb)
            VALUES (:id, :ma_sv, :ho, :ten, :ma_lop, :nam_nhap_hoc, :diem_tb)
        ''', {
            'id': next_id,
            'ma_sv': ma_sv_value,
            'ho': ho_value,
            'ten': ten_value,
            'ma_lop': ma_lop_value,
            'nam_nhap_hoc': nam_nhap_hoc_value,
            'diem_tb': diem_tb_value
        })
    else:
        # Nếu không có khoảng trống, chèn
        # bình thường để SQLite tự tăng ID
        c.execute('''
            INSERT INTO student (ma_sv, ho, ten, ma_lop, nam_nhap_hoc, diem_tb)
            VALUES (:ma_sv, :ho, :ten, :ma_lop, :nam_nhap_hoc, :diem_tb)
        ''', {
            'ma_sv': ma_sv_value,
            'ho': ho_value,
            'ten': ten_value,
            'ma_lop': ma_lop_value,
            'nam_nhap_hoc': nam_nhap_hoc_value,
            'diem_tb': diem_tb_value
        })

    # Cập nhật thay đổi
    conn.commit()
    conn.close()

    # Reset form
    ma_sv.delete(0, END)
    ho.delete(0, END)
    ten.delete(0, END)
    ma_lop.delete(0, END)
    nam_nhap_hoc.delete(0, END)
    diem_tb.delete(0, END)

    # Hiển thị lại dữ liệu
    truy_van()


def xoa():
    # Kiểm tra xem ô nhập liệu có trống không
    if delete_box.get() == "":
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID để xóa!")
        return

    # Kết nối tới cơ sở dữ liệu
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()

    # Kiểm tra xem ID có tồn tại không
    c.execute("SELECT * FROM student WHERE id=:id", {'id': delete_box.get()})
    record = c.fetchone()  # Lấy một bản ghi

    if record is None: # nếu id ko khớp thì hiện cảnh báo và duwngf
        messagebox.showwarning("Lỗi", "Không có bản ghi với ID đã nhập!")
        conn.close()
        return

    # Lưu lại ID của bản ghi sẽ bị xóa
    id_to_delete = int(delete_box.get())

    # Xóa bản ghi có ID đã nhập
    c.execute('''DELETE FROM student WHERE id=:id''', {'id': id_to_delete})
    conn.commit()
    conn.close()

    # Xóa nội dung của ô delete_box
    delete_box.delete(0, END)

    # Hiển thị thông báo sau khi xóa thành công
    messagebox.showinfo("Thông báo", "Đã xóa thành công!")

    # Hiển thị lại dữ liệu
    truy_van()

# trước khi thêm dữ liệu mới, tất cả các
# hàng cũ đều bị xóa để tránh trùng lặp.
def truy_van():
    # Xóa dữ liệu cũ trong TreeView
    for row in tree.get_children():
        tree.delete(row)

    # Kết nối đến cơ sở dữ liệu và lấy dữ liệu
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    c.execute("SELECT * FROM student")
    records = c.fetchall()

    # Hiển thị dữ liệu lên TreeView
    for r in records:
        tree.insert("", END, values=(r[0], r[1], r[2], r[3], r[4], r[5]))

    # Đóng kết nối
    conn.close()


def view():
    global ex1
    ex1 = Tk()
    ex1.title('Thông tin sinh viên')
    ex1.geometry("400x300")

    # Kiểm tra nếu không nhập ID
    if not delete_box.get():
        messagebox.showwarning("Lỗi", "Vui lòng nhập ID!")
        ex1.destroy()  # Đóng cửa sổ nếu không nhập ID
        return

    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute("SELECT * FROM student WHERE id=:id", {'id': record_id})
    records = c.fetchall()

    # Giả sử chỉ có một bản ghi trả về, ta lấy bản ghi đầu tiên
    if records:
        record = records[0]  # record là tuple chứa thông tin sinh viên

        global ma_sv_editor, ho_editor, ten_editor, ma_lop_editor, nam_nhap_hoc_editor, diem_tb_editor

        # Hiển thị ID (chỉ đọc)
        id_label = Label(ex1, text="ID")
        id_label.grid(row=0, column=0, pady=(10, 0))
        id_entry = Entry(ex1, width=30)
        id_entry.grid(row=0, column=1, padx=20, pady=(10, 0))
        id_entry.insert(0, record_id)
        id_entry.config(state="readonly")

        # Hiển thị thông tin sinh viên
        ma_sv_editor = Entry(ex1, width=30, state="normal")
        ma_sv_editor.grid(row=1, column=1, padx=20)
        ma_sv_editor.insert(0, record[1])  # Mã sinh viên
        ma_sv_editor.config(state="readonly")

        ho_editor = Entry(ex1, width=30, state="normal")
        ho_editor.grid(row=2, column=1)
        ho_editor.insert(0, record[2])  # Họ
        ho_editor.config(state="readonly")

        ten_editor = Entry(ex1, width=30, state="normal")
        ten_editor.grid(row=3, column=1)
        ten_editor.insert(0, record[3])  # Tên
        ten_editor.config(state="readonly")

        ma_lop_editor = Entry(ex1, width=30, state="normal")
        ma_lop_editor.grid(row=4, column=1)
        ma_lop_editor.insert(0, record[4])  # Mã lớp
        ma_lop_editor.config(state="readonly")

        nam_nhap_hoc_editor = Entry(ex1, width=30, state="normal")
        nam_nhap_hoc_editor.grid(row=5, column=1)
        nam_nhap_hoc_editor.insert(0, record[5])  # Năm nhập học
        nam_nhap_hoc_editor.config(state="readonly")

        diem_tb_editor = Entry(ex1, width=30, state="normal")
        diem_tb_editor.grid(row=6, column=1)
        diem_tb_editor.insert(0, record[6])  # Điểm trung bình
        diem_tb_editor.config(state="readonly")

        # Gắn nhãn cho các ô nhập liệu
        ma_sv_label = Label(ex1, text="Mã sinh viên")
        ma_sv_label.grid(row=1, column=0)
        ho_label = Label(ex1, text="Họ")
        ho_label.grid(row=2, column=0)
        ten_label = Label(ex1, text="Tên")
        ten_label.grid(row=3, column=0)
        ma_lop_label = Label(ex1, text="Mã lớp")
        ma_lop_label.grid(row=4, column=0)
        nam_nhap_hoc_label = Label(ex1, text="Năm nhập học")
        nam_nhap_hoc_label.grid(row=5, column=0)
        diem_tb_label = Label(ex1, text="Điểm trung bình")
        diem_tb_label.grid(row=6, column=0)

    else:
        # Nếu không tìm thấy bản ghi nào với ID đã nhập
        messagebox.showwarning("Lỗi", "Không có bản ghi với ID đã nhập!")
        ex1.destroy()  # Đóng cửa sổ sau khi hiện thông báo lỗi
        conn.close()
        return
    conn.close()
    truy_van()
def chinh_sua():
    if not delete_box.get():
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID để chỉnh sửa!")
        return
    global editor
    editor = Tk()
    editor.title('Cập nhật bản ghi')
    editor.geometry("400x300")

    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute("SELECT * FROM student WHERE id=:id", {'id': record_id})
    records = c.fetchall()

    global ma_sv_editor, ho_editor, ten_editor, ma_lop_editor, nam_nhap_hoc_editor, diem_tb_editor

    # Hiển thị ID (chỉ đọc)
    id_label = Label(editor, text="ID")
    id_label.grid(row=0, column=0, pady=(10, 0))
    id_entry = Entry(editor, width=30)
    id_entry.grid(row=0, column=1, padx=20, pady=(10, 0))
    id_entry.insert(0, record_id)
    id_entry.config(state="readonly")  # Đặt Entry thành chỉ đọc

    # Tạo các ô nhập liệu cho từng trường
    ma_sv_editor = Entry(editor, width=30)
    ma_sv_editor.grid(row=1, column=1, padx=20)
    ho_editor = Entry(editor, width=30)
    ho_editor.grid(row=2, column=1)
    ten_editor = Entry(editor, width=30)
    ten_editor.grid(row=3, column=1)
    ma_lop_editor = Entry(editor, width=30)
    ma_lop_editor.grid(row=4, column=1)
    nam_nhap_hoc_editor = Entry(editor, width=30)
    nam_nhap_hoc_editor.grid(row=5, column=1)
    diem_tb_editor = Entry(editor, width=30)
    diem_tb_editor.grid(row=6, column=1)

    # Gắn nhãn cho các ô nhập liệu
    ma_sv_label = Label(editor, text="Mã sinh viên")
    ma_sv_label.grid(row=1, column=0)
    ho_label = Label(editor, text="Họ")
    ho_label.grid(row=2, column=0)
    ten_label = Label(editor, text="Tên")
    ten_label.grid(row=3, column=0)
    ma_lop_label = Label(editor, text="Mã lớp")
    ma_lop_label.grid(row=4, column=0)
    nam_nhap_hoc_label = Label(editor, text="Năm nhập học")
    nam_nhap_hoc_label.grid(row=5, column=0)
    diem_tb_label = Label(editor, text="Điểm trung bình")
    diem_tb_label.grid(row=6, column=0)

    # Điền dữ liệu từ bản ghi vào các ô nhập liệu
    for record in records:
        ma_sv_editor.insert(0, record[1])
        ho_editor.insert(0, record[2])
        ten_editor.insert(0, record[3])
        ma_lop_editor.insert(0, record[4])
        nam_nhap_hoc_editor.insert(0, record[5])
        diem_tb_editor.insert(0, record[6])

    # Nút để lưu bản ghi sau khi chỉnh sửa
    edit_btn = Button(editor, text="Lưu bản ghi", command=lambda: cap_nhat(record_id))
    edit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=145)


def cap_nhat(record_id):
    # Kết nối tới cơ sở dữ liệu
    conn = sqlite3.connect('student_book.db')
    c = conn.cursor()

    # Kiểm tra xem ID có tồn tại không
    c.execute("SELECT * FROM student WHERE id=:id", {'id': record_id})
    record = c.fetchone()

    if record is None:
        messagebox.showwarning("Lỗi", "Không có bảng ghi với ID đã nhập!")
        conn.close()
        return

    # Cập nhật thông tin của bản ghi theo ID
    c.execute("""UPDATE student SET
           ma_sv = :ma_sv,
           ho = :ho,
           ten = :ten,
           ma_lop = :ma_lop,
           nam_nhap_hoc = :nam_nhap_hoc,
           diem_tb = :diem_tb
           WHERE id = :id""",
              {
                  'ma_sv': ma_sv_editor.get(),
                  'ho': ho_editor.get(),
                  'ten': ten_editor.get(),
                  'ma_lop': ma_lop_editor.get(),
                  'nam_nhap_hoc': nam_nhap_hoc_editor.get(),
                  'diem_tb': diem_tb_editor.get(),
                  'id': record_id
              })

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()

    # Đóng cửa sổ chỉnh sửa
    editor.destroy()

    # Hiển thị thông báo thành công
    messagebox.showinfo("Thông báo", "Đã cập nhật thành công!")

    # Cập nhật lại danh sách bản ghi sau khi chỉnh sửa
    truy_van()

# Khung cho các ô nhập liệu trong cửa sổ chính
input_frame = Frame(root)
input_frame.pack(pady=10)

# Các ô nhập liệu cho sinh viên
ma_sv = Entry(input_frame, width=30)
ma_sv.grid(row=0, column=1, padx=20, pady=(10, 0))
ho = Entry(input_frame, width=30)
ho.grid(row=1, column=1)
ten = Entry(input_frame, width=30)
ten.grid(row=2, column=1)
ma_lop = Entry(input_frame, width=30)
ma_lop.grid(row=3, column=1)
nam_nhap_hoc = Entry(input_frame, width=30)
nam_nhap_hoc.grid(row=4, column=1)
diem_tb = Entry(input_frame, width=30)
diem_tb.grid(row=5, column=1)

# Các nhãn cho các ô nhập liệu
ma_sv_label = Label(input_frame, text="Mã sinh viên")
ma_sv_label.grid(row=0, column=0, pady=(10, 0))
ho_label = Label(input_frame, text="Họ")
ho_label.grid(row=1, column=0)
ten_label = Label(input_frame, text="Tên")
ten_label.grid(row=2, column=0)
ma_lop_label = Label(input_frame, text="Mã lớp")
ma_lop_label.grid(row=3, column=0)
nam_nhap_hoc_label = Label(input_frame, text="Năm nhập học")
nam_nhap_hoc_label.grid(row=4, column=0)
diem_tb_label = Label(input_frame, text="Điểm trung bình")
diem_tb_label.grid(row=5, column=0)

# Khung cho các nút chức năng
button_frame = Frame(root)
button_frame.pack(pady=10)

# Các nút chức năng
submit_btn = Button(button_frame, text="Thêm bản ghi", command=them)
submit_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
query_btn = Button(button_frame, text="Hiển thị bản ghi", command=view)
query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
delete_box_label = Label(button_frame, text="ID")
delete_box_label.grid(row=2, column=0, pady=5)
delete_box = Entry(button_frame, width=30)
delete_box.grid(row=2, column=1, pady=5)
delete_btn = Button(button_frame, text="Xóa bản ghi", command=xoa)
delete_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=136)
edit_btn = Button(button_frame, text="Chỉnh sửa bản ghi", command=chinh_sua)
edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

# Khung cho Treeview
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Treeview để hiển thị bản ghi
columns = ("ID", "Mã sinh viên", "Họ", "Tên", "Mã lớp", "Năm nhập học", "Điểm trung bình")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
for column in columns:
    tree.column(column, anchor=CENTER)
    tree.heading(column, text=column)
tree.pack()

# Gọi hàm truy vấn để hiển thị bản ghi khi khởi động
truy_van()

root.mainloop()