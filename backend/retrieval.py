# backend/retrieval.py
from typing import Optional, List, Dict, Any
import pandas as pd
from data_loader import DataLoader
 
 
class RetrievalService:
    def __init__(self, loader: DataLoader):
        self.loader = loader
 
        self.users = loader.users
        self.assets = loader.assets
        self.auth = loader.auth_logs
        self.endpoint = loader.endpoint_logs
        self.dns = loader.dns_logs
        self.proxy = loader.proxy_logs
        self.email = loader.email_logs
        self.cloud = loader.cloudtrail_logs
 
    # ---------------------------
    # Context helpers
    # ---------------------------
 
    def get_user_context(self, user_id: str) -> Dict[str, Any]:
        row = self.users[self.users["user_id"] == user_id]
        if row.empty:
            return {}
        return row.iloc[0].to_dict()
 
    def get_asset_context(self, hostname: str) -> Dict[str, Any]:
        row = self.assets[self.assets["hostname"] == hostname]
        if row.empty:
            return {}
        return row.iloc[0].to_dict()
 
    def get_assets_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        rows = self.assets[self.assets["owner_user_id"] == user_id]
        return rows.to_dict(orient="records")
 
    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        row = self.users[self.users["email"] == email]
        if row.empty:
            return {}
        return row.iloc[0].to_dict()
 
    # ---------------------------
    # Generic time filter
    # ---------------------------
 
    def _time_filter(
        self,
        df: pd.DataFrame,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        result = df.copy()
        if start is not None:
            result = result[result["timestamp"] >= start]
        if end is not None:
            result = result[result["timestamp"] <= end]
        return result
 
    # ---------------------------
    # Auth events
    # ---------------------------
 
    def get_auth_events(
        self,
        user_id: Optional[str] = None,
        src_ip: Optional[str] = None,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        df = self._time_filter(self.auth, start, end)
        if user_id:
            df = df[df["user_id"] == user_id]
        if src_ip:
            df = df[df["src_ip"] == src_ip]
        return df.sort_values("timestamp")
 
    # ---------------------------
    # Endpoint events
    # ---------------------------
 
    def get_endpoint_events(
        self,
        host: Optional[str] = None,
        user_id: Optional[str] = None,
        process_name: Optional[str] = None,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        df = self._time_filter(self.endpoint, start, end)
        if host:
            df = df[df["host"] == host]
        if user_id:
            df = df[df["user_id"] == user_id]
        if process_name:
            df = df[df["process_name"].str.lower() == process_name.lower()]
        return df.sort_values("timestamp")
 
    # ---------------------------
    # DNS events
    # ---------------------------
 
    def get_dns_events(
        self,
        host: Optional[str] = None,
        domain: Optional[str] = None,
        user_id: Optional[str] = None,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        df = self._time_filter(self.dns, start, end)
        if host:
            df = df[df["src_host"] == host]
        if user_id:
            df = df[df["user_id"] == user_id]
        if domain:
            df = df[df["query"].str.contains(domain, case=False, na=False)]
        return df.sort_values("timestamp")
 
    # ---------------------------
    # Proxy events
    # ---------------------------
 
    def get_proxy_events(
        self,
        host: Optional[str] = None,
        domain: Optional[str] = None,
        user_id: Optional[str] = None,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        df = self._time_filter(self.proxy, start, end)
        if host:
            df = df[df["src_host"] == host]
        if user_id:
            df = df[df["user_id"] == user_id]
        if domain:
            df = df[df["domain"].str.contains(domain, case=False, na=False)]
        return df.sort_values("timestamp")
 
    # ---------------------------
    # Email events
    # ---------------------------
 
    def get_email_events(
        self,
        user_id: Optional[str] = None,
        recipient_email: Optional[str] = None,
        domain: Optional[str] = None,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        df = self._time_filter(self.email, start, end)
        if user_id:
            df = df[df["recipient_user_id"] == user_id]
        if recipient_email:
            df = df[df["recipient_email"] == recipient_email]
        if domain:
            df = df[df["url_domain"].str.contains(domain, case=False, na=False)]
        return df.sort_values("timestamp")
 
    # ---------------------------
    # Cloud events
    # ---------------------------
 
    def get_cloud_events(
        self,
        user_id: Optional[str] = None,
        source_ip: Optional[str] = None,
        event_name: Optional[str] = None,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        df = self._time_filter(self.cloud, start, end)
        if user_id:
            df = df[df["user_id"] == user_id]
        if source_ip:
            df = df[df["source_ip"] == source_ip]
        if event_name:
            df = df[df["event_name"].str.lower() == event_name.lower()]
        return df.sort_values("timestamp")
 
    # ---------------------------
    # Cross-source helpers
    # ---------------------------
 
    def get_recent_activity_bundle(
        self,
        user_id: str,
        host: Optional[str],
        start: pd.Timestamp,
        end: pd.Timestamp,
    ) -> Dict[str, Any]:
        return {
            "user_context": self.get_user_context(user_id),
            "asset_context": self.get_asset_context(host) if host else {},
            "auth_events": self.get_auth_events(user_id=user_id, start=start, end=end).to_dict(orient="records"),
            "endpoint_events": self.get_endpoint_events(host=host, user_id=user_id, start=start, end=end).to_dict(orient="records"),
            "dns_events": self.get_dns_events(host=host, user_id=user_id, start=start, end=end).to_dict(orient="records"),
            "proxy_events": self.get_proxy_events(host=host, user_id=user_id, start=start, end=end).to_dict(orient="records"),
            "email_events": self.get_email_events(user_id=user_id, start=start - pd.Timedelta(hours=24), end=end).to_dict(orient="records"),
            "cloud_events": self.get_cloud_events(user_id=user_id, start=start, end=end).to_dict(orient="records"),
        }
 
    def domain_prevalence(self, domain: str) -> Dict[str, Any]:
        dns_hits = self.dns[self.dns["query"].str.contains(domain, case=False, na=False)]
        proxy_hits = self.proxy[self.proxy["domain"].str.contains(domain, case=False, na=False)]
        email_hits = self.email[self.email["url_domain"].str.contains(domain, case=False, na=False)]
 
        users = set(dns_hits["user_id"].tolist()) | set(proxy_hits["user_id"].tolist()) | set(email_hits["recipient_user_id"].tolist())
        hosts = set(dns_hits["src_host"].tolist()) | set(proxy_hits["src_host"].tolist())
 
        first_seen = None
        candidate_times = []
        for df in [dns_hits, proxy_hits, email_hits]:
            if not df.empty and "timestamp" in df.columns:
                candidate_times.extend(df["timestamp"].dropna().tolist())
        if candidate_times:
            first_seen = min(candidate_times)
 
        return {
            "domain": domain,
            "users_seen_count": len(users),
            "hosts_seen_count": len(hosts),
            "users_seen": list(users),
            "hosts_seen": list(hosts),
            "first_seen": str(first_seen) if first_seen else None,
            "dns_hits": len(dns_hits),
            "proxy_hits": len(proxy_hits),
            "email_hits": len(email_hits),
        }
 
    def ip_prevalence(self, ip: str) -> Dict[str, Any]:
        auth_hits = self.auth[self.auth["src_ip"] == ip]
        cloud_hits = self.cloud[self.cloud["source_ip"] == ip]
 
        users = set(auth_hits["user_id"].tolist()) | set(cloud_hits["user_id"].tolist())
 
        first_seen = None
        candidate_times = []
        for df in [auth_hits, cloud_hits]:
            if not df.empty:
                candidate_times.extend(df["timestamp"].dropna().tolist())
        if candidate_times:
            first_seen = min(candidate_times)
 
        return {
            "ip": ip,
            "users_seen_count": len(users),
            "users_seen": list(users),
            "auth_hits": len(auth_hits),
            "cloud_hits": len(cloud_hits),
            "first_seen": str(first_seen) if first_seen else None,
        }
 