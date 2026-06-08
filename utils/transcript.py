from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound
)


def get_transcript(video_id, language):

    try:

        api = YouTubeTranscriptApi()

        transcript_list = api.fetch(
            video_id,
            languages=[language]
        )

        transcript = " ".join(
            chunk.text for chunk in transcript_list
        )

        return transcript

    except (TranscriptsDisabled, NoTranscriptFound):

        return None