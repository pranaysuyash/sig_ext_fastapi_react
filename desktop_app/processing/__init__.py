"""Local image processing module for signature extraction.

This module provides offline-first image processing capabilities,
eliminating the need for backend API calls for core functionality.
"""

from .extractor import SignatureExtractor, ProcessingSession, ProcessingParams, SecurityValidator

__all__ = ["SignatureExtractor", "ProcessingSession", "ProcessingParams", "SecurityValidator"]