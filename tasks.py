from robocorp.tasks import task
from AlijazeeraExtractor import AljazeeraExtractor
from robocorp import workitems
@task
def minimal_task():
    item = workitems.inputs.current
    al = AljazeeraExtractor()
    al.extractLatestNews(item.payload)
