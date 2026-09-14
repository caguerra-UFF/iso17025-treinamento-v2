import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
CLIENT_SECRETS_FILE = Path(r"F:\Transcricoes_Consolidadas\client_oauth.json")
TOKEN_FILE = Path(r"F:\Transcricoes_Consolidadas\token_gcloud.json")

def get_credentials():
    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception:
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Atualizando token expirado...", flush=True)
            creds.refresh(Request())
        else:
            print("Iniciando fluxo de autorização no navegador...", flush=True)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=8080, open_browser=True, prompt="consent")
        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())
    return creds

if __name__ == "__main__":
    print("Iniciando autenticação Google Cloud (OAuth)...", flush=True)
    creds = get_credentials()
    print("Autenticação realizada com sucesso!", flush=True)
    print("Token salvo em:", TOKEN_FILE, flush=True)
