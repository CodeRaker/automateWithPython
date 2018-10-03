import subprocess, os

class Commands:
    def inSystem(self, command):
        os.system(command)
    def subSystem(self, command):
        try:
            c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            return [c.stdout.read().decode("utf-8"),c.stderr.read().decode("utf-8")]
        except Exception as e:
            raise
