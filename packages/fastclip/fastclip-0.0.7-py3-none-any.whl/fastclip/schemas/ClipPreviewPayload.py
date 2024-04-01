from typing import List
from pydantic import BaseModel

from fastclip.enums.ClipFormat import ClipFormat
from fastclip.schemas.SubtitleSettings import SubtitleSettings
from fastclip.schemas.Word import Word


class ClipPreviewPayload(BaseModel):
    start: float
    end: float
    subtitles_settings: SubtitleSettings
    subtitles: List[Word] = []
    format: ClipFormat = ClipFormat.HORIZONTAL
    has_subtitles: bool = False

    def to_json(self):
        return {
            "start": self.start,
            "end": self.end,
            "subtitles_settings": self.subtitles_settings.to_json(),
            "subtitles": [word.to_json() for word in self.subtitles],
            "format": self.format.value,
            "has_subtitles": self.has_subtitles,
        }
