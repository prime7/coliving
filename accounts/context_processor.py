from .forms import DataListForm

def include_modal_context_processor(request):
    return {'form': DataListForm(request.POST or None)}
