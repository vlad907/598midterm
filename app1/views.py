from django.shortcuts import render, redirect
from app1.models import ChessBoard
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from app1.forms import ChessMoveForm, JoinForm, LoginForm

@login_required(login_url='/login/')
def home(request):
    if not request.user.is_authenticated:
        return redirect('/login/')  # Redirects unauthenticated users to login

    # Start with a fresh instance of the form.
    chess_form_instance = ChessMoveForm()

    # If no board exists or a new game is requested, create a new game.
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
            chess_form_instance = chess_form  # Pass form with errors back to the template

    # Build a dictionary of the board from the database.
    board_dict = {}
    for piece in ChessBoard.objects.filter(user=request.user):
        board_dict[piece.position] = piece.piece_type

    # Convert the dictionary to a nested list (rows) for easier iteration.
    # We use standard chess coordinates: files "abcdefgh" and ranks "8" to "1".
    rows = []
    for rank in "87654321":
        row = []
        for file in "abcdefgh":
            pos = file + rank  # e.g., "a8", "b8", etc.
            row.append(board_dict.get(pos, ""))  # Default to empty string if no piece.
        rows.append(row)

    # Prepare context with rows and form.
    context = {
        "rows": rows,
        "chess_form": chess_form_instance,
    }
    return render(request, 'app1/home.html', context)


def rules(request):
    return render(request, 'app1/rules.html')

def about(request):
    return render(request, 'app1/about.html')

def new_game(request):
    starting_positions = [
        # Black Pieces (Top - rank 8 & 7)
        ("a8", "&#9820;"), ("b8", "&#9822;"), ("c8", "&#9821;"), ("d8", "&#9819;"),
        ("e8", "&#9818;"), ("f8", "&#9821;"), ("g8", "&#9822;"), ("h8", "&#9820;"),
        ("a7", "&#9823;"), ("b7", "&#9823;"), ("c7", "&#9823;"), ("d7", "&#9823;"),
        ("e7", "&#9823;"), ("f7", "&#9823;"), ("g7", "&#9823;"), ("h7", "&#9823;"),
        
        # White Pieces (Bottom - rank 2 & 1)
        ("a2", "&#9817;"), ("b2", "&#9817;"), ("c2", "&#9817;"), ("d2", "&#9817;"),
        ("e2", "&#9817;"), ("f2", "&#9817;"), ("g2", "&#9817;"), ("h2", "&#9817;"),
        ("a1", "&#9814;"), ("b1", "&#9816;"), ("c1", "&#9815;"), ("d1", "&#9813;"),
        ("e1", "&#9812;"), ("f1", "&#9815;"), ("g1", "&#9816;"), ("h1", "&#9814;")
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
