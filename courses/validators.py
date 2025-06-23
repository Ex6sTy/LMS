import re
from rest_framework.exceptions import ValidationError


YOUTUBE_REGEX = re.compile(
    r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
)


def validate_youtube_link(value):
    if value and not YOUTUBE_REGEX.match(value):
        raise ValidationError("Допускаются только ссылки на youtube.com или youtu.be")
    return value
