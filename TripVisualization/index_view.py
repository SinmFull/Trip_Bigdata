from django.shortcuts import render
from django.views.decorators import csrf
import pymongo
from . import setting
import random
from django.http import JsonResponse
# from django.conf import settings

# settings.configure()

def index(request):  # index页面加载
    context = {}
    return render(request, 'index.html', context)

def get_poi_data(request):
    # 建立与MongoDB的连接
    client = pymongo.MongoClient(host=setting.MONGODB_HOST, port=setting.MONGODB_PORT)
    db = client[setting.MONGODB_NAME]
    collection = db['my_col']
    print(f'连接MongoDB {setting.MONGODB_NAME}.{collection.name} 成功')

    poi_data = list(collection.find({}, {'_id': 0}))
    # print(poi_data[0:10])
    new_list = random.sample(poi_data,5000)
    sorted_list = sorted(new_list, key=lambda x: x['properties']['hot_score'],reverse=True)
    # print(sorted_list[0])
    geojson = {'type': 'FeatureCollection', 'features': sorted_list}
    return JsonResponse(geojson, safe=False)
