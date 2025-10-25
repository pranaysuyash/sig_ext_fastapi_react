from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class SessionState:
    access_token: Optional[str] = None
    user_email: Optional[str] = None
    session_id: Optional[str] = None  # image id returned by upload
    last_request: Dict[str, Any] = field(default_factory=dict)

    def auth_header(self) -> Dict[str, str]:
        if not self.access_token:
            return {}
        return {"Authorization": f"Bearer {self.access_token}"}
