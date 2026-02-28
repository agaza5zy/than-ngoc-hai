from django.shortcuts import render, redirect
from django.db import connection
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

def home_view(request):
    # Chỉ lấy những ảnh đã được phê duyệt và không phải riêng tư để hiển thị công khai
    query = "SELECT title, image_path, category FROM wallpapers WHERE is_approved = 1 AND is_private = 0"
    
    wallpapers = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Chuyển dữ liệu sang dạng list các dictionary
        for row in rows:
            wallpapers.append({
                'title': row[0],
                'image_path': row[1],
                'category': row[2]
            })
            
    # Trả về trang index.html với danh sách ảnh đã lọc
    return render(request, 'index.html', {'wallpapers': wallpapers})

def login_view(request):
    user = None
    error_msg = None
    if request.method == 'POST':
        email_input = request.POST.get('email')
        pass_input = request.POST.get('password')
        
        # Cập nhật SELECT để lấy thêm cột role (cột thứ 4)
        query = f"SELECT id, name, email, role FROM users WHERE email = '{email_input}' AND password='{pass_input}'"
        
        with connection.cursor() as cursor:
            cursor.execute(query) 
            user = cursor.fetchone()
    
        if user:
            request.session['user_id'] = user[0] 
            request.session['user_name'] = user[1]
            # Lưu quyền admin vào session (user[3] là cột role)
            request.session['is_admin'] = (user[3] == 1)
            
            # Tự động chuyển hướng nếu là Admin
            if request.session['is_admin']:
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            error_msg = "Email hoặc mật khẩu không chính xác!"
    return render(request, 'Login.html', {'error': error_msg})
    
def register_view(request):
    error_msg = None
    if request.method == 'POST':
        name_input = request.POST.get('full_name')
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')
        confirm_input = request.POST.get('confirm_password')

        if confirm_input != password_input:
            error_msg = "Mật khẩu không khớp! Vui lòng nhập lại"
        else:
            # BƯỚC KIỂM TRA: Tìm xem email đã tồn tại chưa
            check_query = f"SELECT * FROM users WHERE email = '{email_input}'"
            with connection.cursor() as cursor:
                cursor.execute(check_query)
                existing_user = cursor.fetchone()
            
            if existing_user:
                error_msg = "Email này đã được đăng ký. Vui lòng dùng email khác!"
            else:
                # Nếu chưa có thì mới INSERT
                insert_query = f"INSERT INTO users (name, email, password) VALUES ('{name_input}', '{email_input}', '{password_input}')"
                with connection.cursor() as cursor:
                    cursor.execute(insert_query)
                return redirect('login')
            
    return render(request, 'register.html', {'error': error_msg})
def logout_view(request):
    request.session.flush() 
    return redirect('login')

def index(request):
    # 1. Kiểm tra đăng nhập
    if 'user_id' not in request.session:
        return redirect('login')
    
    print(f"--- DEBUG: ID CỦA TÔI LÀ {request.session.get('user_id')} ---")
    query_param = request.GET.get('q', '')
    
    # 2. Sử dụng SELECT để lấy ảnh đã duyệt (is_approved=1)
    # Đây là nơi bạn để lỗ hổng SQL Injection cho bài Lab (nối chuỗi query_param)
    sql = "SELECT id, title, image_path, category FROM wallpapers WHERE is_approved = 1 AND is_private = 0"
    
    if query_param:
        sql += f" AND title LIKE '%{query_param}%'"

    wallpapers = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            wallpapers.append({
                'id': row[0],
                'title': row[1], 
                'image_path': row[2].strip() if row[2] else "", 
                'category': row[3]
            })

    # 3. Trả về template kèm danh sách ảnh
    return render(request, 'index.html', {'wallpapers': wallpapers, 'search_query': query_param})

def forgot_password_view(request):
    error_msg = None
    if request.method == 'POST':
        email_input = request.POST.get('email')
        
        # Kiểm tra email tồn tại bằng Raw SQL (phong cách SQL LAB)
        query = f"SELECT * FROM users WHERE email = '{email_input}'"
        with connection.cursor() as cursor:
            cursor.execute(query)
            user = cursor.fetchone()
            
        if user:
            # Nếu tìm thấy user, chuyển sang trang đổi mật khẩu
            return redirect(f'/password-reset-confirm/?email={email_input}')
        else:
            error_msg = "Email này không tồn tại trong hệ thống!"
            
    return render(request, 'forgot_password.html', {'error': error_msg})

