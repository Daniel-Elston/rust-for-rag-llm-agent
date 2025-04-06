from __future__ import annotations

import json
import msgpack

import logging
from pathlib import Path
from typing import Dict, List
import joblib
import numpy as np
import pandas as pd
import pickle


class FileAccess:
    """Automatic file loading and saving."""
    @staticmethod
    def extract_suffix(path: Path):
        return path.suffix

    @staticmethod
    def load_file(path: Path):
        path = Path(path)
        suffix = path.suffix
        logging.getLogger("file_access").file_track(f"Loading Input File: ``{path}``")
        if suffix == ".parquet":
            return pd.read_parquet(path)
        elif suffix == ".csv":
            return pd.read_csv(path)
        elif suffix == ".xlsx":
            return pd.read_excel(path)
        elif suffix == ".npy":
            return np.load(path)
        elif suffix == ".joblib":
            return joblib.load(path)
        elif suffix == ".json":
            return pd.read_json(path, orient="index")
        elif suffix == ".pkl":
            return pickle.load(open(path, "rb"))
        elif suffix == ".msgpack": # Add support for .msgpack extension
            return FileAccess.load_msgpack(path)
        elif suffix == ".pdf":
            pass
        else:
            raise ValueError(f"Unknown file type: {suffix}")

    @staticmethod
    def save_file(df: pd.DataFrame, path: Path, index=False):
        suffix = path.suffix
        logging.getLogger("file_access").file_track(f"Saving Output File: ``{path}``")
        if suffix == ".parquet":
            return df.to_parquet(path, index=index)
        elif suffix == ".csv":
            return df.to_csv(path, index=index)
        elif suffix == ".xlsx":
            return df.to_excel(path, index=index)
        elif suffix == ".npy":
            return np.save(path, df)
        elif suffix == ".joblib":
            return joblib.dump(df, path)
        elif suffix == ".json":
            if isinstance(df, pd.DataFrame):
                return df.to_json(path, orient="records", indent=4)
            elif isinstance(df, List):
                return FileAccess.save_json(df, path)
        elif suffix == ".pkl":
            return pickle.dump(df, open(path, "wb"))
        elif suffix == ".txt":
            with open(path, "a", encoding="utf-8") as f:
                f.write(df)
        elif suffix == ".msgpack":  # Add support for .msgpack extension
            if isinstance(df, List):
                return FileAccess.save_msgpack(df, path)
            else:
                raise TypeError(f"Unsupported data type for MessagePack: {type(df)}")
        else:
            raise ValueError(f"Unknown file type: {path} {suffix}")

    @staticmethod
    def load_json(path):
        with open(path, "r") as file:
            return json.load(file)

    @staticmethod
    def save_json(data, path, overwrite=False):
        if overwrite is False and Path(path).exists():
            pass
        else:
            with open(path, "w") as file:
                json.dump(data, file)

    @staticmethod
    def save_msgpack(data: List[dict], path: Path, overwrite=False):
        """Saves data to a MessagePack file."""
        if overwrite is False and Path(path).exists():
            pass
        else:
            with open(path, "wb") as file:
                packed_data = msgpack.pack(data)
                file.write(packed_data)

    @staticmethod
    def load_msgpack(path: Path):
        """Loads data from a MessagePack file."""
        with open(path, "rb") as file:
            unpacked_data = msgpack.unpackb(file.read(), raw=False)
            return unpacked_data