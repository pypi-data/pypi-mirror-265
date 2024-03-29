import json
import os
from pathlib import Path

from komodo.framework.komodo_tool import KomodoTool
from komodo.shared.utils.digest import get_shortcode_with_path
from komodo.shared.utils.filestats import file_details


class DirectoryReader(KomodoTool):
    name = "Directory Reader"
    purpose = "Lists directory contents recursively"
    shortcode = "komodo_directory_reader"

    def definition(self, shortcode):
        return {
            "type": "function",
            "function": {
                "name": shortcode,
                "description": self.purpose,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Pattern of files to match. Defaults to all files if not provided."
                        },
                    }
                }
            }
        }

    def __init__(self, path: Path):
        shortcode = get_shortcode_with_path(self.shortcode, path)
        super().__init__(shortcode=shortcode,
                         name=self.name,
                         definition=self.definition(shortcode),
                         action=self.action)
        self.path = path

    def action(self, args):
        try:
            pattern = args.get("pattern", "*")
            files = self.get_files_recursively_pathlib(self.path, pattern)
            result = []

            for file in files:
                if os.path.isfile(file):
                    details = file_details(str(file))
                    file_info = {
                        "path": str(file.relative_to(self.path)),
                        "basename": details.name,
                        "type": details.magic,
                        "checksum": details.checksum,
                        "created_at": details.created_at,
                        "updated_at": details.modified_at
                    }
                    result.append(file_info)

            # print(result)
            return json.dumps(result, default=str)

        except Exception as e:
            print("Failed to list files: ", e)
            return "Failed to list files: " + str(args.get("pattern", ""))

    def get_files_recursively_pathlib(self, datadir, pattern='*'):
        return Path(datadir).rglob(pattern)


if __name__ == "__main__":
    from komodo.config import PlatformConfig
    from komodo.framework.komodo_tool_registry import KomodoToolRegistry

    d = PlatformConfig().komodo_hello_path
    t = DirectoryReader(d)
    print(t.definition)
    print(t.action({"pattern": "*.txt"}))

    reader = DirectoryReader(d)
    KomodoToolRegistry.register(reader)

    s = reader.shortcode
    print(s)
    print(KomodoToolRegistry.get_definitions([s]))

    y = KomodoToolRegistry.get_tool_by_shortcode(s)
    print(y.definition)
    print(y.action({"pattern": "*.txt"}))
