from .celery_app import celery_app

@celery_app.task(name="process_staging")
def process_staging(staging_id: int):
    # Placeholder durable worker task
    print(f"Processing staging id={staging_id}")
    return {"staging_id": staging_id, "status": "processed"}
