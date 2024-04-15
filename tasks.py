from robocorp.tasks import task
from AlijazeeraExtractor import AljazeeraExtractor

@task
def minimal_task():
    ext = AljazeeraExtractor()
    ext.extractLatestNews("science")
