# core/auth.py

from pathlib import Path
from typing import Optional
import json


class TwitchAuthManager:
    """
    Handles Twitch authentication, cookies and token refresh.
    Stores cookies in cookies.jar similar to TwitchDropsMiner.
    """

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.cookies_file = data_dir / "cookies.jar"
        self.token_file = data_dir / "token.json"

    def load_session(self) -> bool:
        """
        Load existing session from token/cookies if it exists.
        Returns True if session loaded, False otherwise.
        """
        try:
            if self.token_file.exists():
                with open(self.token_file) as f:
                    self.token_data = json.load(f)
                return True
        except Exception:
            pass
        return False

    def login_with_browser_flow(self) -> None:
        """
        Start login flow (manual browser + paste token).
        For now, this is a placeholder.
        """
        raise NotImplementedError("OAuth flow not yet implemented")

    def get_auth_headers(self) -> dict:
        """
        Return HTTP headers for authenticated Twitch requests.
        """
        if not hasattr(self, 'token_data'):
            return {}
        return {
            "Authorization": f"Bearer {self.token_data.get('access_token', '')}"
        }

    def save_token(self, token_data: dict) -> None:
        """Save token to file."""
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)
        self.token_data = token_data
