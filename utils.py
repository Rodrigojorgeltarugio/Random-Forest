import numpy as np
import pandas as pd
import json
import os
from zipfile import ZipFile
from io import BytesIO
from scipy import stats


def load_file_as_array(path):
    """Load a file and return an (n,3) numpy array when possible.
    Supports CSV (columns x,y,z or first 3 columns), JSON arrays, NPY, XLSX, and ZIP (will return None for ZIP -- caller should unzip)."""
    lower = path.lower()
    try:
        if lower.endswith('.npy'):
            arr = np.load(path)
            return arr
        if lower.endswith('.csv'):
            df = pd.read_csv(path)
            # If columns named x,y,z exist use them, else use first three numeric columns
            cols = None
            for c in ['x', 'y', 'z']:
                if c in df.columns:
                    cols = ['x', 'y', 'z']
                    break
            if cols is None:
                # pick first three numeric cols
                numcols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(numcols) >= 3:
                    cols = numcols[:3]
                else:
                    # maybe data is rows of arrays
                    values = df.values
                    if values.shape[1] >= 3:
                        return values[:, :3]
            return df[cols].values
        if lower.endswith('.json'):
            with open(path, 'r', encoding='utf-8') as f:
                j = json.load(f)
            arr = np.array(j)
            return arr
        if lower.endswith('.xlsx') or lower.endswith('.xls'):
            df = pd.read_excel(path)
            numcols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numcols) >= 3:
                return df[numcols[:3]].values
        if lower.endswith('.zip'):
            # Caller should explicitly expand archives using expand_archive()
            return None
    except Exception:
        return None
    return None


def expand_archive(path, dest_dir=None):
    """Extract a zip archive into a directory and return a list of extracted file paths.
    If dest_dir is None, extract into a folder next to the archive named <archive>_extracted."""
    if dest_dir is None:
        base = os.path.splitext(path)[0]
        dest_dir = f"{base}_extracted"
    os.makedirs(dest_dir, exist_ok=True)
    extracted = []
    try:
        with ZipFile(path, 'r') as z:
            z.extractall(dest_dir)
            for name in z.namelist():
                abs_path = os.path.join(dest_dir, name)
                if os.path.isfile(abs_path):
                    extracted.append(abs_path)
    except Exception:
        return []
    return extracted


def list_supported_files(paths):
    """Given an iterable of file paths, return only those with supported extensions."""
    supported = {'.csv', '.json', '.npy', '.xlsx', '.xls'}
    out = []
    for p in paths:
        _, ext = os.path.splitext(p.lower())
        if ext in supported:
            out.append(p)
    return out


def extract_features_from_array(arr):
    """Given an array-like of shape (n, m) or (n,) return a dict of features.
    If n x 3, compute aggregated features per axis and flatten."""
    a = np.asarray(arr)
    if a.ndim == 1:
        a = a.reshape(-1, 1)
    ncols = a.shape[1]
    features = {}
    for i in range(ncols):
        col = a[:, i]
        prefix = f'a{i}'
        features[f'{prefix}_mean'] = float(np.nanmean(col))
        features[f'{prefix}_std'] = float(np.nanstd(col))
        features[f'{prefix}_min'] = float(np.nanmin(col))
        features[f'{prefix}_max'] = float(np.nanmax(col))
        features[f'{prefix}_median'] = float(np.nanmedian(col))
        features[f'{prefix}_iqr'] = float(np.subtract(*np.percentile(col, [75, 25])))
        features[f'{prefix}_rms'] = float(np.sqrt(np.nanmean(col ** 2)))
        features[f'{prefix}_skew'] = float(stats.skew(col, nan_policy='omit'))
        features[f'{prefix}_kurtosis'] = float(stats.kurtosis(col, nan_policy='omit'))
        # energy
        features[f'{prefix}_energy'] = float(np.nansum(col ** 2))
        # simple spectral feature: dominant frequency magnitude via FFT
        try:
            fft = np.fft.rfft(col - np.nanmean(col))
            mags = np.abs(fft)
            dom = np.argmax(mags)
            features[f'{prefix}_dom_freq'] = float(dom)
        except Exception:
            features[f'{prefix}_dom_freq'] = 0.0
    return features
