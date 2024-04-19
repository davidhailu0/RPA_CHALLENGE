from robocorp.tasks import task
from AlijazeeraExtractor import AljazeeraExtractor
from robocorp import workitems
@task
def minimal_task():
    item = workitems.inputs.current
    value = "Science"
    if item.payload!=None and len(item.payload)!=0 and list(item.payload.keys())[0]!='' and item.payload[list(item.payload.keys())[0]]!='':
        value = item.payload[list(item.payload.keys())[0]]
    al = AljazeeraExtractor()
    al.extractLatestNews(value)
