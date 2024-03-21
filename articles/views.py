from django.shortcuts import redirect, render
from articles.models import Document
from .forms import DocumentForm

    
def documentsList(request):
    documents = Document.objects.all()
    # reader = PdfFileReader(documents.file)
    

    return render(request, 'articles/documents.html', {'document': documents})
    

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = DocumentForm()
    return render(request, 'articles/upload.html', {
        'form': form
    })

