import getpass
import os

class Credentials:
    user: str = os.environ.get(f"TACACS_USERNAME", None)
    password: str = os.environ.get(f"TACACS_PASSWORD", None)

    @staticmethod
    def set():
        if Credentials.user is None:
            Credentials.user = input(f"Enter your TACACS username: ")

        if Credentials.password is None:
            Credentials.password = getpass.getpass(prompt=f"TACACS password for {Credentials.user}: ")

    @staticmethod
    def get() -> tuple:
        return (Credentials.user, Credentials.password)