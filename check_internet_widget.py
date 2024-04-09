import subprocess

def check_connectivity():
    try:
        subprocess.check_call(['ping', '-c', '1', '8.8.8.8'], stdout=subprocess.DEVNULL)
        return "🌐 10-2"
    except subprocess.CalledProcessError:
        return "🔴🔴🔴 No Internetz?"

