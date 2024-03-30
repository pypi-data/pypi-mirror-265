import random
from temp_email_automa.main import TempMail, Email
import requests
import re
import time
from typing import Optional, List
import base64


class PixlrApi:
    def __init__(self):
        self.temp_mail = TempMail()
        self.bearer_token: Optional[str] = None

    def register(self) -> bool:
        self.temp_mail.generate_random_email_address()
        email = self.temp_mail.email
        self.email = email
        password = email

        cookies = {
            "country": "ZA",
            "lang": "en-US",
        }

        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://pixlr.com",
            "referer": "https://pixlr.com/",
            "sec-ch-ua": '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }

        json_data = {
            "email": email,
            "password": password,
            "newsletter": random.choice([True, False]),
            "country": "US",
        }

        response = requests.post(
            "https://pixlr.com/auth/register",
            cookies=cookies,
            headers=headers,
            json=json_data,
        )
        # {"status":true,"message":"Registration success; Check your inbox for verification email!"}
        if response.status_code != 200:
            print(f"PixlrApi().register(): Something Went Wrong! {response.text}")
            return False

        response_json = response.json()
        if response_json["status"] is True:
            return True

        print(f"PixlrApi().register(): Something Went Wrong! {response_json}")
        return False

    def verify_email(self) -> bool:
        email: Optional[Email] = None
        max_iter = 50
        for _ in range(max_iter):
            time.sleep(1)
            emails = self.temp_mail.get_list_of_emails()
            if emails:
                email = self.temp_mail.get_single_email(emails[0]["id"])
                break

        if not email:
            print(
                "PixlrApi().verify_email(): No Email Found! TODO: Improve On The error Handeling Here!"
            )
            exit(1)
        code = re.search(r"\d{6}", email.body)
        if not code:
            print(
                "PixlrApi().verify_email(): No 6 Digit Code Found In The Email! TODO: Improve On The error Handeling Here!",
                email,
            )
            exit(1)

        cookies = {
            "country": "ZA",
            "lang": "en-US",
        }

        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://pixlr.com",
            "referer": "https://pixlr.com/",
            "sec-ch-ua": '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }

        json_data = {"email": self.email, "code": code.group()}

        response = requests.post(
            "https://pixlr.com/auth/verify",
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        if response.status_code != 200:
            print(f"PixlrApi().verify_email(): Something Went Wrong! {response.text}")
            return False

        response_json = response.json()
        # {"status":true,"accessToken":"<TOKEN>","refreshToken":"<TOKEN>","message":"Your account has been successfully verified!"}

        if response_json["status"] is True:
            self.bearer_token = response_json["accessToken"]
            return True

        return True

    def generate_image(
        self, width: int, height: int, amount: int, prompt: str
    ) -> List[str]:
        cookies = {
            "country": "ZA",
            "lang": "en-US",
            "__pat": self.bearer_token,
        }

        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://pixlr.com",
            "referer": "https://pixlr.com/image-generator/",
            "sec-ch-ua": '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }

        json_data = {
            "amount": amount,
            "width": width,
            "height": height,
            "prompt": prompt,
            "personal": True,
        }

        response = requests.post(
            "https://pixlr.com/api/openai/generate",
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        if response.status_code != 200:
            print(f"PixlrApi().generate_image(): Something Went Wrong! {response.text}")
            return []

        response_json = response.json()
        image_paths = []
        if response_json["status"] is True:
            for image in response_json["data"]["images"]:
                image_base64 = image["image"]
                image_base64 = image_base64.split(",")[1]
                image_data = base64.b64decode(image_base64)
                image_path = f"/tmp/{image['id']}.png"
                with open(image_path, "wb") as file:
                    file.write(image_data)
                image_paths.append(image_path)

        return image_paths

    def delete_account(self):
        cookies = {
            "country": "ZA",
            "lang": "en-US",
            "__pat": self.bearer_token,
        }

        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "authorization": f"Bearer {self.bearer_token}",
            "content-type": "application/json",
            "origin": "https://pixlr.com",
            "referer": "https://pixlr.com/myaccount/",
            "sec-ch-ua": '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }

        json_data = {
            "reason": f"leavingReasons{random.choice([0,1,2,3])}",
        }

        response = requests.delete(
            "https://pixlr.com/api/myaccount/profile",
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        if response.status_code != 200:
            print(f"PixlrApi().delete_account(): Something Went Wrong! {response.text}")
            return False

        response_json = response.json()
        if response_json["status"] is True:
            return True

        return False
