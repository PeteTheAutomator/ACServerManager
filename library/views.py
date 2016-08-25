from django.shortcuts import redirect
from .models import AssetCollection
from .tasks import process_assets
from time import sleep


def process_assetcollection(request, assetcollection_id):
    # TODO: make it pretty (yeah - it's horrible, but let's get something vaguely working)
    process_assets(assetcollection_id)
    return redirect('/admin/library/assetcollection/')
