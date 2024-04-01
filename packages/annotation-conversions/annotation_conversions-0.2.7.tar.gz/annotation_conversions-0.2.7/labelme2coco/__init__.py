from __future__ import absolute_import

__version__ = "0.2.7"

import logging
import os
from pathlib import Path

from sahi.utils.file import save_json

from labelme2coco.labelme2coco import get_coco_from_labelme_folder

from typing import List

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
)


def convert(
    labelme_folder: str,
    export_dir: str = "runs/labelme2coco/",
    train_split_rate: float = 1,
    skip_labels: List[str] = [],
    dataset_name: str = 'dataset',
):
    """
    Args:
        labelme_folder: folder that contains labelme annotations and image files
        export_dir: path for coco jsons to be exported
        train_split_rate: ratio for train test split. Defaulting to 1 forms one common file
        skip_labels: labels of shapes to skip and not include in the coco file
        dataset_name: name of the dataset without extension
    """
    coco = get_coco_from_labelme_folder(labelme_folder, skip_labels=skip_labels)
    if train_split_rate < 1:
        result = coco.split_coco_as_train_val(train_split_rate)
        # export train split
        save_path = str(Path(export_dir) / f"{dataset_name}_train.json")
        save_json(result["train_coco"].json, save_path)
        logger.info(f"Training split in COCO format is exported to {save_path}")
        # export val split
        save_path = str(Path(export_dir) / f"{dataset_name}_val.json")
        save_json(result["val_coco"].json, save_path)
        logger.info(f"Validation split in COCO format is exported to {save_path}")
    else:
        save_path = str(Path(export_dir) / f"{dataset_name}.json")
        save_json(coco.json, save_path)
        logger.info(f"Converted annotations in COCO format is exported to {save_path}")
