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

    def to_json(self):
        return {
            "start": self.start,
            "end": self.end,
            "subtitles_settings": self.subtitles_settings,
            "subtitles": [word.to_json() for word in self.subtitles],
            "format": self.format.value,
        }
