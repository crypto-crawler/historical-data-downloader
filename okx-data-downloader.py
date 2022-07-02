import logging
import os
import sys
import time
import zipfile
from typing import List

import requests

logging.basicConfig(level=logging.INFO)


def validate_zip_file(zip_file: str) -> bool:
    """Validate zip file."""
    the_zip_file = zipfile.ZipFile(zip_file)
    ret = the_zip_file.testzip()
    return ret is None


def download(url: str, output_file: str) -> bool:
    """Download a zip file, skip if it exists."""
    assert output_file.endswith(".zip")
    if os.path.exists(output_file) and validate_zip_file(output_file):
        logging.info(f"Skipped {url}")
        return True
    logging.info(f"Downloading {url}")
    resp = requests.get(url, stream=True)
    with open(output_file, "wb") as f_out:
        for chunk in resp.iter_content(chunk_size=4096):
            if chunk:  # filter out keep-alive new chunks
                f_out.write(chunk)
    return True


def list_files(msg_type: str, month: int) -> List[str]:
    """List files in a month."""
    url = f"https://www.okx.com/priapi/v5/broker/public/orderRecord?t={int(time.time()*1000)}&path=cdn/okex/traderecords/{msg_type}/monthly/{month}"
    obj = requests.get(url).json()
    if obj["code"] != "0":
        raise ValueError(obj)
    return [x["fileName"] for x in obj["data"]]


def okx_download(msg_type: str, month: str, output_dir: str) -> bool:
    """Download OKX data.

    Args:
        msg_type: allspot, allswap, allfuture
    """
    files = list_files(msg_type, int(month.replace("-", "")))
    for file in files:
        url = f"https://static.okx.com/cdn/okex/traderecords/{msg_type}/monthly/{month.replace('-', '')}/{file}"
        output_file = os.path.join(output_dir, os.path.basename(url))
        if not download(url, output_file):
            return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: okx-data-downloader.py <yyyy-MM> <output_dir>")
        sys.exit(1)

    month = sys.argv[1]
    output_dir = os.path.join(sys.argv[2])
    msg_types = ["trades", "swaprate"]

    for msg_type in msg_types:
        msg_type_dir = os.path.join(output_dir, msg_type, month.replace("-", ""))
        os.makedirs(msg_type_dir, exist_ok=True)
        okx_download(msg_type, month, msg_type_dir)
