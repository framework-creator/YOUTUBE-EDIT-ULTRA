"""The public API cannot clear Content ID; all uploads must remain private."""
import json
import sys
import types
from unittest.mock import Mock

from youtube_edit_ultra.youtube import upload


def test_requested_public_or_unlisted_upload_is_private(tmp_path, monkeypatch):
    fake_package = types.ModuleType("googleapiclient")
    fake_package.__path__ = []
    fake_http = types.ModuleType("googleapiclient.http")
    fake_http.MediaFileUpload = lambda *args, **kwargs: object()
    monkeypatch.setitem(sys.modules, "googleapiclient", fake_package)
    monkeypatch.setitem(sys.modules, "googleapiclient.http", fake_http)
    youtube = Mock()
    youtube.videos.return_value.insert.return_value.next_chunk.return_value = (
        None, {"id": "jNQXAC9IVRw"}
    )
    monkeypatch.setattr("youtube_edit_ultra.youtube.client", lambda: youtube)
    video = tmp_path / "edited.mp4"
    video.write_bytes(b"simulated fixture")
    for visibility in ("public", "unlisted"):
        state_path = tmp_path / f"{visibility}.json"
        result = upload(video, title="Demo", description="Demo", tags=[],
                        privacy=visibility, state_path=state_path)
        assert result["uploaded_privacy"] == "private"
        assert result["requested_privacy"] == visibility
        assert result["copyright_check"] == "PENDING_STUDIO_REVIEW"
        assert result["publication_requires_manual_approval"]
        assert json.loads(state_path.read_text())["uploaded_privacy"] == "private"
        call = youtube.videos.return_value.insert.call_args
        assert call.kwargs["body"]["status"]["privacyStatus"] == "private"
    assert youtube.videos.return_value.insert.call_count == 2
    # Idempotent re-run cannot create another upload.
    upload(video, title="Demo", description="Demo", tags=[],
           privacy="public", state_path=tmp_path / "public.json")
    assert youtube.videos.return_value.insert.call_count == 2
