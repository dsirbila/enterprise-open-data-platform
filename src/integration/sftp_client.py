"""lecture 15: SFTP client — B2B partner feed ინტეგრაცია."""
import logging
import paramiko

logger = logging.getLogger(__name__)

class SFTPIntegrationError(Exception):
    """SFTP-თან დაკავშირებული ნებისმიერი შეცდომა."""

class SFTPClient:
    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self._transport = None
        self._sftp = None

    def connect(self) -> None:
        try:
            self._transport = paramiko.Transport((self.host, self.port))
            self._transport.connect(username=self.username, password=self.password)
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        except paramiko.SSHException as exc:
            raise SFTPIntegrationError(f"SFTP დაკავშირება ჩავარდა: {exc}") from exc
        logger.info("SFTP დაკავშირება წარმატებულია: %s:%s", self.host, self.port)

    def close(self) -> None:
        if self._sftp:
            self._sftp.close()
        if self._transport:
            self._transport.close()

    def list_new_files(self, remote_dir: str) -> list:
        return [f for f in self._sftp.listdir(remote_dir) if f.endswith((".csv", ".xml"))]

    def download(self, remote_path: str, local_path: str) -> None:
        self._sftp.get(remote_path, local_path)

    def upload(self, local_path: str, remote_path: str) -> None:
        self._sftp.put(local_path, remote_path)

    def move_remote(self, src: str, dst: str) -> None:
        self._sftp.rename(src, dst)

    def __enter__(self) -> "SFTPClient":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
