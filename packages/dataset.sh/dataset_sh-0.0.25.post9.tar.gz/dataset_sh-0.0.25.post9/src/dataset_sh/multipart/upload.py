import json
import os.path
import time

import requests
from tqdm import tqdm

from dataset_sh.multipart.multipart import FilePartsInfo, read_file_range
from dataset_sh.utils.files import checksum


class MultipartUploadClient(object):

    def __init__(self, url, source_file, headers=None, additional_params=None, progress_name=None):
        self.headers = headers
        self.source_file = source_file
        self.checksum = checksum(source_file)
        self.file_length = os.path.getsize(source_file)

        self.params = additional_params if additional_params is not None else {}
        self.params['checksum_value'] = self.checksum
        self.params['file_length'] = self.file_length
        self.url = url

        self.progress_name = progress_name

    def _init(self) -> FilePartsInfo:
        resp = requests.post(self.url, params={
            **self.params,
            'action': 'init'
        }, headers=self.headers)
        resp.raise_for_status()
        info = FilePartsInfo(**json.loads(resp.content.decode('utf-8')))
        return info

    def _upload_part(self, part_id, chunk_size):
        file_data = read_file_range(self.source_file, part_id * chunk_size, chunk_size)
        resp = requests.post(self.url, params={
            **self.params,
            'action': 'upload',
            'part_id': part_id,
        }, headers=self.headers, data=file_data)
        resp.raise_for_status()

    def _done(self):
        resp = requests.post(
            self.url, params={
                **self.params,
                'action': 'done'
            }, headers=self.headers)
        resp.raise_for_status()

    def upload(self):
        info = self._init()
        desc = f"Uploading {self.progress_name}" if self.progress_name else 'Upload Progress'
        for i in tqdm(
                range(info.parts_count), desc=desc, unit="it",
                bar_format="{l_bar}{bar}| {percentage:0.0f}% Completed"):
            if i not in info.finished:
                self._upload_part(i, info.chunk_size)
                time.sleep(2)
        self._done()

    def abort(self):
        resp = requests.post(
            self.url, params={
                **self.params,
                'action': 'abort'
            }, headers=self.headers)
        resp.raise_for_status()


def upload_to_url(upload_url, file_path, headers, params, name):  # pragma: no cover
    client = MultipartUploadClient(
        upload_url, file_path, headers=headers, additional_params=params, progress_name=name
    )
    try:
        client.upload()
    except requests.HTTPError as e:
        client.abort()
