import uuid

class SessionManager:
    @staticmethod
    def generate_session_id() -> str:
        return str(uuid.uuid4())
