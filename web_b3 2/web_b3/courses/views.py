import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Course
from openai import OpenAI

# Khởi tạo API ChatGPT
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "sk-dummy"))

# --- CHỨC NĂNG CŨ ---
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('course_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('course_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.students.add(request.user)
    return redirect('course_detail', pk=pk)

# --- CHỨC NĂNG CHATBOT MỚI ---
def chatbot_view(request):
    return render(request, 'courses/chatbot.html')

def chat_api(request):
    query = request.GET.get('msg', '').lower()
    
    # Ưu tiên 1: Tìm trong Database khóa học
    results = Course.objects.filter(title__icontains=query)
    if results.exists():
        course = results.first()
        return JsonResponse({'response': f"Tôi tìm thấy khóa học '{course.title}' trong hệ thống. Bạn hãy ra trang chủ để xem chi tiết nhé!"})
    
    # Ưu tiên 2: Nhờ ChatGPT tư vấn
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý ảo hỗ trợ học tập, thư viện và tìm vé máy bay. Trả lời ngắn gọn, thân thiện bằng tiếng Việt."},
                {"role": "user", "content": query}
            ]
        )
        response = completion.choices[0].message.content
    except Exception as e:
        # Câu trả lời thân thiện dành cho học sinh/giáo viên khi AI không phản hồi
        response = "Xin lỗi bạn, hiện tại hệ thống tư vấn đang hơi quá tải một chút. Nhưng bạn yên tâm, tôi vẫn có thể giúp bạn tìm các khóa học đang có trên web. Bạn muốn tìm hiểu môn gì nhỉ?"
        
    return JsonResponse({'response': response})