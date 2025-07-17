from bs4 import BeautifulSoup
import requests


class Session:

    __instance = None

    LOGINURL = f"https://ilias3.uni-stuttgart.de/ilias.php?baseClass=ilstartupgui&cmd=post&fallbackCmd=doStandardAuthentication&lang=de&client_id=Uni_Stuttgart"
    PARAMS = {
        "baseClass": "ilstartupgui",
        "cmd": "post",
        "fallbackCmd": "doStandardAuthentication",
        "lang": "de",
        "client_id": "Uni_Stuttgart"
    }

    @staticmethod
    def set_session(username, password):
        if Session.__instance is not None:
            return True
        data = {
            "login_form/input_3/input_4": username,
            "login_form/input_3/input_5": password,
        }
        session = requests.Session()
        session.post(
            Session.LOGINURL, 
            params=Session.PARAMS, 
            data=data, 
            allow_redirects=True
        )
        
        if Session.is_valid(session):
            Session.__instance = session
            return True
        return False

    @staticmethod
    def is_valid(session):
        TESTURL = "https://ilias3.uni-stuttgart.de/ilias.php?baseClass=ilDashboardGUI&cmd=jumpToSelectedItems"
        test_content = BeautifulSoup(session.get(TESTURL).text, "lxml")
        # If "Anmelden" button is present, then we are not already logged in
        if test_content.find(attrs={"class": "glyphicon glyphicon-login"}) is not None:
            return False
        else:
            return True

    @staticmethod
    def get_content(url):
        if Session.__instance is None:
            raise Exception("No global session is set")
        return BeautifulSoup(Session.__instance.get(url).text, 'lxml')

    @staticmethod
    def get_file_content(url):
        if Session.__instance is None:
            raise Exception("No global session is set")
        return Session.__instance.get(url).content
        
