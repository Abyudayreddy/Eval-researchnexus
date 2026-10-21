import json
import base64
import subprocess
import time
import urllib.request
import websocket
import os

def capture_theme(theme_name, output_path, route=""):
    url = f"http://localhost:5173{route}"
    # Start Chrome with remote debugging
    chrome_proc = subprocess.Popen([
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--remote-debugging-port=9222",
        "--remote-allow-origins=*",
        "--window-size=1440,900",
        "--disable-gpu",
        "--no-sandbox"
    ])
    time.sleep(2)

    try:
        req = urllib.request.Request("http://localhost:9222/json/new?" + urllib.parse.quote(url), method="PUT")
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

        # Set auth token and theme via localStorage before navigation
        js_setup = f"""
        localStorage.setItem('researchnexus_token', 'mock_token_for_qa');
        localStorage.setItem('researchnexus_theme_mode', '{theme_name}');
        """
        send_cdp("Runtime.evaluate", {"expression": js_setup})
        
        # Navigate to target route
        send_cdp("Page.navigate", {"url": url})
        time.sleep(3) # allow page & components to render

        # Apply theme class to document
        js_code = f"""
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
        send_cdp("Runtime.evaluate", {"expression": js_code})
        time.sleep(1.5)

        # Get screenshot
        shot = send_cdp("Page.captureScreenshot", {"format": "png"})
        img_data = base64.b64decode(shot["data"])
        with open(output_path, "wb") as f:
            f.write(img_data)
        print(f"Captured {theme_name} screenshot to {output_path} ({len(img_data)} bytes)")

        # Also get computed styles of key elements
        inspect_code = """
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
                inputColor: getColor('input[type="text"]'),
                starterBg: getBg('div[class*="rounded-full"][class*="cursor-pointer"]'),
                starterText: getColor('div[class*="rounded-full"][class*="cursor-pointer"] span')
            });
        })()
        """
        eval_res = send_cdp("Runtime.evaluate", {"expression": inspect_code})
        print(f"Computed styles for {theme_name}:", eval_res.get("result", {}).get("value"))

        ws.close()
    finally:
        chrome_proc.terminate()

if __name__ == "__main__":
    import urllib.parse
    out_dir = r"C:\Users\Abyureddy\.gemini\antigravity\brain\754ade24-cacb-4027-b694-4df14416b28a"
    capture_theme("dark", os.path.join(out_dir, "explorer_dark_real.png"), route="/hybrid-search")
    capture_theme("relax", os.path.join(out_dir, "explorer_relax_real.png"), route="/hybrid-search")
    capture_theme("light", os.path.join(out_dir, "explorer_light_real.png"), route="/hybrid-search")
    capture_theme("dark", os.path.join(out_dir, "assistant_dark_real.png"), route="/assistant")
