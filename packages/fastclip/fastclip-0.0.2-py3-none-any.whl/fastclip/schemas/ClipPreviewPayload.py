from typing import List
from pydantic import BaseModel

from fastclip.enums.ClipFormat import ClipFormat
from fastclip.schemas.Word import Word


class ClipPreviewPayload(BaseModel):
    start: float
    end: float
    subtitles_settings: dict
    subtitles: List[Word] = []
    format: ClipFormat = ClipFormat.HORIZONTAL

    @property
    def has_subtitles(self):
        return len(self.subtitles) > 0
