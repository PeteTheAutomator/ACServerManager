from django.shortcuts import redirect
from .models import AssetCollection
from .tasks import process_assets
from time import sleep


def process_assets(request, asset_collection_id):
    # TODO: make it pretty (yeah - it's horrible, but let's get something vaguely working)
    process_assets(asset_collection_id)
    return redirect('/admin/library/assetcollection/')
