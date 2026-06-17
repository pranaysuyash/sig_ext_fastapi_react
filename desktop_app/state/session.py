from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class PDFState:
    """State for PDF viewing and signing operations."""
    current_pdf_path: Optional[str] = None
    current_page: int = 0
    total_pages: int = 0
    zoom_level: float = 1.0
    placed_signatures: List[Dict[str, Any]] = field(default_factory=list)
    # placed_signatures format: [{"page": 0, "sig_path": "...", "x": 100, "y": 200, "width": 150, "height": 50}, ...]


@dataclass
class SessionState:
    # EXISTING FIELDS (UNCHANGED)
    access_token: Optional[str] = None
    user_email: Optional[str] = None
    session_id: Optional[str] = None  # image id returned by upload
    last_request: Dict[str, Any] = field(default_factory=dict)
    
    # NEW: PDF state (initialized to None, created on-demand)
    pdf_state: Optional[PDFState] = None

    def auth_header(self) -> Dict[str, str]:
        if not self.access_token:
            return {}
        return {"Authorization": f"Bearer {self.access_token}"}

    def set_authentication(self, access_token: str, user_email: Optional[str] = None) -> None:
        """Store authenticated user state in one place."""
        self.access_token = access_token
        self.user_email = user_email

    def clear_authentication(self) -> None:
        """Clear authenticated user state."""
        self.access_token = None
        self.user_email = None

    def set_extraction_session(self, session_id: Optional[str]) -> None:
        """Store the current extraction session id."""
        self.session_id = session_id

    def clear_extraction_session(self) -> None:
        """Clear the current extraction session id."""
        self.session_id = None
    
    # NEW: PDF state management
    def init_pdf_state(self) -> None:
        """Initialize PDF state if not already present."""
        if self.pdf_state is None:
            self.pdf_state = PDFState()
    
    def clear_pdf_state(self) -> None:
        """Clear PDF state (when closing PDF)."""
        self.pdf_state = None
