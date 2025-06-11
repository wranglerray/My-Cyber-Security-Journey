import cmd
import requests
import urllib.parse

class SQLShell(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "sql> "

    def default(self, line):
        # URL-encode the user input
        encoded_line = urllib.parse.quote(line)
        url = f"http://10.10.110.20/api/v1/user/validate/{encoded_line}"
        try:
            r = requests.get(url)
            print(r.text)
        except requests.RequestException as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    shell = SQLShell()
    shell.cmdloop()

