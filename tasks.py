from robocorp.tasks import task
from AlijazeeraExtractor import AljazeeraExtractor
from RPA.Robocorp.WorkItems import WorkItems
@task
def minimal_task():
    item = WorkItems()
    # payload = item.get_work_item_payload()
    # print(payload)
    value = "Science"
    # if item.payload!=None and len(item.payload)!=0 and list(item.payload.keys())[0]!='' and item.payload[list(item.payload.keys())[0]]!='':
    #     value = item.payload[list(item.payload.keys())[0]]
    al = AljazeeraExtractor()
    al.extract_latest_news(value)
