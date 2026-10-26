"""Multimodal Gemini API integration client with demonstration mode and resilient fallbacks."""

import json
import base64
import re
import requests
from io import BytesIO
from typing import Dict, Any, Optional, List, Tuple
from PIL import Image

class GeminiMultimodalClient:
    """Handles multimodal prompts (Image + Text) and text generation using Google Gemini 1.5.
    
    Falls back gracefully to demonstration mode if no API key is provided or if network fails.
    """
    
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        self.api_key = (api_key or "").strip()
        self.model = model or "gemini-1.5-flash"

    @property
    def is_demo_mode(self) -> bool:
        return not bool(self.api_key)

    def _pil_to_base64_jpeg(self, image: Image.Image) -> str:
        """Convert a PIL Image to a base64 encoded JPEG string."""
        buffered = BytesIO()
        rgb_image = image.convert("RGB")
        rgb_image.save(buffered, format="JPEG", quality=85)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def _clean_json_response(self, text: str) -> Dict[str, Any]:
        """Strip markdown codeblocks and parse JSON safely."""
        text = text.strip()
        # Remove ```json and ``` wrapping
        pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(pattern, text)
        if match:
            text = match.group(1).strip()
            
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Attempt to extract first { to last }
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                return json.loads(text[start:end+1])
            raise

    def analyze_image_with_json_contract(
        self,
        image: Image.Image,
        system_prompt: str,
        user_prompt: str,
        demo_fallback_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], bool, str]:
        """Sends an image and prompts to Gemini, requesting structured JSON.
        
        Returns:
            Tuple[data_dict, is_simulated, status_message]
        """
        if self.is_demo_mode:
            return demo_fallback_data, True, "Demo Mode active (no API key supplied). Realistic civil engineering simulation loaded."

        endpoint = f"{self.BASE_URL}/{self.model}:generateContent?key={self.api_key}"
        img_b64 = self._pil_to_base64_jpeg(image)

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"{system_prompt}\n\nTask: {user_prompt}\nRespond ONLY with valid JSON conforming to the requested schema. Do not enclose in explanations."},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": img_b64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "response_mime_type": "application/json"
            }
        }

        try:
            response = requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=45
            )

            if response.status_code == 200:
                result = response.json()
                candidate_text = result["candidates"][0]["content"]["parts"][0]["text"]
                parsed = self._clean_json_response(candidate_text)
                return parsed, False, "Live Gemini 1.5 Multimodal Analysis Complete"
            else:
                error_msg = f"Gemini API Error {response.status_code}: {response.text[:200]}"
                # Fallback on failure
                return demo_fallback_data, True, f"{error_msg} -> Falling back to offline engineering simulation."
        except Exception as e:
            return demo_fallback_data, True, f"Network/Connection error ({str(e)}) -> Demonstration simulation displayed."

    def generate_chat_response(
        self,
        chat_history: List[Dict[str, str]],
        system_instruction: str,
        demo_fallback_text: str
    ) -> Tuple[str, bool]:
        """Generate conversational answer for site assistant."""
        if self.is_demo_mode:
            return demo_fallback_text, True

        endpoint = f"{self.BASE_URL}/{self.model}:generateContent?key={self.api_key}"
        
        # Build contents array
        contents = []
        for msg in chat_history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        payload = {
            "contents": contents,
            "system_instruction": {
                "parts": [{"text": system_instruction}]
            },
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 1000
            }
        }

        try:
            response = requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                return text, False
            else:
                return f"{demo_fallback_text}\n\n*(Note: Live API returned status {response.status_code}. Defaulted to engineering knowledgebase)*", True
        except Exception as e:
            return f"{demo_fallback_text}\n\n*(Note: Live connection unavailable ({str(e)}). Response generated from offline engineering knowledgebase)*", True
