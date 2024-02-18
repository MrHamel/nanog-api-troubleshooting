import getpass
import os

class Credentials:
    '''
    This credentials class is largely unmodified from the original proceedural
    version. It just adds structure for getting and setting this information.
    I do not know if this will cause an issue, but it assumes that "TACACS" is
    the environment variable prefix.

    I went with the 'credentials' name as it's not immediately obvious in the
    that it contains a username and password, versus tokens, or anything else.
    '''

    user: str = os.environ.get(f"TACACS_USERNAME", None)
    password: str = os.environ.get(f"TACACS_PASSWORD", None)

    @staticmethod
    def set():
        if Credentials.user is None:
            '''
            If the username of your system is the same as TACACS, I highly
            recommend transitioning to `getpass.getuser()` instead, to
            automatically fill that in.
            '''
            Credentials.user = input(f"Enter your TACACS username: ")

        if Credentials.password is None:
            Credentials.password = getpass.getpass(prompt=f"TACACS password for {Credentials.user}: ")

    @staticmethod
    def get() -> tuple:
        return (Credentials.user, Credentials.password)