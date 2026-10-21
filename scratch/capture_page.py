import json
import base64
import subprocess
import time
import urllib.request
import urllib.parse
import websocket
import os

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTE3MjUxODYsInN1YiI6ImRlZmF1bHRfdXNlciJ9.sBentYFk7gjibMJ34p_Wvah-vOVmVZ4kwyHqCni-f1E"
OUT_DIR = r"C:\Users\Abyureddy\.gemini\antigravity\brain\754ade24-cacb-4027-b694-4df14416b28a"

def capture_single(theme_name, route, output_filename, viewport=(1440, 900)):
    url = f"http://localhost:5173{route}"
    chrome_proc = subprocess.Popen([
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--remote-debugging-port=9222",
        "--remote-allow-origins=*",
        f"--window-size={viewport[0]},{viewport[1]}",
        "--disable-gpu",
        "--no-sandbox"
    ])
    time.sleep(1.5)

    try:
        req = urllib.request.Request("http://localhost:9222/json/new?" + urllib.parse.quote("http://localhost:5173"), method="PUT")
        with urllib.request.urlopen(req) as resp:
            tab = json.loads(resp.read().decode())
        
        ws_url = tab["webSocketDebuggerUrl"]
        ws = websocket.create_connection(ws_url)

        def send_cdp(method, params=None):
            msg_id = int(time.time() * 1000) % 100000
            payload = {"id": msg_id, "method": method, "params": params or {}}
            ws.send(json.dumps(payload))
            while True:
                res = json.loads(ws.recv())
                if res.get("id") == msg_id:
                    return res.get("result", {})

        send_cdp("Page.enable")
        send_cdp("Runtime.enable")

        init_js = f"""
        localStorage.setItem('researchnexus_token', '{TOKEN}');
        localStorage.setItem('researchnexus_theme_mode', '{theme_name}');
        """
        send_cdp("Runtime.evaluate", {"expression": init_js})

        send_cdp("Page.navigate", {"url": url})
        time.sleep(3.5)

        apply_theme_js = f"""
        document.documentElement.classList.remove('theme-light', 'theme-dark', 'theme-relax', 'dark');
        if ('{theme_name}' === 'dark') {{
            document.documentElement.classList.add('dark', 'theme-dark');
        }} else if ('{theme_name}' === 'relax') {{
            document.documentElement.classList.add('theme-relax');
        }} else {{
            document.documentElement.classList.add('theme-light');
        }}
        document.documentElement.setAttribute('data-theme', '{theme_name}');
        """
        send_cdp("Runtime.evaluate", {"expression": apply_theme_js})
        time.sleep(1.0)

        shot = send_cdp("Page.captureScreenshot", {"format": "png"})
        img_bytes = base64.b64decode(shot["data"])
        out_path = os.path.join(OUT_DIR, output_filename)
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"Captured {theme_name} [{route}] -> {output_filename}")
        ws.close()
    finally:
        chrome_proc.terminate()
        time.sleep(1)

if __name__ == "__main__":
    import sys
    theme = sys.argv[1] if len(sys.argv) > 1 else "dark"
    route = sys.argv[2] if len(sys.argv) > 2 else "/hybrid-search"
    out_file = sys.argv[3] if len(sys.argv) > 3 else "test.png"
    capture_single(theme, route, out_file)
