from .forms import ListingDataListForm, LookingDataListForm

def include_modal_context_processor(request):
    return {'listingdatalistform': ListingDataListForm(request.POST or None), 'lookingdatalistform': LookingDataListForm(request.POST or None)}
