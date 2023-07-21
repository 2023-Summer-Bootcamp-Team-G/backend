import os
import re
import time
import random
import requests

from enum import Enum

BING_URL = "https://www.bing.com"

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "referrer": f"{BING_URL}/images/create/",
    "origin": BING_URL,
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
    "x-forwarded-for": f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
}


class Error(Enum):
    ERROR_TIMEOUT = "Your request has timed out."
    ERROR_BLOCKED_PROMPT = "Your prompt has been blocked by Bing. Try to change any bad words and try again."
    ERROR_BEING_REVIEWED_PROMPT = "Your prompt is being reviewed by Bing. Try to change any sensitive words and try again."
    ERROR_NO_RESULTS = "Could not get results"
    ERROR_UNSUPPORTED_LANG = "This language is currently not supported by Bing"
    ERROR_NO_IMAGES = "No images"


class ImageGenAPI:
    def __init__(
        self,
        auth_cookie: str,
    ):
        self.session: requests.Session = requests.Session()
        self.session.headers = HEADERS
        self.session.cookies.set("_U", auth_cookie)

    def get_images(self, prompt: str):
        url_encoded_prompt = requests.utils.quote(prompt)
        payload = f"q={url_encoded_prompt}&qs=ds"

        url = f"{BING_URL}/images/create?q={url_encoded_prompt}&rt=4&FORM=GENCRE"
        response = self.session.post(
            url,
            allow_redirects=False,
            data=payload,
            timeout=200,
        )

        res_message = response.text.lower()

        if "this prompt is being reviewed" in res_message:
            raise Exception(Error.ERROR_BEING_REVIEWED_PROMPT.value)
        if "this prompt has been blocked" in res_message:
            raise Exception(Error.ERROR_BLOCKED_PROMPT.value)

        if response.status_code != 302:
            # error?
            pass

        # Get redirect URL
        redirect_url = response.headers["Location"].replace("&nfy=1", "")
        request_id = redirect_url.split("id=")[-1]
        self.session.get(f"{BING_URL}{redirect_url}")
        polling_url = f"{BING_URL}/images/create/async/results/{request_id}?q={url_encoded_prompt}"

        start_wait = time.time()

        while True:
            if int(time.time() - start_wait) > 200:
                raise Exception(Error.ERROR_TIMEOUT.value)

            response = self.session.get(polling_url)

            if response.status_code != 200:
                raise Exception(Error.ERROR_NO_RESULTS.value)

            if not response.text or "errorMessage" in response.text:  # 무한 루프?
                time.sleep(1)
            else:
                break

        image_links = re.findall(r'src="([^"]+)"', response.text)

        if len(image_links) == 0:
            raise Exception(Error.ERROR_NO_IMAGES.value)

        normal_image_links = [link.split("?w=")[0] for link in image_links]

        return normal_image_links


if __name__ == "__main__":
    prompt = "a 4d shaped hamburger, digital art"
    # prompt = "여우 분홍색 지브리 개 기타 도서관"

    image_generator = ImageGenAPI(
        os.getenv("BING_SESSION_ID")
    )  # .env 에 추가, BING_SESSION_ID=ID

    iL = image_generator.get_images(prompt)

    print(iL)

    # (response.content) 추후 저장

    # 웹 쿠키 얻기 cookieStore.get("_U").then(result => console.log(result.value))
