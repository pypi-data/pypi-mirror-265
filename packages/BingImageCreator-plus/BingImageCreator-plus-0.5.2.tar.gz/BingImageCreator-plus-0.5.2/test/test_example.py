import json
import os

from src.BingImageCreator import ImageGen


def test_get_images():
    with open(
        os.path.join(os.path.expanduser("~"), ".config", "bing-cookies.json"), "r"
    ) as f:
        cookies = json.loads(f.read())
        u = [x.get("value") for x in cookies if x.get("name") == "_U"][0]
        srch = srch = [
            x.get("value")
            for x in cookies
            if x.get("name") == "SRCHHPGUSR" and x.get("path") == "/images"
        ][0]
        print(srch)
        gen = ImageGen(auth_cookie=u, auth_cookie_SRCHHPGUSR=srch)
        list_img = gen.get_images("roasted coffee beans in palms")
        assert list_img
        print(list_img)
