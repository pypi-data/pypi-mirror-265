from datetime import datetime
from pathlib import Path

import magic

from komodo.proto.generated.collection_pb2 import File
from komodo.shared.utils.digest import get_file_digest_full, GUID_LEN


def file_details(filepath):
    path = Path(filepath)
    checksum = get_file_digest_full(filepath)
    
    file = File(guid=checksum[:GUID_LEN], path=str(path))
    stat = path.stat()
    file.name = path.stem
    file.size = stat.st_size
    file.magic = magic.from_file(filepath, mime=True)
    file.checksum = checksum
    file.created_at = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    file.modified_at = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    return file
