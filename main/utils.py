from .models import Image, JSON
import json


def get_info_by_title(title):
    img_all = Image.objects.get(title=title)
    json_all = JSON.objects.get(title=title)
    table_data_all = json.loads(json_all.data).items()

    title_qa = f'{title}_qa'
    img_qa = Image.objects.get(title=title_qa)
    json_qa = JSON.objects.get(title=title_qa)
    table_data_qa = json.loads(json_qa.data).items()

    return img_all, table_data_all, img_qa, table_data_qa
