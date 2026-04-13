# backend/data_loader.py
from pathlib import Path
import pandas as pd
 
 
class DataLoader:
    def __init__(self, data_dir: str = None):
        backend_dir = Path(__file__).resolve().parent
        project_root = backend_dir.parent
 
        # Your dataset is directly inside project_root/data
        self.data_dir = Path(data_dir) if data_dir else (project_root / "data")
 
        self.users = None
        self.assets = None
        self.auth_logs = None
        self.endpoint_logs = None
        self.dns_logs = None
        self.proxy_logs = None
        self.email_logs = None
        self.cloudtrail_logs = None
 
    def load_all(self):
        print("Loading data from:", self.data_dir)
 
        self.users = pd.read_csv(self.data_dir / "users.csv")
        self.assets = pd.read_csv(self.data_dir / "assets.csv")
        self.auth_logs = pd.read_csv(self.data_dir / "auth_logs.csv")
        self.endpoint_logs = pd.read_csv(self.data_dir / "endpoint_logs.csv")
        self.dns_logs = pd.read_csv(self.data_dir / "dns_logs.csv")
        self.proxy_logs = pd.read_csv(self.data_dir / "proxy_logs.csv")
        self.email_logs = pd.read_csv(self.data_dir / "email_logs.csv")
        self.cloudtrail_logs = pd.read_csv(self.data_dir / "cloudtrail_logs.csv")
 
        self._normalize()
 
    def _normalize(self):
        for df_name in [
            "auth_logs",
            "endpoint_logs",
            "dns_logs",
            "proxy_logs",
            "email_logs",
            "cloudtrail_logs",
        ]:
            df = getattr(self, df_name)
            if df is not None and "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
 
        for df_name in [
            "users",
            "assets",
            "auth_logs",
            "endpoint_logs",
            "dns_logs",
            "proxy_logs",
            "email_logs",
            "cloudtrail_logs",
        ]:
            df = getattr(self, df_name)
            if df is None:
                continue
            for col in df.columns:
                if df[col].dtype == object:
                    df[col] = df[col].fillna("").astype(str).str.strip()
 
    def get_all(self):
        return {
            "users": self.users,
            "assets": self.assets,
            "auth_logs": self.auth_logs,
            "endpoint_logs": self.endpoint_logs,
            "dns_logs": self.dns_logs,
            "proxy_logs": self.proxy_logs,
            "email_logs": self.email_logs,
            "cloudtrail_logs": self.cloudtrail_logs,
        }