from django.shortcuts import redirect, render
from .models import NguoiMuon, Sach

# Create your views here.
def signup(request):
    return render(request, 'thuvien/signup.html')

def signin(request):
    return render(request, 'thuvien/signin.html')

def logout(request):
    response = redirect('/')
    response.delete_cookie('token')
    return response

def index(request):
    try:
        nguoi_muon = NguoiMuon.objects.raw('SELECT * FROM thuvien_nguoimuon WHERE token = %s', [request.COOKIES['token']])[0]
        # get list of books and pass to template
        sachs = Sach.objects.raw('select * from thuvien_sach')
        return render(request, 'thuvien/homepage.html', {'sach': sachs, 'user': nguoi_muon})
    except:
        return signin(request)

def cart(request):
    try:
        nguoi_muon = NguoiMuon.objects.raw('SELECT * FROM thuvien_nguoimuon WHERE token = %s', [request.COOKIES['token']])[0]
        return render(request, 'thuvien/cart.html', {'user': nguoi_muon})
    except:
        return signin(request)

def history(request):
    try:
        nguoi_muon = NguoiMuon.objects.raw('SELECT * FROM thuvien_nguoimuon WHERE token = %s', [request.COOKIES['token']])[0]
        return render(request, 'thuvien/history.html', {'user': nguoi_muon})
    except:
        return signin(request)

def account(request):
    try:
        nguoi_muon = NguoiMuon.objects.raw('SELECT * FROM thuvien_nguoimuon WHERE token = %s', [request.COOKIES['token']])[0]
        return render(request, 'thuvien/account.html', {'user': nguoi_muon})
    except:
        return signin(request)

def search(request):
    try:
        nguoi_muon = NguoiMuon.objects.raw('SELECT * FROM thuvien_nguoimuon WHERE token = %s', [request.COOKIES['token']])[0]
        try:
            keyword = request.GET['search']
        except:
            return index(request)
        sachs = Sach.objects.raw('''select * FROM thuvien_sach WHERE
            tenSach LIKE %s or
            tacGia LIKE %s or
            theLoai LIKE %s or
            ngonNgu LIKE %s''', ['%' + keyword + '%','%' + keyword + '%','%' + keyword + '%','%' + keyword + '%'])
        
        return render(request, 'thuvien/search.html', {'sach': sachs, 'user': nguoi_muon})
    except:
        return signin(request)