import uuid
# Helper function to check if a string is a valid UUID
def is_valid_uuid(uuid_string):
    try:
        uuid.UUID(uuid_string, version=4)
        return True
    except ValueError:
        return False