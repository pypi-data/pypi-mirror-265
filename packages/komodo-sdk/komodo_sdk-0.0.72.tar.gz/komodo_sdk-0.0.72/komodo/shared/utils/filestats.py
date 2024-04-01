from datetime import datetime
from pathlib import Path

import magic

from komodo.proto.generated.collection_pb2 import File
from komodo.shared.utils.digest import get_file_digest_full, get_guid_short


def file_details(filepath):
    path = Path(filepath)
    file = File(guid=get_guid_short(), path=str(path))
    stat = path.stat()
    file.name = path.stem
    file.size = stat.st_size
    file.magic = magic.from_file(filepath, mime=True)
    file.checksum = get_file_digest_full(filepath)
    file.created_at = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    file.modified_at = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    return file
