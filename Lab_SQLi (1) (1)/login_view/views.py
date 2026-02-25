from django.shortcuts import render, redirect
from django.db import connection

def login_view(request):
    user = None
    error_msg = None
    if request.method == 'POST':
        email_input = request.POST.get('email')
        pass_input = request.POST.get('password')
        
        query = f"SELECT * FROM users WHERE email = '{email_input}' AND password='{pass_input}'"
        
        with connection.cursor() as cursor:
            cursor.execute(query) 
            user = cursor.fetchone()
    
        if user:
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

        if confirm_input == password_input:
            query=f"INSERT INTO users VALUES ('{name_input}', '{email_input}', '{password_input}')"
            with connection.cursor() as cursor:
                cursor.execute(query) 
             
            return redirect('login')
        else:
            error_msg = "Mật khẩu không khớp!Vui lòng nhập lại"
            
    return render(request, 'register.html', {'error': error_msg})

def index(request):
    query_param = request.GET.get('q', '')
    
    sql = "SELECT id, title, image_path, category FROM wallpapers WHERE title LIKE '" + query_param + "%'"

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