from django.shortcuts import render
from .forms import CommentForm
from .ml_model import model


def index(request):
    form = CommentForm()
    return render(request, "index.html", {'form': form})


def get_comment(request):
    status = rating = ''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            prediction = model.comment_checking(form.data['comment'])
            status = prediction[0]
            rating = prediction[1]
    else:
        form = CommentForm()

    return render(request, 'index.html', {'form': form, 'status': status, 'rating': rating})
