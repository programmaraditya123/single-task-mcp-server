import os

def cleanup_file(path: str) -> None:
    """Removes a file safely."""
    try:
        if os.path.exists(path):
            os.remove(path)
            # print(f"[INFO] Cleaned up file: {path}") # Optional logging
    except Exception as e:
        # Print error instead of crashing, as cleanup is a background task
        print(f"[ERROR] Failed to clean up file {path}: {e}")