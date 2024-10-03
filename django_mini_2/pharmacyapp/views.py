from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from pharmacyapp.forms import BoardForm, ScoreForm
from pharmacyapp.models import Pharmacy, Score, Board
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
def create_review(request, pharmacy_id):
    if request.method == 'POST':
        board_form = BoardForm(request.POST)
        if board_form.is_valid():
            board = board_form.save()
            board.user = request.user
            board.pname_id = pharmacy_id
            board.save()
            return redirect('review_list')  # 수정함
    else:
        board_form = BoardForm()
    return render(request, 'review_create.html', {'board_form': board_form})


def create_score(request, pharmacy_id):
    if request.method == 'POST':
        score_form = ScoreForm(request.POST)
        if score_form.is_valid():
            score = score_form.save(commit=False)
            score.user = request.user
            score.pharmacy_id = pharmacy_id
            score.save()
            return redirect('pharmacy_detail', pk=pharmacy_id)
    else:
        score_form = ScoreForm()
    return render(request, 'score_create.html', {'score_form': score_form})


#전체 게시글 조회
def review_list_view(request):
    reviews = Score.objects.all()
    paginator = Paginator(reviews, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reviews':page_obj,

    }
    return render(request, 'review_list.html', context)

#개별 게시글 조회
def board_detail_view(request, pk):
    board = get_object_or_404(Board, pk=pk)  # 주어진 pk에 해당하는 Board 객체를 가져옵니다.

    context = {
        'board': board,  # 템플릿에 전달할 컨텍스트
    }

    return render(request, 'board_detail.html', context)  # 템플릿을 렌더링합니다.

@login_required
def delete_score(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    if request.user == score.user:
        if request.method == 'POST':
            pharmacy_id = score.pharmacy.id
            score.delete()
            return redirect('pharmacy_detail', pk=pharmacy_id)
        return render(request, 'score_delete_confirm.html', {'score': score})
    else:
        return redirect('pharmacy_list')


def dashboard():
    return None


class SignUpView(View):
    pass

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # 사용자가 이메일로 로그인할 수 있도록 설정
        backend = 'myproject.backend.EmailAuthBackend'  # 사용할 백엔드 지정
        user = form.get_user()
        login(self.request, user, backend=backend)  # 로그인 호출 시 백엔드 지정
        return super().form_valid(form)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'base.html', {'form': form})

class BoardUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Board
    fields = ['title', 'content']
    template_name = 'board_update.html'
    success_url = reverse_lazy('board')
    permission_required = 'pharmacyapp.change_board'

    def get_queryset(self):

        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
@login_required
def nearby_pharmacies(request):
    user_lat = request.GET.get('latitude')
    user_lon = request.GET.get('longitude')
    user_location = (user_lat, user_lon)

    pharmacies = Pharmacy.objects.all()
    nearby = []

    for pharmacy in pharmacies:
        pharmacy_location = (pharmacy.latitude, pharmacy.longitude)
        distance = geodesic(user_location, pharmacy_location).km
        if distance <= 5:
            nearby.append(pharmacy)

    return render(request, 'nearby_pharmacies.html', {'pharmacies': nearby})

@login_required
def create_score(request, pharmacy_id):
    pharmacy = get_object_or_404(Pharmacy, pk=pharmacy_id)
    if request.method == 'POST':
        q1 = request.POST.get('q1_score')
        q2 = request.POST.get('q2_score')
        q3 = request.POST.get('q3_score')
        q4 = request.POST.get('q4_score')
        q5 = request.POST.get('q5_score')

        Score.objects.create(
            pharmacy=pharmacy,
            user=request.user,
            q1_score=q1,
            q2_score=q2,
            q3_score=q3,
            q4_score=q4,
            q5_score=q5,
        )
        return redirect('pharmacy_detail', pharmacy_id=pharmacy_id)

    return render(request, 'create_score.html', {'pharmacy': pharmacy})

@login_required
def pharmacy_detail(request, pharmacy_id):
    pharmacy = get_object_or_404(Pharmacy, pk=pharmacy_id)
    reviews = Board.objects.filter(pharmacy=pharmacy)
    scores = Score.objects.filter(pharmacy=pharmacy)

    return render(request, 'pharmacy_detail.html', {
        'pharmacy': pharmacy,
        'scores': scores
    })

def pharmacy_list(request):
    pharmacies = Pharmacy.objects.all()
    return render(request, 'pharmacyapp/pharmacy_list.html', {'pharmacies': pharmacies})

def home(request):
    return render(request, 'home.html')