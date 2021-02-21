from pathlib import Path
import sys



def add_comments() -> None:
  """Add text to every line of every file in directory tree"""
  root = Path(".")
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


def yaml_to_toml_or_json() -> None:
  """ convert yaml file to toml
      dev.py input.yml output.toml

      uncommonent pyYAML and toml-sort in pyproject.toml to use
  """
  import json
  import yaml
  import toml
  from toml_sort.tomlsort import TomlSort
  if len(sys.argv) < 3: raise Exception('Usage is `yml_to_toml.py input.yml output.toml`')


  yml_file = sys.argv[1]
  stem = yml_file.rstrip(".yaml")

  # open the yaml file and convert to json and toml
  with open(yml_file) as source:
      yaml_dict = yaml.load(source.read(), Loader=yaml.FullLoader)
      json_str = json.dumps(yaml_dict, ensure_ascii=False, indent=4)
      json_dict = json.loads(json_str)
      toml_str_unsorted = toml.dumps(json_dict).encode('utf-8').decode('unicode-escape')
      toml_str = TomlSort(toml_str_unsorted).sorted()

  output_file = sys.argv[2]
  if output_file.endswith(".toml"):
    writable = toml_str
  elif output_file.endswith(".json"):
    writable = json_str

  with open(output_file, 'w') as target:
    target.write(writable)
    # new_toml_string = toml.dump(json_dict, target)


