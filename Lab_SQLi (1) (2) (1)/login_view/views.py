import os
from django.shortcuts import render, redirect
from django.db import connection, DatabaseError
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# --- CÁC HÀM CƠ BẢN ---

def home_view(request):
    try:
        query = "SELECT title, image_path, category FROM wallpapers WHERE is_approved = 1 AND is_private = 0"
        wallpapers = []
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                wallpapers.append({'title': row[0], 'image_path': row[1], 'category': row[2]})
        return render(request, 'index.html', {'wallpapers': wallpapers})
    except Exception:
        return render(request, 'error.html',status=500)

def login_view(request):
    error_msg = None
    if request.method == 'POST':
        email_input = request.POST.get('email')
        pass_input = request.POST.get('password')
        try:
            query = f"SELECT id, username, email, role FROM users WHERE email = '{email_input}' AND password='{pass_input}'"
            with connection.cursor() as cursor:
                cursor.execute(query) 
                user = cursor.fetchone()
            
            if user:
                request.session['user_id'] = user[0] 
                request.session['user_name'] = user[1]
                request.session['is_admin'] = (user[3] == 1)
                return redirect('admin_dashboard') if request.session['is_admin'] else redirect('home')
            else:
                error_msg = "Email hoặc mật khẩu không chính xác!"
        except Exception:
            return render(request, 'error.html',status=500)
            
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
            try:
                check_query = f"SELECT * FROM users WHERE email = '{email_input}'"
                with connection.cursor() as cursor:
                    cursor.execute(check_query)
                    existing_user = cursor.fetchone()
                
                if existing_user:
                    error_msg = "Email này đã được đăng ký. Vui lòng dùng email khác!"
                else:
                    insert_query = f"INSERT INTO users (username, email, password) VALUES ('{name_input}', '{email_input}', '{password_input}')"
                    with connection.cursor() as cursor:
                        cursor.execute(insert_query)
                    return redirect('login')
            except Exception:
                return render(request, 'error.html',status=500)
    return render(request, 'register.html', {'error': error_msg})

def logout_view(request):
    request.session.flush() 
    return redirect('login')

def index(request):
    if 'user_id' not in request.session: return redirect('login')
    query_param = request.GET.get('q', '')
    
    try:
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
        return render(request, 'index.html', {'wallpapers': wallpapers, 'search_query': query_param})
    except Exception:
        return render(request, 'error.html',status=500)

def forgot_password_view(request):
    error_msg = None
    if request.method == 'POST':
        email_input = request.POST.get('email')
        try:
            query = f"SELECT * FROM users WHERE email = '{email_input}'"
            with connection.cursor() as cursor:
                cursor.execute(query)
                user = cursor.fetchone()
                
            if user:
                return redirect(f'/password-reset-confirm/?email={email_input}')
            else:
                error_msg = "Email này không tồn tại trong hệ thống!"
        except Exception:
            return render(request, 'error.html',status=500)
    return render(request, 'forgot_password.html', {'error': error_msg})

def password_reset_confirm_view(request):
    error_msg = None
    email_url = request.GET.get('email', '')

    if request.method == 'POST':
        password_input = request.POST.get('password')
        confirm_input = request.POST.get('confirm_password')

        if password_input == confirm_input:
            try:
                query = f"UPDATE users SET password = '{password_input}' WHERE email = '{email_url}'"
                with connection.cursor() as cursor:
                    cursor.execute(query)
                return redirect('login')
            except Exception:
                return render(request, 'error.html',status=500)
        else:
            error_msg = "Mật khẩu xác nhận không khớp!"
    return render(request, 'password_reset_confirm.html', {'error': error_msg, 'email': email_url})

