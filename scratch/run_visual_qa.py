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

def capture_page(theme_name, route, output_filename, viewport=(1440, 900)):
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

        # Inject auth token, user info, and theme
        init_js = f"""
        localStorage.setItem('researchnexus_token', '{TOKEN}');
        localStorage.setItem('researchnexus_theme_mode', '{theme_name}');
        """
        send_cdp("Runtime.evaluate", {"expression": init_js})

        # Navigate to target authenticated route
        send_cdp("Page.navigate", {"url": url})
        time.sleep(3.5) # allow data fetching and rendering

        # Apply CSS classes on HTML
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

        # Capture screenshot
        shot = send_cdp("Page.captureScreenshot", {"format": "png"})
        img_bytes = base64.b64decode(shot["data"])
        out_path = os.path.join(OUT_DIR, output_filename)
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"Captured {theme_name} [{route}] -> {output_filename} ({len(img_bytes)} bytes)")

        # Query colors of key components
        diag_js = """
        (() => {
            const getBg = sel => {
                const el = document.querySelector(sel);
                return el ? window.getComputedStyle(el).backgroundColor : 'NOT_FOUND';
            };
            const getColor = sel => {
                const el = document.querySelector(sel);
                return el ? window.getComputedStyle(el).color : 'NOT_FOUND';
            };
            return JSON.stringify({
                bodyBg: window.getComputedStyle(document.body).backgroundColor,
                headerBg: getBg('header'),
                inputBg: getBg('input[type="text"]'),
                inputBorder: getBg('input[type="text"]'),
                pillsBg: getBg('div[class*="rounded-full"][class*="cursor-pointer"]')
            });
        })()
        """
        diag_res = send_cdp("Runtime.evaluate", {"expression": diag_js})
        print(f"Diagnostics: {diag_res.get('result', {}).get('value')}")

        ws.close()
    finally:
        chrome_proc.terminate()
        time.sleep(1)

if __name__ == "__main__":
    # Test Research Explorer across all 3 themes
    print("--- 1. Testing Research Explorer ---")
    capture_page("dark", "/hybrid-search", "qa_explorer_dark.png")
    capture_page("relax", "/hybrid-search", "qa_explorer_relax.png")
    capture_page("light", "/hybrid-search", "qa_explorer_light.png")

    # Test AI Assistant
    print("--- 2. Testing AI Assistant ---")
    capture_page("dark", "/assistant", "qa_assistant_dark.png")
    capture_page("relax", "/assistant", "qa_assistant_relax.png")

    # Test Dashboard & Settings
    print("--- 3. Testing Dashboard & Settings ---")
    capture_page("dark", "/dashboard", "qa_dashboard_dark.png")
    capture_page("dark", "/settings", "qa_settings_dark.png")
