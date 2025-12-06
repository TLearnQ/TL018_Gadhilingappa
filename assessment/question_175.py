import logging

logging.basicConfig(filename="audit.log", level=logging.INFO)

def process_logs(lines):
    processed = 0
    failed = 0

    for line in lines:
        try:
            processed += 1
            if "ERROR" in line or "WARNING" in line:
                logging.info(line)
        except Exception as e:
            failed += 1
            logging.error(f"Failed to process line: {e}")

    return {"processed": processed, "failed": failed}

print(process_logs(["INFO: OK", "ERROR: Timeout", "WARNING: Low memory"]))