def upload_image_view(request):
    if 'user_id' not in request.session: return redirect('login')
    error_msg = None
        
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        is_private = int(request.POST.get('is_private', 0))
        user_id = request.session.get('user_id')
        image_file = request.FILES.get('wallpaper_file')

        if image_file:
            ext = os.path.splitext(image_file.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                error_msg = f"Lỗi: Không hỗ trợ định dạng file {ext}."
            else:
                try:
                    upload_dir = os.path.join(settings.BASE_DIR, 'static/uploads')
                    fs = FileSystemStorage(location=upload_dir)
                    filename = fs.save(image_file.name, image_file)
                    is_approved = 1 if is_private == 1 else 0
                    db_path = f"uploads/{filename}"
                    query = f"INSERT INTO wallpapers (title, image_path, category, uploader_id, is_approved, is_private) VALUES ('{title}', '{db_path}', '{category}', {user_id}, {is_approved}, {is_private})"
                    with connection.cursor() as cursor:
                        cursor.execute(query)
                    return redirect('profile' if is_private else 'home')
                except Exception:
                    return render(request, 'error.html',status=500)
    return render(request, 'uploads.html', {'error': error_msg})

def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id: return redirect('login')

    try:
        query = f"SELECT id, title, image_path, category, is_approved, is_private FROM wallpapers WHERE uploader_id = {user_id}"
        user_wallpapers = []
        with connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                user_wallpapers.append({
                    'id': row[0], 'title': row[1], 'image_path': row[2],
                    'category': row[3], 'is_approved': row[4], 'is_private': row[5],
                })
        return render(request, 'profile.html', {'user_wallpapers': user_wallpapers})
    except Exception:
        return render(request, 'error.html',status=500)

def admin_dashboard_view(request):
    if not request.session.get('is_admin'): return redirect('login')
    try:
        pending_wallpapers = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, image_path, category FROM wallpapers WHERE is_approved = 0")
            for row in cursor.fetchall():
                pending_wallpapers.append({'id': row[0], 'title': row[1], 'image_path': row[2], 'category': row[3]})
        return render(request, 'admin_dashboard.html', {'pending_wallpapers': pending_wallpapers})
    except Exception:
        return render(request, 'error.html',status=500)

def approve_image_view(request, image_id):
    if not request.session.get('is_admin'): return redirect('login')
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE wallpapers SET is_approved = 1 WHERE id = {image_id}")
        return redirect('admin_dashboard')
    except Exception:
        return render(request, 'error.html',status=500)

def reject_image_view(request, image_id):
    if not request.session.get('is_admin'): return redirect('login')
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT image_path FROM wallpapers WHERE id = %s", [image_id])
            row = cursor.fetchone()
            if row:
                full_path = os.path.join(settings.BASE_DIR, 'static', row[0])
                if os.path.exists(full_path): os.remove(full_path)
                cursor.execute("DELETE FROM wallpapers WHERE id = %s", [image_id])
        return redirect('admin_dashboard')
    except Exception:
        return render(request, 'error.html',status=500)

def manage_members_view(request):
    if not request.session.get('is_admin'): return redirect('home')
    try:
        members_data = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, username, email, role FROM users")
            for row in cursor.fetchall():
                members_data.append({
                    'id': row[0], 'username': row[1], 'email': row[2],
                    'role': 'Administrator' if row[3] == 1 else 'User'
                })
        return render(request, 'admin-manage.html', {'members': members_data})
    except Exception:
        return render(request, 'error.html',status=500)
 
def member_logs_view(request, user_id):
    if not request.session.get('is_admin'):
        return redirect('home')
    try:
        logs = []
        user_name = "Unknown"
        with connection.cursor() as cursor:
            # Lấy username
            cursor.execute("SELECT username FROM users WHERE id = %s", [user_id])
            row = cursor.fetchone()
            if row:
                user_name = row[0]

            # Lấy log của user
            cursor.execute("SELECT title, is_approved, is_private, created_at FROM wallpapers WHERE uploader_id = %s", [user_id])
            for row in cursor.fetchall():
                logs.append({
                    'title': row[0],
                    'status': "Đã duyệt" if row[1] == 1 else "Từ chối",
                    'privacy': "Riêng tư" if row[2] == 1 else "Công khai",
                    'created_at': row[3]
                })
        return render(request, 'log.html', {'logs': logs, 'user_id': user_id, 'user_name': user_name})
    except Exception as e:
        print("LỖI THẬT SỰ LÀ:", e) # Dòng này sẽ in lỗi ra Terminal
        raise e