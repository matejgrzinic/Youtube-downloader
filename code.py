# The below imports are required by the patch
import json
from urllib.parse import parse_qs, unquote

# This function is based off on the changes made in
# https://github.com/nficano/pytube/pull/643

def apply_descrambler(stream_data, key):
    """Apply various in-place transforms to YouTube's media stream data.
    Creates a ``list`` of dictionaries by string splitting on commas, then
    taking each list item, parsing it as a query string, converting it to a
    ``dict`` and unquoting the value.
    :param dict stream_data:
        Dictionary containing query string encoded values.
    :param str key:
        Name of the key in dictionary.
    **Example**:
    >>> d = {'foo': 'bar=1&var=test,em=5&t=url%20encoded'}
    >>> apply_descrambler(d, 'foo')
    >>> print(d)
    {'foo': [{'bar': '1', 'var': 'test'}, {'em': '5', 't': 'url encoded'}]}
    """
    otf_type = "FORMAT_STREAM_TYPE_OTF"

    if key == "url_encoded_fmt_stream_map" and not stream_data.get(
        "url_encoded_fmt_stream_map"
    ):
        formats = json.loads(stream_data["player_response"])["streamingData"]["formats"]
        formats.extend(
            json.loads(stream_data["player_response"])["streamingData"][
                "adaptiveFormats"
            ]
        )
        try:
            stream_data[key] = [
                {
                    "url": format_item["url"],
                    "type": format_item["mimeType"],
                    "quality": format_item["quality"],
                    "itag": format_item["itag"],
                    "bitrate": format_item.get("bitrate"),
                    "is_otf": (format_item.get("type") == otf_type),
                }
                for format_item in formats
            ]
        except KeyError:
            cipher_url = []
            for data in formats:
                cipher = data.get("cipher") or data["signatureCipher"]
                cipher_url.append(parse_qs(cipher))
            stream_data[key] = [
                {
                    "url": cipher_url[i]["url"][0],
                    "s": cipher_url[i]["s"][0],
                    "type": format_item["mimeType"],
                    "quality": format_item["quality"],
                    "itag": format_item["itag"],
                    "bitrate": format_item.get("bitrate"),
                    "is_otf": (format_item.get("type") == otf_type),
                }
                for i, format_item in enumerate(formats)
            ]
    else:
        stream_data[key] = [
            {k: unquote(v) for k, v in parse_qsl(i)}
            for i in stream_data[key].split(",")
        ]


import pytube
import time
import sys
import os

pytube.__main__.apply_descrambler = apply_descrambler

def download(url, file_format, quality, output, filename):    
        
    yt = pytube.YouTube(url)  
    
    filename = yt.title if not filename else filename
    
    if file_format == "mp3":
        file = yt.streams.get_audio_only()
    elif file_format == "mp4":
        file = yt.streams.get_highest_resolution()
    
    return (file.download(output, filename), yt.length)
    
    