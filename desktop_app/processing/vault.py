import os
import json
import time
import uuid
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from cryptography.fernet import Fernet

LOG = logging.getLogger(__name__)

class NotaryVault:
    """Secure local storage for extracted signatures.
    
    Signatures are encrypted at rest using AES (Fernet).
    Metadata is stored in a JSON index.
    """
    
    def __init__(self, vault_dir: Optional[str] = None):
        """Initialize the vault.
        
        Args:
            vault_dir: Custom vault directory path. If None, uses ~/.signkit/vault
        """
        if vault_dir:
            self.vault_dir = Path(vault_dir)
        else:
            self.vault_dir = Path.home() / ".signkit" / "vault"
            
        self.keys_dir = self.vault_dir / "keys"
        self.blobs_dir = self.vault_dir / "blobs"
        self.metadata_file = self.vault_dir / "metadata.json"
        
        self._ensure_structure()
        self._load_key()
        self._load_metadata()
        
    def _ensure_structure(self):
        """Create vault directory structure."""
        self.keys_dir.mkdir(parents=True, exist_ok=True)
        self.blobs_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_key(self):
        """Load or generate the master encryption key."""
        key_path = self.keys_dir / "master.key"
        if key_path.exists():
            with open(key_path, "rb") as f:
                self.key = f.read()
        else:
            LOG.info("Generating new vault master key")
            self.key = Fernet.generate_key()
            # Set restrictive permissions for key file
            with open(key_path, "wb") as f:
                f.write(self.key)
            os.chmod(key_path, 0o600)
            
        self.cipher = Fernet(self.key)
        
    def _load_metadata(self):
        """Load metadata index."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    self.metadata = json.load(f)
            except Exception as e:
                LOG.error(f"Failed to load vault metadata: {e}")
                self.metadata = {}
        else:
            self.metadata = {}
            
    def _save_metadata(self):
        """Save metadata index."""
        try:
            with open(self.metadata_file, "w") as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            LOG.error(f"Failed to save vault metadata: {e}")
            raise

    def store_signature(self, png_bytes: bytes, meta: Dict[str, Any]) -> str:
        """Encrypt and store a signature.
        
        Args:
            png_bytes: Raw PNG data
            meta: Metadata dictionary (source, date, etc.)
            
        Returns:
            Signature ID
        """
        sig_id = str(uuid.uuid4())
        
        # Encrypt data
        encrypted_data = self.cipher.encrypt(png_bytes)
        
        # Save encrypted blob
        blob_path = self.blobs_dir / f"{sig_id}.enc"
        with open(blob_path, "wb") as f:
            f.write(encrypted_data)
            
        # Update metadata
        timestamp = time.time()
        entry = {
            "id": sig_id,
            "created_at": timestamp,
            "size_bytes": len(png_bytes),
            **meta
        }
        self.metadata[sig_id] = entry
        self._save_metadata()
        
        LOG.info(f"Stored signature {sig_id} in vault")
        return sig_id
        
    def list_signatures(self) -> List[Dict[str, Any]]:
        """List all stored signatures sorted by date (newest first)."""
        sigs = list(self.metadata.values())
        sigs.sort(key=lambda x: x.get("created_at", 0), reverse=True)
        return sigs
        
    def retrieve_signature(self, sig_id: str) -> bytes:
        """Retrieve and decrypt a signature.
        
        Args:
            sig_id: Signature ID
            
        Returns:
            Decrypted PNG bytes
        """
        if sig_id not in self.metadata:
            raise ValueError(f"Signature {sig_id} not found in vault")
            
        blob_path = self.blobs_dir / f"{sig_id}.enc"
        if not blob_path.exists():
            raise FileNotFoundError(f"Encrypted blob for {sig_id} missing")
            
        with open(blob_path, "rb") as f:
            encrypted_data = f.read()
            
        return self.cipher.decrypt(encrypted_data)
        
    def delete_signature(self, sig_id: str):
        """Delete a signature from the vault."""
        if sig_id in self.metadata:
            del self.metadata[sig_id]
            self._save_metadata()
            
        blob_path = self.blobs_dir / f"{sig_id}.enc"
        if blob_path.exists():
            os.remove(blob_path)
            
        LOG.info(f"Deleted signature {sig_id} from vault")
