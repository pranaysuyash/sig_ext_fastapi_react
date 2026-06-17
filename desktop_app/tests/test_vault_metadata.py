from __future__ import annotations

from desktop_app.processing.vault import NotaryVault


def test_vault_tracks_usage_history(tmp_path):
    vault = NotaryVault(vault_dir=str(tmp_path / "vault"))

    sig_id = vault.store_signature(
        b"png-bytes",
        {
            "source_name": "sample.png",
            "health_score": 91,
            "health_rating": "Excellent",
            "tags": ["invoice", "client-a"],
            "extraction_mode": "Standard",
        },
    )

    meta_before = vault.list_signatures()[0]
    assert meta_before["use_count"] == 0
    assert meta_before["last_used_at"] is None

    retrieved = vault.retrieve_signature(sig_id)
    assert retrieved == b"png-bytes"

    meta_after = vault.list_signatures()[0]
    assert meta_after["use_count"] == 1
    assert meta_after["last_used_at"] is not None
    assert meta_after["tags"] == ["invoice", "client-a"]
