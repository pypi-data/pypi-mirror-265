import base64
import mimetypes


def encode_file(file_path: str):
    with open(file_path, "rb") as file:
        file_data = file.read()
        mime_type, _ = mimetypes.guess_type(file_path)
        base64_data = base64.b64encode(file_data).decode("ascii")
        data_url = f"data:{mime_type};base64,{base64_data}"
        return data_url


def decode_dataurl(data_url: str):
    header, encoded = data_url.split(",", 1)
    mime_type = header.split(":")[1].split(";")[0]
    extension = mimetypes.guess_extension(mime_type)
    file_data = base64.b64decode(encoded)
    return extension, file_data
