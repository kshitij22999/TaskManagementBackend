def task_schema(data):
    return {
        "date": data.get("date"),
        "entity_name": data.get("entity_name"),
        "task_type": data.get("task_type"),
        "time": data.get("time"),
        "contact_person": data.get("contact_person"),
        "note": data.get("note", ""),
        "status": data.get("status", "open")
    }