
service = []

def add_entries(data):
    if not isinstance(data, dict) or "title" not in data or "status" not in data:
        return {"error": "Invalid payload"}
    service.append(data)
    return {"message": "service added", "data": data}

def list_existing(query=None):
    if query and "status" in query:
        return [b for b in service if b["status"] == query["status"]]
    return service

def get_stats():
    return {
        "total": len(service),
        "available": sum(1 for b in service if b["status"] == "available"),
        "issued": sum(1 for b in service if b["status"] == "issued"),
    }

def router(request_string, payload=None):
    try:
        method, path = request_string.split() 
    except:
        return {"error": "Malformed request"}

    if method not in ["GET", "POST"]:
        return {"error": "Invalid method"}

    if path == "/items":
        if method == "POST":
            return add_entries(payload)
        elif method == "GET":
            return list_existing(payload)
    elif path == "/stats" and method == "GET":
        return get_stats()

    return {"error": "Unknown path"}

print(router("POST /items", {"title": "rest_api", "status": "available"}))
print(router("POST /items", {"title": "telecom", "status": "issued"}))
print(router("GET /stats"))
print(router("GET /items"))


    
    