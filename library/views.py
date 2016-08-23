from django.shortcuts import redirect
from .models import Document
from .tasks import process_assets
from time import sleep


def process_document(request, document_id):
    # TODO: make it pretty (yeah - it's horrible, but let's get something vaguely working)
    process_assets(document_id)
    return redirect('/admin/library/document/')