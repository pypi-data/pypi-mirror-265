from pydantic import BaseModel


class SubtitleSettings(BaseModel):
    font: str
    font_size: int

    def to_json(self):
        return {
            "font": self.font,
            "font_size": self.font_size,
        }
