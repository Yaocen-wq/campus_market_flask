import os
import yaml
import config

def load_yaml(rel_path):
    path = os.path.join(config.DATA_DIR, rel_path)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)
