from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Entry
from .forms import EntryForm

@login_required
def entry_list(request):
    entries = Entry.objects.all()
    return render(request, 'journal/entry_list.html', {'entries': entries})

@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'journal/entry_detail.html', {'entry': entry})

@login_required
def entry_create(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('journal:entry_list')
    else:
        form = EntryForm()
    return render(request, 'journal/entry_form.html', {'form': form})

@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('journal:entry_detail', pk=pk) 
    else:
        form = EntryForm(instance=entry)
    return render(request, 'journal/entry_form.html', {'form': form})

@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    entry.delete()
    return redirect('journal:entry_list')
