from robocorp.tasks import task
from AlijazeeraExtractor import AljazeeraExtractor

@task
def minimal_task():
    al = AljazeeraExtractor()
    al.extractLatestNews("science")
