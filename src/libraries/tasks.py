from celery import Celery
from time import perf_counter

app = Celery('task', backend="redis://localhost", broker="redis://localhost")

@app.task()
def long_task() -> str:
    """Simula uma tarefa longa"""
    print('Calculando...')
    t1 = perf_counter()
    x = 1
    for i in range(1200):
        for j in range(1200):
            x += i**j
    t = perf_counter() - t1
    result = len(str(x)), t
    result = str(result)
    print(result)
    return result