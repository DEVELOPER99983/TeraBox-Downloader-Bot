import re
import time
from urllib.parse import parse_qs, urlparse

import requests

from tools import get_formatted_size


# ---------------- URL VALIDATION ---------------- #

def check_url_patterns(url):
    patterns = [
        r"ww\.mirrobox\.com",
        r"www\.nephobox\.com",
        r"freeterabox\.com",
        r"www\.freeterabox\.com",
        r"1024tera\.com",
        r"4funbox\.co",
        r"www\.4funbox\.com",
        r"mirrobox\.com",
        r"nephobox\.com",
        r"terabox\.app",
        r"terabox\.com",
        r"www\.terabox\.ap",
        r"www\.terabox\.com",
        r"www\.1024tera\.co",
        r"www\.momerybox\.com",
        r"teraboxapp\.com",
        r"momerybox\.com",
        r"tibibox\.com",
        r"www\.tibibox\.com",
        r"www\.teraboxapp\.com",
    ]

    for pattern in patterns:
        if re.search(pattern, url):
            return True

    return False


def get_urls_from_string(string: str) -> list[str]:
    pattern = r"(https?://\S+)"
    urls = re.findall(pattern, string)
    urls = [url for url in urls if check_url_patterns(url)]
    if not urls:
        return []
    return urls[0]


def extract_surl_from_url(url: str) -> str | None:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    surl = query_params.get("surl", [])
    return surl[0] if surl else False


# ---------------- API SETTINGS ---------------- #

NTM_API_TEMPLATE = (
    "https://teradown1.nepcoder.workers.dev/api/resolve?url={url}"
)


# ---------------- RETRY WRAPPER ---------------- #

def retry_request(method, url, attempts=3, delay=2, **kwargs):
    """
    Generic retry wrapper for GET / HEAD requests
    """

    for i in range(1, attempts + 1):
        try:
            resp = requests.request(method, url, timeout=25, **kwargs)

            # Accept 200 and 302 for redirect cases
            if resp.status_code in (200, 302):
                return resp

            print(f"[Retry {i}] HTTP {resp.status_code}")

        except Exception as e:
            print(f"[Retry {i}] Error:", e)

        time.sleep(delay)

    return None


# ---------------- MAIN API HANDLER ---------------- #
def get_data(url: str):
    """
    Fetch TeraBox file data from /api/resolve
    """

    api_url = NTM_API_TEMPLATE.format(url=url)

    print("\nREQUESTING API:", api_url)

    # -------- Retry API Call -------- #

    res = retry_request(
        "GET",
        api_url,
        attempts=3,
        delay=2
    )

    if not res:
        print("API failed after retries")
        return False

    print("API STATUS:", res.status_code)

    # -------- Decode JSON -------- #

    try:
        data = res.json()

    except Exception as e:
        print("JSON parse error:", e)
        return False

    print("API RAW RESPONSE:", data)

    # -------- Validate API -------- #

    if not data.get("ok"):
        print("API returned ok=false")
        return False

    value = data.get("value")

    if not isinstance(value, dict):
        print("Missing value object")
        return False

    files = value.get("files")

    if not isinstance(files, list) or not files:
        print("No files returned")
        return False

    # -------- First File -------- #

    file_data = files[0]

    # -------- Extract Fields -------- #

    filename = file_data.get("name")
    size_bytes = int(file_data.get("size") or 0)
    thumbnail = file_data.get("thumb")

    fast_link = file_data.get("downloadUrl")

    stream_link = file_data.get("streamUrl")

    if not fast_link:
        print("Missing downloadUrl in API response")
        return False

    print("FILE NAME:", filename)
    print("FILE SIZE:", size_bytes)
    print("FAST LINK:", fast_link)

    # -------- Resolve Redirect -------- #

    head = retry_request(
        "HEAD",
        fast_link,
        attempts=3,
        delay=2,
        allow_redirects=True
    )

    if head:
        real_direct_url = head.url
    else:
        print(
            "Redirect resolve failed — "
            "using downloadUrl fallback"
        )

        real_direct_url = fast_link

    print(
        "FINAL CDN URL:",
        real_direct_url
    )

    # -------- Return Structure -------- #

    return {
        "file_name": filename,

        "size": (
            size_bytes
            if size_bytes
            else get_formatted_size(size_bytes)
        ),

        "sizebytes": size_bytes,

        "thumb": thumbnail,

        "direct_link": real_direct_url,

        "link": fast_link,

        "stream_link": stream_link,

        "id": file_data.get("id"),

        "type": file_data.get("type"),

        "expires_at": file_data.get("expiresAt"),
    }
