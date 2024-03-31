def encode_file(file_path: str) -> str:
    """
    Encodes the contents of a file as a base64 data URL.

    Args:
        file_path (str): The path to the file to be encoded.

    Returns:
        str: The base64 data URL representing the file contents.
    """
    ...

def decode_dataurl(data_url: str) -> tuple[str | None, bytes]:
    """
    Decodes a base64 data URL into the file extension and file data.

    Args:
        data_url (str): The base64 data URL to be decoded.

    Returns:
        tuple[str | None, bytes]: A tuple containing the file extension (or None if not found) and the decoded file data.
    """
    ...
