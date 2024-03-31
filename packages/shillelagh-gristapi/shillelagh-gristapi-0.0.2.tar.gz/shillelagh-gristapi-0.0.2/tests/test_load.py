from collections import defaultdict
from typing import cast
from importlib.metadata import entry_points


loaders = defaultdict(list)

for entry_point in entry_points(group="shillelagh.adapter"):
  loaders[entry_point.name].append(entry_point.load)

print(loaders)

print(loaders.keys())

for load in loaders["gristapi"]:
  load()