def password_reset_confirm_view(request):
    error_msg = None
    # Lấy email từ URL (ví dụ: /password-reset-confirm/?email=user@example.com)
    email_url = request.GET.get('email', '')

    if request.method == 'POST':
        password_input = request.POST.get('password')
        confirm_input = request.POST.get('confirm_password')

        if password_input == confirm_input:
            # Truy vấn SQL thuần để cập nhật mật khẩu
            # Chú ý: Đây là điểm có thể khai thác SQL Injection nếu không được xử lý kỹ
            query = f"UPDATE users SET password = '{password_input}' WHERE email = '{email_url}'"
            
            with connection.cursor() as cursor:
                cursor.execute(query)
            
            return redirect('login')
        else:
            error_msg = "Mật khẩu xác nhận không khớp!"
            
    return render(request, 'password_reset_confirm.html', {'error': error_msg, 'email': email_url})

def upload_image_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    error_msg = None
        
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        # Lấy giá trị từ select box: '1' là riêng tư, '0' là công khai
        is_private = int(request.POST.get('is_private', 0))
        user_id = request.session.get('user_id')
        image_file = request.FILES.get('wallpaper_file')

        if image_file:
            # --- PHẦN KIỂM TRA ĐUÔI FILE ---
            ext = os.path.splitext(image_file.name)[1].lower() # Lấy đuôi file (ví dụ: .jpg)
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif'] # Danh sách cho phép
            
            if ext not in allowed_extensions:
                error_msg = f"Lỗi: Không hỗ trợ định dạng file {ext}. Chỉ cho phép upload ảnh!"
                return render(request, 'uploads.html', {'error': error_msg})
            # -------------------------------

            upload_dir = os.path.join(settings.BASE_DIR, 'static/uploads')
            fs = FileSystemStorage(location=upload_dir)
            filename = fs.save(image_file.name, image_file)
            
            is_approved = 1 if is_private == 1 else 0
            
            db_path = f"uploads/{filename}"
            query = f"INSERT INTO wallpapers (title, image_path, category, uploader_id, is_approved, is_private) \
                      VALUES ('{title}', '{db_path}', '{category}', {user_id}, {is_approved}, {is_private})"
            
            with connection.cursor() as cursor:
                cursor.execute(query)
            
            return redirect('profile' if is_private else 'home')
    
    return render(request, 'uploads.html', {'error': error_msg})

def profile_view(request):
    # 1. Kiểm tra xem người dùng đã đăng nhập chưa
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login') # Nếu chưa login thì đá về trang đăng nhập

    # 2. Truy vấn lấy tất cả ảnh của RIÊNG người dùng này
    # Lưu ý: Ở đây không lọc 'is_approved = 1' để user thấy được cả ảnh đang chờ duyệt
    query = f"SELECT id, title, image_path, category, is_approved, is_private FROM wallpapers WHERE uploader_id = {user_id}"
    
    user_wallpapers = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Chuyển đổi dữ liệu từ tuple sang dictionary để dễ dùng trong template
        for row in rows:
            user_wallpapers.append({
                'id': row[0],
                'title': row[1],
                'image_path': row[2],
                'category': row[3],
                'is_approved': row[4],
                'is_private': row[5],
            })

    # 3. Trả về template kèm danh sách ảnh
    return render(request, 'profile.html', {'user_wallpapers': user_wallpapers})

# Thêm vào cuối file views.py
def admin_dashboard_view(request):
    # Dựa trên log, bạn đã đăng nhập thành công. 
    # Tôi sẽ tạm để tất cả user đều có thể vào để bạn test, 
    # sau đó bạn có thể đổi thành if request.session.get('user_id') == 1:
    if 'user_id' not in request.session:
        return redirect('login')

    # Lấy danh sách ảnh CHƯA DUYỆT (is_approved = 0)
    query = "SELECT id, title, image_path, category FROM wallpapers WHERE is_approved = 0"
    
    pending_wallpapers = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            pending_wallpapers.append({
                'id': row[0],
                'title': row[1],
                'image_path': row[2],
                'category': row[3]
            })
            
    return render(request, 'admin_dashboard.html', {'pending_wallpapers': pending_wallpapers})

def approve_image_view(request, image_id):
    if 'user_id' not in request.session:
        return redirect('login')

    # Query cập nhật trạng thái phê duyệt
    query = f"UPDATE wallpapers SET is_approved = 1 WHERE id = {image_id}"
    with connection.cursor() as cursor:
        cursor.execute(query)
    
    return redirect('admin_dashboard')