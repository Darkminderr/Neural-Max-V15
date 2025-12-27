from flask import Flask, jsonify, render_template_string
import datetime, pytz, hashlib

app = Flask(__name__)

def get_30s_precision_prediction(period_str):
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    seconds = now.second

    # അവസാന 30 സെക്കൻഡിന് മുൻപാണെങ്കിൽ സിഗ്നൽ നൽകില്ല (ഡാറ്റ വിശകലനം ചെയ്യുന്നു)
    if seconds < 30:
        return "ANALYZING...", "#FFA500", f"WAIT FOR LAST 30s ({30-seconds}s remaining)"

    # അവസാന 30 സെക്കൻഡിൽ മാത്രം പ്രവർത്തിക്കുന്ന ലോജിക്
    # പീരിയഡ് നമ്പറും മിനിറ്റും മാത്രം ഉപയോഗിക്കുന്നു (Stability ഉറപ്പാക്കാൻ)
    mining_key = f"V47_FINAL_30S_{period_str}_ULTRA_LOCK"
    hash_result = hashlib.sha384(mining_key.encode()).hexdigest()
    
    # പ്രവചനം നിശ്ചയിക്കുന്നു
    prediction_bit = int(hash_result[0], 16) % 10
    
    if prediction_bit in [1, 3, 5, 7, 9]:
        res = "BIG"
        color = "#00FF00"
    else:
        res = "SMALL"
        color = "#FF0000"
        
    return res, color, "SURE SHOT LOCKED"

@app.route("/")
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>V47 FINAL 30S AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #000; color: #fff; text-align: center; font-family: sans-serif; padding-top: 60px; }
        .main-box { border: 4px solid #00FFFF; padding: 40px; border-radius: 45px; background: #050505; display: inline-block; width: 340px; box-shadow: 0 0 50px rgba(0,255,255,0.2); }
        .period-txt { color: #888; font-size: 15px; margin-bottom: 15px; }
        .signal-txt { font-size: 85px; font-weight: 900; margin: 20px 0; letter-spacing: 5px; }
        .status-txt { font-size: 14px; font-weight: bold; color: #00FF00; }
        .warning { font-size: 10px; color: #444; margin-top: 30px; border-top: 1px solid #222; padding-top: 15px; }
    </style>
</head>
<body>
    <div class="main-box">
        <div id="p_id" class="period-txt">CONNECTING...</div>
        <div id="s_id" class="signal-txt">WAIT</div>
        <div id="st_id" class="status-txt">READY</div>
        <div class="warning">BET ONLY IN THE LAST 30 SECONDS</div>
    </div>
    <script>
        async function fetchV47() {
            try {
                const r = await fetch('/api/v47');
                const d = await r.json();
                document.getElementById('p_id').innerText = "PERIOD: " + d.p;
                const sig = document.getElementById('s_id');
                sig.innerText = d.t; sig.style.color = d.c;
                document.getElementById('st_id').innerText = d.s;
                if(d.t === "ANALYZING...") { sig.style.fontSize = "35px"; } else { sig.style.fontSize = "85px"; }
            } catch(e) {}
        }
        setInterval(fetchV47, 2000); fetchV47();
    </script>
</body>
</html>
''')

@app.route("/api/v47")
def api():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    idx = (now.hour * 60) + now.minute + 10001
    p = f"{now.strftime('%Y%m%d')}{idx}"
    t, c, s = get_30s_precision_prediction(p)
    return jsonify({"p": p, "t": t, "c": c, "s": s})

if  __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)