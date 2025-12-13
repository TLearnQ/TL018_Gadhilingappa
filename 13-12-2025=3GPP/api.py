import yaml, json, os, logging

# ---- Custom API Error ----
class APIResponseError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status

# ---- File Path ----
url = r"C:\Users\ADMIN\OneDrive\Desktop\telcom\5gapi\etc.yaml"

# ---- Logging Setup ----
log_file = r"C:\Users\ADMIN\OneDrive\Desktop\telcom\5gapi\logss.txt"
err_file = r"C:\Users\ADMIN\OneDrive\Desktop\telcom\5gapi\logss.txt"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Starting service extraction")

try:
    # ---- Load YAML ----
    logging.info(f"Loading YAML: {url}")
    with open(url) as file:
        data = yaml.safe_load(file)
    if not data:
        raise APIResponseError("YAML file is empty or unreadable")

    # ---- Validate paths ----
    paths = data.get("paths")
    if paths is None:
        raise APIResponseError("Missing 'paths' section in OpenAPI spec")

    metadata = []

    # ---- Summary Aggregation Variables ----
    method_count = {}
    endpoints_with_resp = 0
    endpoints_without_resp = 0
    request_response_map = []
    auth_methods = data.get("components", {}).get("securitySchemes", {})

    # ---- Extract services ----
    for path, methods in paths.items():
        for method, details in methods.items():
            if method.lower() in ["get", "post", "put", "delete", "patch"]:
                
                # Count HTTP methods
                method_count[method.upper()] = method_count.get(method.upper(), 0) + 1

                responses = details.get("responses", {})
                if responses:
                    endpoints_with_resp += 1
                else:
                    endpoints_without_resp += 1

                request_response_map.append({
                    "path": path,
                    "method": method.upper(),
                    "responses": list(responses.keys())
                })

                entry = {
                    "path": path,
                    "method": method.upper(),
                    "summary": details.get("summary"),
                    "description": details.get("description"),
                    "operationId": details.get("operationId"),
                    "tags": details.get("tags"),
                    "responses": responses
                }
                metadata.append(entry)
                logging.info(f"Extracted endpoint: {method.upper()} {path}")

    if not metadata:
        raise APIResponseError("No endpoints found in the API spec")

    # ---- Save metadata to JSON ----
    out_file = r"C:\Users\ADMIN\OneDrive\Desktop\telcom\5gapi\api_output.json"
    with open(out_file, "w") as f:
        json.dump(metadata, f, indent=2)

    logging.info("Services saved")

    # ---- SUMMARY OUTPUT ----
    summary = {
        "http_method_count": method_count,
        "endpoints_with_responses": endpoints_with_resp,
        "endpoints_without_responses": endpoints_without_resp,
        "authentication_methods": list(auth_methods.keys()),
        "request_response_map": request_response_map,
        "total_endpoints": len(metadata)
    }

    summary_file = r"C:\Users\ADMIN\OneDrive\Desktop\telcom\5gapi\summary.txt"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    logging.info("Summary saved successfully")

    print("Services saved to:", out_file)
    print("Summary saved to:", summary_file)
    print("Logs saved to:", log_file)

except FileNotFoundError as e:
    with open(err_file, "a") as ef:
        ef.write(str(e) + "\n")
    logging.error("YAML file not found")
    raise APIResponseError("YAML file not found on disk")

except APIResponseError as e:
    with open(err_file, "a") as ef:
        ef.write("APIResponseError: " + str(e) + "\n")
    logging.error(f"APIResponseError: {e}")
    print("ERROR:", e)

except Exception as e:
    with open(err_file, "a") as ef:
        ef.write("Unexpected Error: " + str(e) + "\n")
    logging.error(f"Unexpected error: {e}")
    raise APIResponseError("Unknown error occurred while processing YAML")

