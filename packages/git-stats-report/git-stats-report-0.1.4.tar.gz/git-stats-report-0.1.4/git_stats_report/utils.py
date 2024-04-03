import subprocess


def run_command(command: str) -> str:
    return subprocess.check_output(command, shell=True).decode("utf-8")
