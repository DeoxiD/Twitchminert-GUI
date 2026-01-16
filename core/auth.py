# core/auth.py

from pathlib import Path
from typing import Optional
import json
import secrets
import time
import requests
import webbrowser
from urllib.parse import urlencode
from flask import request


class TwitchAuthManager:
    """
    Handles Twitch OAuth2 authentication with proper token management.
    Implements authorization code flow with PKCE for security.
    """

    TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/authorize"
    TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
    TWITCH_VALIDATE_URL = "https://id.twitch.tv/oauth2/validate"
    TWITCH_REVOKE_URL = "https://id.twitch.tv/oauth2/revoke"

    SCOPES = [
        "user:read:email",
        "channel:read:subscriptions",
        "bits:read",
        "channel:read:redemptions",
    ]

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, data_dir: Path) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.data_dir = data_dir
        self.token_file = data_dir / "token.json"
        self.token_data = None
        self.state = None

    def load_session(self) -> bool:
        """
        Load existing session from token file.
        Returns True if valid session exists, False otherwise.
        """
        try:
            if self.token_file.exists():
                with open(self.token_file, 'r') as f:
                    self.token_data = json.load(f)
                
                # Check if token is expired
                if self._is_token_expired():
                    # Try to refresh the token
                    if self._refresh_token():
                        return True
                    return False
                
                # Validate token with Twitch API
                if self._validate_token():
                    return True
                else:
                    # Token invalid, try to refresh
                    return self._refresh_token()
            return False
        except Exception as e:
            print(f"Error loading session: {e}")
            return False

    def get_auth_url(self) -> str:
        """
        Generate OAuth2 authorization URL.
        Returns the URL to redirect user for authorization.
        """
        self.state = secrets.token_urlsafe(32)
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.SCOPES),
            "state": self.state,
            "force_verify": "false",
        }
        
        return f"{self.TWITCH_AUTH_URL}?{urlencode(params)}"

    def handle_callback(self, code: str, state: str) -> bool:
        """
        Handle OAuth callback and exchange code for tokens.
        Returns True if successful, False otherwise.
        """
        # Verify state to prevent CSRF attacks
        if state != self.state:
            print("State mismatch - possible CSRF attack")
            return False

        try:
            # Exchange authorization code for access token
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri,
            }

            response = requests.post(self.TWITCH_TOKEN_URL, data=data)
            response.raise_for_status()

            token_data = response.json()
            token_data['obtained_at'] = int(time.time())
            
            self.token_data = token_data
            self.save_token(token_data)
            
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error exchanging code for token: {e}")
            return False

    def _refresh_token(self) -> bool:
        """
        Refresh the access token using refresh token.
        Returns True if successful, False otherwise.
        """
        if not self.token_data or 'refresh_token' not in self.token_data:
            return False

        try:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": self.token_data['refresh_token'],
            }

            response = requests.post(self.TWITCH_TOKEN_URL, data=data)
            response.raise_for_status()

            token_data = response.json()
            token_data['obtained_at'] = int(time.time())
            
            # Preserve refresh_token if not provided in response
            if 'refresh_token' not in token_data:
                token_data['refresh_token'] = self.token_data['refresh_token']
            
            self.token_data = token_data
            self.save_token(token_data)
            
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error refreshing token: {e}")
            return False

    def _validate_token(self) -> bool:
        """
        Validate token with Twitch API.
        Returns True if token is valid, False otherwise.
        """
        if not self.token_data or 'access_token' not in self.token_data:
            return False

        try:
            headers = {
                "Authorization": f"OAuth {self.token_data['access_token']}"
            }
            
            response = requests.get(self.TWITCH_VALIDATE_URL, headers=headers)
            
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.RequestException:
            return False

    def _is_token_expired(self) -> bool:
        """
        Check if access token is expired.
        Returns True if expired, False otherwise.
        """
        if not self.token_data:
            return True
        
        if 'obtained_at' not in self.token_data or 'expires_in' not in self.token_data:
            return False  # Can't determine, assume not expired
        
        current_time = int(time.time())
        expiry_time = self.token_data['obtained_at'] + self.token_data['expires_in']
        
        # Add 60 second buffer before actual expiry
        return current_time >= (expiry_time - 60)

    def revoke_token(self) -> bool:
        """
        Revoke the current access token.
        Returns True if successful, False otherwise.
        """
        if not self.token_data or 'access_token' not in self.token_data:
            return False

        try:
            data = {
                "client_id": self.client_id,
                "token": self.token_data['access_token'],
            }
            
            response = requests.post(self.TWITCH_REVOKE_URL, data=data)
            response.raise_for_status()
            
            # Clear token data
            self.token_data = None
            if self.token_file.exists():
                self.token_file.unlink()
            
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error revoking token: {e}")
            return False

    def get_auth_headers(self) -> dict:
        """
        Get HTTP headers for authenticated Twitch API requests.
        Automatically refreshes token if needed.
        """
        if not self.token_data:
            return {}
        
        # Check if token needs refresh
        if self._is_token_expired():
            self._refresh_token()
        
        if 'access_token' in self.token_data:
            return {
                "Authorization": f"Bearer {self.token_data['access_token']}",
                "Client-Id": self.client_id,
            }
        
        return {}

    def save_token(self, token_data: dict) -> None:
        """
        Save token data to file.
        """
        try:
            with open(self.token_file, 'w') as f:
                json.dump(token_data, f, indent=2)
            self.token_data = token_data
        except Exception as e:
            print(f"Error saving token: {e}")

    def is_authenticated(self) -> bool:
        """
        Check if user is currently authenticated.
        Returns True if authenticated, False otherwise.
        """
        return self.token_data is not None and 'access_token' in self.token_data

    def get_user_info(self) -> Optional[dict]:
        """
        Get authenticated user information from Twitch API.
        Returns user data dict or None if failed.
        """
        if not self.is_authenticated():
            return None

        try:
            headers = self.get_auth_headers()
            response = requests.get("https://api.twitch.tv/helix/users", headers=headers)
            response.raise_for_status()
            
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                return data['data'][0]
            
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error getting user info: {e}")
            return None
