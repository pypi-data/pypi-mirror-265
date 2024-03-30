import logging
from pathlib import Path
import yaml

logger = logging.getLogger()


def load_yaml(fp):
    with open(fp, encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
    return data


def get_module_data(fp, key_name=None):
    if isinstance(fp, str):
        fp = Path(fp)
    data_fp = fp.parent / 'data' / f'{fp.stem}.yml'
    data = load_yaml(fp=data_fp)

    if isinstance(data, dict):
        if key_name is None:
            raise ValueError("The 'key_name' is not set")
        data = data.get(key_name)
    if not isinstance(data, list):
        data = [data]

    return_val = {'argnames': None, 'argvalues': []}
    for item in data:
        if not isinstance(item, dict):
            break
        keys = item.keys()
        if return_val['argnames'] is None:
            return_val['argnames'] = ','.join(keys)
        if len(keys) == 1:
            return_val['argvalues'].extend(list(item.values()))
        else:
            return_val['argvalues'].append([item[k] for k in keys])
    return return_val


def log_step(title):
    logger.info(f'Step: {title}')
    return title
