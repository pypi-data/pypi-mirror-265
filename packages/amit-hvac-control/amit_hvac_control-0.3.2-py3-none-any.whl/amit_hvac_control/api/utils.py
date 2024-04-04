from aiohttp import MultipartWriter


def get_multipart_data(post: dict):
    with MultipartWriter("form-data") as mp:
        for key, value in post.items():
            part = mp.append(str(value))

            del part._headers["Content-Type"]
            del part._headers["Content-Length"]
            part.set_content_disposition("form-data", name=key)
        return mp
