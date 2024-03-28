from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Entry
from .forms import EntryForm
from .serializers import EntrySerializer

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def list(self, request):
        entries = self.queryset
        return render(request, 'journal/entry_list.html', {'entries': entries})

    def retrieve(self, request, pk=None):
        entry = get_object_or_404(self.queryset, pk=pk)
        return render(request, 'journal/entry_detail.html', {'entry': entry})

    def create(self, request):
        if request.method == 'POST':
            form = EntryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('journal:entry-list')  # Corrected view name
        else:
            form = EntryForm()
        return render(request, 'journal/entry_form.html', {'form': form})

    def update(self, request, pk=None):
        entry = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'POST':
            form = EntryForm(request.POST, instance=entry)
            if form.is_valid():
                form.save()
                return redirect('journal:entry-detail', pk=pk)  # Corrected view name
        else:
            form = EntryForm(instance=entry)
        return render(request, 'journal/entry_form.html', {'form': form})

    def destroy(self, request, pk=None):
        entry = get_object_or_404(self.queryset, pk=pk)
        entry.delete()
        return redirect('journal:entry-list')  # Corrected view name
