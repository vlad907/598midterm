from django.shortcuts import render, redirect
from app1.models import ChessBoard
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from app1.forms import ChessMoveForm, JoinForm, LoginForm

@login_required(login_url='/login/')
def home(request):
    page_data = {"board": {}, "chess_form": ChessMoveForm}
    
    # If no board exists or a new game is requested
    if (ChessBoard.objects.filter(user=request.user).count() == 0) or \
       (request.method == 'POST' and 'new_game' in request.POST):
        new_game(request)
    elif request.method == 'POST':
        chess_form = ChessMoveForm(request.POST)
        if chess_form.is_valid():
            from_position = chess_form.cleaned_data["from_position"]
            to_position = chess_form.cleaned_data["to_position"]
            
            try:
                piece = ChessBoard.objects.get(user=request.user, position=from_position)
                piece.position = to_position
                piece.save()
            except ChessBoard.DoesNotExist:
                pass
        else:
            page_data["chess_form"] = chess_form
    
    # Populate page_data from ChessBoard model
    for piece in ChessBoard.objects.filter(user=request.user):
        page_data["board"][piece.position] = piece.piece_type
    
    return render(request, 'app1/home.html', page_data)

def rules(request):
    return render(request, 'app1/rules.html')

def about(request):
    return render(request, 'app1/about.html')

def new_game(request):
    starting_positions = [
        ("r1c1", "rook"), ("r1c2", "knight"), ("r1c3", "bishop"), ("r1c4", "queen"), ("r1c5", "king"),
        ("r1c6", "bishop"), ("r1c7", "knight"), ("r1c8", "rook"),
        ("r2c1", "pawn"), ("r2c2", "pawn"), ("r2c3", "pawn"), ("r2c4", "pawn"), ("r2c5", "pawn"),
        ("r2c6", "pawn"), ("r2c7", "pawn"), ("r2c8", "pawn"),
        ("r8c1", "rook"), ("r8c2", "knight"), ("r8c3", "bishop"), ("r8c4", "queen"), ("r8c5", "king"),
        ("r8c6", "bishop"), ("r8c7", "knight"), ("r8c8", "rook"),
        ("r7c1", "pawn"), ("r7c2", "pawn"), ("r7c3", "pawn"), ("r7c4", "pawn"), ("r7c5", "pawn"),
        ("r7c6", "pawn"), ("r7c7", "pawn"), ("r7c8", "pawn"),
    ]
    
    ChessBoard.objects.filter(user=request.user).delete()
    
    for position, piece in starting_positions:
        ChessBoard(user=request.user, position=position, piece_type=piece).save()

def join(request):
    if request.method == "POST":
        join_form = JoinForm(request.POST)
        if join_form.is_valid():
            user = join_form.save()
            user.set_password(user.password)
            user.save()
            return redirect("/")
        else:
            return render(request, 'app1/join.html', {"join_form": join_form})
    else:
        return render(request, 'app1/join.html', {"join_form": JoinForm})

def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    return HttpResponse("Your account is not active.")
            else:
                return render(request, 'app1/login.html', {"login_form": LoginForm})
    else:
        return render(request, 'app1/login.html', {"login_form": LoginForm})

@login_required(login_url='/login/')    
def user_logout(request):
    logout(request)
    return redirect("/")
