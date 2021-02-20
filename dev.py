from pathlib import Path

root = Path(".")

"""
for path_object in root.glob('**/*'):
    if path_object.is_file() and str(path_object).endswith(".py") and not str(path_object).startswith("dev"):
        with open(path_object, "r") as fp:
          lines = fp.read().splitlines()
        with open(path_object, "w") as fp:
          for line in lines:
              if line in ['\n', '\r\n']:
                print(line, file=fp)
              else:
                print(line + "  # (c)2018", file=fp)
        print(f"{path_object} modified")
"""