import urllib.request

url = "https://jobs.ashbyhq.com/neon/software-engineer-backend"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8')
        if '"posting":null' in html:
            print("Neon is EXPIRED")
        else:
            print("Neon is ACTIVE")
except Exception as e:
    print(f"Error checking Neon: {e}")
