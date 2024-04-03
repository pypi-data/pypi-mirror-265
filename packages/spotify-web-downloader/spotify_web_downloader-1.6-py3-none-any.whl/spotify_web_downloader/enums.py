from enum import Enum


class DownloadModeSong(Enum):
    YTDLP = "ydlp"
    ARIA2C = "aria2c"


class DownloadModeVideo(Enum):
    YTDLP = "ydlp"
    NM3U8DLRE = "nm3u8dlre"
