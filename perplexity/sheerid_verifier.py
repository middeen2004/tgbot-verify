"""Perplexity Pro student verification flow (SheerID)."""
import logging
import random
import re
import time
from typing import Dict, Optional, Tuple

import httpx
from PIL import Image, ImageDraw, ImageFont

SHEERID_BASE_URL = "https://services.sheerid.com/rest/v2"
DEFAULT_ORG = {
    "id": 291085,
    "idExtended": "291085",
    "name": "University of Groningen",
    "domain": "rug.nl",
}

FIRST_NAMES = [
    "James",
    "John",
    "Robert",
    "Michael",
    "William",
    "David",
    "Richard",
    "Joseph",
    "Thomas",
    "Christopher",
    "Charles",
    "Daniel",
    "Matthew",
    "Anthony",
    "Mark",
    "Donald",
    "Steven",
    "Andrew",
    "Paul",
    "Joshua",
    "Kenneth",
    "Kevin",
    "Brian",
    "George",
    "Timothy",
    "Ronald",
    "Edward",
    "Jason",
    "Jeffrey",
    "Ryan",
    "Mary",
    "Patricia",
    "Jennifer",
    "Linda",
    "Barbara",
    "Elizabeth",
    "Susan",
    "Jessica",
    "Sarah",
    "Karen",
    "Lisa",
    "Nancy",
    "Betty",
    "Margaret",
    "Sandra",
    "Ashley",
    "Kimberly",
    "Emily",
    "Donna",
    "Michelle",
    "Dorothy",
    "Carol",
    "Amanda",
    "Melissa",
    "Deborah",
    "Stephanie",
    "Rebecca",
    "Sharon",
    "Laura",
    "Emma",
    "Olivia",
    "Ava",
    "Isabella",
    "Sophia",
    "Mia",
    "Charlotte",
    "Amelia",
]
LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Perez",
    "Thompson",
    "White",
    "Harris",
    "Sanchez",
    "Clark",
    "Ramirez",
    "Lewis",
    "Robinson",
    "Walker",
    "Young",
    "Allen",
    "King",
    "Wright",
    "Scott",
    "Torres",
    "Nguyen",
    "Hill",
    "Flores",
    "Green",
    "Adams",
    "Nelson",
    "Baker",
    "Hall",
    "Rivera",
    "Campbell",
    "Mitchell",
    "Carter",
    "Roberts",
    "Turner",
    "Phillips",
    "Evans",
    "Parker",
    "Edwards",
]

logger = logging.getLogger(__name__)


def _random_delay():
    time.sleep(random.uniform(0.25, 0.65))


def _generate_device_fingerprint() -> str:
    chars = "0123456789abcdef"
    return "".join(random.choice(chars) for _ in range(32))


def _generate_name() -> Tuple[str, str]:
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def _generate_birth_date() -> str:
    year = random.randint(2000, 2006)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


def _generate_email(first: str, last: str, domain: str) -> str:
    patterns = [
        f"{first[0].lower()}{last.lower()}{random.randint(100, 999)}",
        f"{first.lower()}.{last.lower()}{random.randint(10, 99)}",
        f"{last.lower()}{first[0].lower()}{random.randint(100, 999)}",
    ]
    return f"{random.choice(patterns)}@{domain.lower()}"


def _generate_invoice(first: str, last: str, dob: str, school: str) -> bytes:
    """Create a simple A4 invoice-style PNG using Pillow only."""
    width, height = 595, 842
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 18)
        font_text = ImageFont.truetype("arial.ttf", 12)
        font_small = ImageFont.truetype("arial.ttf", 10)
        font_bold = ImageFont.truetype("arialbd.ttf", 12)
    except Exception:
        font_title = font_text = font_small = font_bold = ImageFont.load_default()

    draw.rectangle([(20, 20), (width - 20, 120)], outline=(200, 0, 0), width=2)
    draw.text((32, 32), "UNIVERSITY OF GRONINGEN", fill=(200, 0, 0), font=font_title)
    draw.text((32, 60), "Student Fee Invoice", fill=(0, 0, 0), font=font_bold)
    draw.text((32, 80), "student information and administration", fill=(90, 90, 90), font=font_small)

    draw.text((32, 150), "Bill to:", fill=(0, 0, 0), font=font_bold)
    draw.text((32, 170), f"{first} {last}", fill=(0, 0, 0), font=font_text)
    draw.text((32, 190), f"Date of birth: {dob}", fill=(0, 0, 0), font=font_text)
    draw.text((32, 210), f"Program: {school}", fill=(0, 0, 0), font=font_text)

    y = 260
    draw.text((32, y), "Description", fill=(0, 0, 0), font=font_bold)
    draw.text((400, y), "Amount", fill=(0, 0, 0), font=font_bold)
    y += 24
    draw.text((32, y), "Tuition fees 2025/2026", fill=(0, 0, 0), font=font_text)
    draw.text((400, y), f"€{random.randint(10, 12)},{random.randint(100, 999)}.00", fill=(0, 0, 0), font=font_text)

    y += 40
    draw.line([(32, y), (width - 32, y)], fill=(0, 0, 0), width=1)
    y += 20
    draw.text((32, y), "Make sure to transfer the tuition fees before the starting date of the programme.", fill=(200, 0, 0), font=font_small)

    buffer = Image.new("RGB", img.size, (255, 255, 255))
    buffer.paste(img, (0, 0))
    output = Image.new("RGB", img.size, (255, 255, 255))
    output.paste(buffer, (0, 0))
    byte_stream = output.tobytes()

    buf = Image.new("RGB", img.size)
    buf.paste(output)
    from io import BytesIO

    out = BytesIO()
    buf.save(out, format="PNG")
    return out.getvalue()


