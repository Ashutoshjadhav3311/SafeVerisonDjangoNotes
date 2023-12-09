from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Notes, Revision, RevisionCheckbox
from datetime import timedelta
from .forms import NotesForm, RevisionCheckboxForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
User = get_user_model()
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='login')  # Ensure the user is logged in to access this view
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Redirect to the profile page or any other page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'registration/password.html', {'form': form})

@login_required(login_url='login')  # login is required to render this view
def index(request):
    notes = Notes.objects.filter(user=request.user)         # Filter notes by the logged in user
    return render(request, "index.html", {"notes": notes})

def about(request):
    #notes = Notes.objects.all()
    return render(request, "about.html")
def profile(request):
    #notes = Notes.objects.all()
    return render(request, "profile.html")


def new_note(request):
    form = NotesForm()
    if request.method == 'POST':
        form = NotesForm(request.POST)
        #print(request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            revision_intervals = [3, 5, 7, 9, 10, 12]
            for interval in revision_intervals:
                revision_date = note.time + timedelta(days=interval)
                Revision.objects.create(note=note, revision_date=revision_date)

            return redirect("index")

    return render(request, "update.html", {"form": form})

@login_required(login_url='login')  # Cannot render without login   
def note_detail(request, pk):
    note = Notes.objects.get(id=pk)  # Get the note based on the provided `pk`
    form = NotesForm(instance=note)
    revision_checkboxes = RevisionCheckbox.objects.filter(revision__note=note)
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
        for revision_checkbox in revision_checkboxes:
            checkbox_data = request.POST.get(f"revision_checkboxes_{revision_checkbox.id}", False)
            checkbox_data = checkbox_data == "True"
            revision_checkbox.checked = checkbox_data
            revision_checkbox.save()

        return redirect("index")

    revision_checkbox_forms = [
        {"revision_checkbox": revision_checkbox, "form": RevisionCheckboxForm(instance=revision_checkbox)}
        for revision_checkbox in revision_checkboxes
    ]

    return render(request, "update.html", {"note": note, "form": form, "revision_checkbox_forms": revision_checkbox_forms})



# def delete_note(request, pk):
def delete_note(request, pk):
    note = Notes.objects.get(id=pk)
    form = NotesForm(instance=note)
    if request.method == 'POST':
        note.delete()
        messages.info(request, "The note has been deleted")
    return render(request, "delete.html", {"note": note, "form": form})


    