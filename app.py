from flask import Flask, jsonify, render_template_string
import datetime, pytz, math

app = Flask(__name__)

def auto_mining_v18_logic(period_str):
    """
    V18 PRO MAX: Auto-Trend Analysis Logic.
    ലക്ഷ്യം: 2-3 ലെവൽ വിന്നിംഗ്.
    """
    try:
        d = [int(x) for x in period_str]
        last_digits = d[-5:]
        
        # 1. ലെയർ: അഡ്വാൻസ്ഡ് പാറ്റേൺ കാൽക്കുലേഷൻ
        # പീരിയഡ് നമ്പറിലെ അക്കങ്ങളെ സ്ക്വയർ ചെയ്ത് വിശകലനം ചെയ്യുന്നു
        calc = sum([x**2 for x in last_digits])
        
        # 2. ലെയർ: ട്രെൻഡ് കൺട്രോളർ (Dragon Trend Protection)
        # സമയം (മിനിറ്റ്) അടിസ്ഥാനമാക്കി പാറ്റേൺ ബാലൻസ് ചെയ്യുന്നു
        ist = pytz.timezone('Asia/Kolkata')
        minute = datetime.datetime.now(ist).minute
        
        final_val = (calc + minute + 1.618) % 10
        
        # 3. ലെയർ: സ്ട്രിക്റ്റ് ഔട്ട്പുട്ട് (Classic Big/Small)
        if final_val >= 5.0:
            return "BIG", "#00FF00" # Green
        else:
            return "SMALL", "#FF0000" # Red
            
    except Exception as e:
        return "WAIT", "#FFFFFF"

@app.route("/")
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>AI V18 PRO MAX</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }
        .container { border: 5px solid #333; padding: 40px; border-radius: 30px; max-width: 350px; margin: auto; background: #111; box-shadow: 0 0 20px rgba(0,255,0,0.1); }
        #res { font-size: 80px; font-weight: bold; margin: 20px 0; text-shadow: 0 0 20px rgba(255,255,255,0.2); }
        .p-box { color: #FFA500; font-size: 18px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #222; padding-bottom: 10px; }
        .status-bar { font-size: 12px; color: #00FF00; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="status-bar">V18 PRO MAX ACTIVE</div>
        <div id="p_id" class="p-box">SYNCING...</div>
        <div id="res">---</div>
        <div style="font-size:10px; color:#555;">AUTO-MINING DATA...</div>
    </div>
    <p style="margin-top:20px; font-size:12px; color:#888;">TARGET: 3 LEVELS<br>STRICTLY FOLLOW 1x-3x-9x</p>

    <script>
        async function loadSignal() {
            try {
                let r = await fetch('/api/v18');
                let d = await r.json();
                document.getElementById('p_id').innerText = "PERIOD: " + d.p;
                let s = document.getElementById('res');
                s.innerText = d.s;
                s.style.color = d.c;
            } catch(e) {
                document.getElementById('res').innerText = "ERROR";
            }
        }
        setInterval(loadSignal, 3000);
        loadSignal();
    </script>
</body>
</html>
''')

@app.route("/api/v18")
def api():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.datetime.now(ist)
        # പീരിയഡ് നമ്പർ കൃത്യമായി കാൽക്കുലേഷൻ ചെയ്യുന്നു
        idx = (now.hour * 60) + now.minute + 10001
        p_str = f"{now.strftime('%Y%m%d')}{idx}"
        
        s, c = auto_mining_v18_logic(p_str)
        return jsonify({"p": p_str, "s": s, "c": c})
    except:
        return jsonify({"p": "ERROR", "s": "RETRY", "c": "#FFF"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)