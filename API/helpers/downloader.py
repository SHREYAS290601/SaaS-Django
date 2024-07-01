from pathlib import Path

import requests


def download_to_local(
    url: str = None, out_path: Path = None, parent_mkdir: bool = True
) -> str:
    if not isinstance(out_path, Path):
        raise ValueError(f"This is not a valid path {out_path}")
    if parent_mkdir:
        out_path.parent.mkdir(exist_ok=True, parents=True)

    try:
        response = requests.get(url)
        response.raise_for_status()

        out_path.write_bytes(response.content)
        return out_path
    except requests.RequestException as e:
        raise requests.RequestException(f"Error downloading {url} to {out_path}") from e