class SheerIDVerifier:
    """Perplexity Pro student verifier."""

    def __init__(self, url: str):
        self.url = url
        self.verification_id = self.parse_verification_id(url)
        self.program_id = self.parse_program_id(url)
        self.device_fingerprint = _generate_device_fingerprint()
        self.client = httpx.Client(timeout=30.0)
        self.organization = None

    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()

    @staticmethod
    def parse_verification_id(url: str) -> Optional[str]:
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        match = re.search(r"/verification/([a-f0-9]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def parse_program_id(url: str) -> Optional[str]:
        match = re.search(r"/verify/([a-f0-9]+)/", url, re.IGNORECASE)
        return match.group(1) if match else None

    def _request(self, method: str, endpoint: str, body: Optional[Dict] = None) -> Tuple[Dict, int]:
        _random_delay()
        headers = {"Content-Type": "application/json"}
        resp = self.client.request(method, f"{SHEERID_BASE_URL}{endpoint}", json=body, headers=headers)
        try:
            data = resp.json()
        except Exception:
            data = resp.text
        return data, resp.status_code

    def _upload_s3(self, upload_url: str, payload: bytes) -> bool:
        try:
            resp = self.client.put(upload_url, content=payload, headers={"Content-Type": "image/png"}, timeout=60.0)
            return 200 <= resp.status_code < 300
        except Exception as exc:
            logger.error("S3 upload failed: %s", exc)
            return False

    def _search_organization(self) -> Optional[Dict]:
        if not self.program_id:
            return None
        for term in ["Rijksuniversiteit Groningen", "University of Groningen", "Groningen"]:
            try:
                data, status = self._request(
                    "GET",
                    f"/organization?searchTerm={term}&programId={self.program_id}",
                )
                if status == 200 and isinstance(data, list) and data:
                    org = data[0]
                    org.setdefault("idExtended", str(org.get("id")))
                    org.setdefault("domain", "rug.nl")
                    return org
            except Exception as exc:
                logger.warning("Organization search failed for term %s: %s", term, exc)
        return None

    def verify(self) -> Dict:
        if not self.verification_id:
            return {"success": False, "message": "Invalid SheerID link"}

        try:
            # Check link status
            info, status = self._request("GET", f"/verification/{self.verification_id}")
            if status != 200:
                return {"success": False, "message": f"Verification lookup failed (HTTP {status})"}

            current_step = info.get("currentStep", "") if isinstance(info, dict) else ""
            if current_step in {"success", "pending"}:
                return {"success": False, "message": f"Link already {current_step}"}

            # Organization selection
            self.organization = self._search_organization() or DEFAULT_ORG

            # Identity generation
            first, last = _generate_name()
            email = _generate_email(first, last, self.organization.get("domain", "rug.nl"))
            dob = _generate_birth_date()
            document = _generate_invoice(first, last, dob, self.organization["name"])

            # Step: collect personal info (if needed)
            if current_step == "collectStudentPersonalInfo":
                payload = {
                    "firstName": first,
                    "lastName": last,
                    "birthDate": dob,
                    "email": email,
                    "phoneNumber": "",
                    "organization": {
                        "id": int(self.organization["id"]),
                        "idExtended": self.organization["idExtended"],
                        "name": self.organization["name"],
                    },
                    "deviceFingerprintHash": self.device_fingerprint,
                    "locale": "en-US",
                    "metadata": {
                        "marketConsentValue": False,
                        "verificationId": self.verification_id,
                    },
                }
                data, status = self._request(
                    "POST",
                    f"/verification/{self.verification_id}/step/collectStudentPersonalInfo",
                    payload,
                )
                if status != 200:
                    return {"success": False, "message": f"Step collect info failed ({status})"}
                if isinstance(data, dict) and data.get("currentStep") == "error":
                    return {"success": False, "message": ", ".join(data.get("errorIds", [])) or "collect info error"}
                current_step = data.get("currentStep", current_step)

            # Step: skip SSO if required
            if current_step in {"sso", "collectStudentPersonalInfo"}:
                self._request("DELETE", f"/verification/{self.verification_id}/step/sso")

            # Step: doc upload
            upload_body = {
                "files": [
                    {"fileName": "student_card.png", "mimeType": "image/png", "fileSize": len(document)}
                ]
            }
            data, status = self._request(
                "POST",
                f"/verification/{self.verification_id}/step/docUpload",
                upload_body,
            )
            if status != 200 or not isinstance(data, dict) or not data.get("documents"):
                return {"success": False, "message": "Failed to obtain upload URL"}

            upload_url = data["documents"][0].get("uploadUrl")
            if not upload_url:
                return {"success": False, "message": "Upload URL missing"}

            if not self._upload_s3(upload_url, document):
                return {"success": False, "message": "Uploading document failed"}

            final_data, _ = self._request(
                "POST",
                f"/verification/{self.verification_id}/step/completeDocUpload",
            )

            return {
                "success": True,
                "pending": True,
                "message": "Documents submitted, awaiting review",
                "verification_id": self.verification_id,
                "redirect_url": final_data.get("redirectUrl") if isinstance(final_data, dict) else None,
            }

        except Exception as exc:
            logger.error("Perplexity verification failed: %s", exc)
            return {"success": False, "message": str(exc)}
