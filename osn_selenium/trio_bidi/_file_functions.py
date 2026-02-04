import os
import base64
import zipfile
import tempfile
from io import BytesIO


__all__ = ["unzip_file"]


def unzip_file(base64_zip: str) -> str:
	"""
	Decodes a base64 encoded zip file and extracts its first content to a temporary directory.

	Args:
		base64_zip (str): The base64 encoded string of the zip file.

	Returns:
		str: The path to the extracted file.
	"""
	
	zip_data = base64.b64decode(base64_zip)
	
	with zipfile.ZipFile(BytesIO(zip_data)) as zipped_file:
		temp_dir = tempfile.mkdtemp()
		zipped_file.extractall(temp_dir)
	
		return os.path.join(temp_dir, zipped_file.namelist()[0])
