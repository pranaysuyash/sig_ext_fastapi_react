from __future__ import annotations


class ApiClientError(RuntimeError):
    """Base class for API client failures."""


class ApiValidationError(ApiClientError):
    """Raised when the client rejects invalid input before the request."""


class ApiContractError(ApiClientError):
    """Raised when the backend response breaks the expected contract."""


class BackendUnavailable(ApiClientError):
    """Raised when the backend cannot be reached or times out."""


class AuthenticationFailed(ApiClientError):
    """Raised when credentials are rejected."""


class UploadFailed(ApiClientError):
    """Raised when image upload fails."""


class ProcessingFailed(ApiClientError):
    """Raised when image processing fails."""


class ExtractionSessionMissing(ApiClientError):
    """Raised when the backend cannot find the uploaded extraction session."""
