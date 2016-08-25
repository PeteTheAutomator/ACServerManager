from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .tasks import process_assets


@login_required
def process_assetcollection(request, assetcollection_id):
    # TODO: make it pretty (yeah - it's horrible, but let's get something vaguely working)
    process_assets(assetcollection_id)
    return redirect('/admin/library/assetcollection/')
