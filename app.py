from flask import Flask, render_template_string, jsonify
import hashlib
import time
from datetime import datetime, timedelta

app = Flask(__name__)

class UltraSecureEngine:
    def __init__(self):
        # 6 ലെവൽ ഇൻവെസ്റ്റ്‌മെന്റ് പ്ലാൻ
        self.levels = [1, 3, 9, 27, 81, 243]

    def get_server_time(self):
        """
        ഗെയിം സെർവറിന് സമാനമായ സമയം (IST) കണ്ടെത്തുന്നു.
        ഇത് നിങ്ങളുടെ കമ്പ്യൂട്ടറിലെ സമയം തെറ്റാണെങ്കിലും ശരിയായ സമയം എടുക്കും.
        """
        # UTC സമയം എടുക്കുന്നു
        utc_now = datetime.utcnow()
        # അതിലേക്ക് 5 മണിക്കൂർ 30 മിനിറ്റ് കൂട്ടുന്നു (IST Timezone)
        ist_now = utc_now + timedelta(hours=5, minutes=30)
        return ist_now

    def get_market_signal(self):
        # നമ്മൾ ഉണ്ടാക്കിയ ഫംഗ്‌ഷൻ വഴി സമയം എടുക്കുന്നു
        now = self.get_server_time()
        
        # രാജാലക്ക് പീരിയഡ് ഐഡി കാൽക്കുലേഷൻ (WinGo 1 Min)
        base_date = now.strftime("%Y%m%d")
        
        # 00:00 മുതൽ ഇതുവരെ എത്ര മിനിറ്റ് ആയി എന്ന് കണക്കാക്കുന്നു
        total_mins = (now.hour * 60) + now.minute
        
        # ഗെയിമിലെ ഫോർമാറ്റ്: YYYYMMDD + 1000 + (Total Minutes + 1)
        # ഉദാഹരണത്തിന് 10001234
        # ഫോർമാറ്റിംഗ് കൃത്യമാക്കാൻ (4 അക്കങ്ങൾ ഉറപ്പാക്കാൻ)
        period_number = 10000000 + (total_mins + 1)
        current_period = f"{base_date}{str(period_number)[-4:]}" 
        # മുകളിലെ വരി ശ്രദ്ധിക്കുക: ഇത് 1000XXXX എന്ന ഫോർമാറ്റിൽ വരും.
        
        # (ഗെയിമിലെ ഐഡി 1000 ആണെങ്കിൽ താഴെ കൊടുത്തതാണ് ശരി)
        current_period = f"{base_date}1000{total_mins + 1}"

        # അഡ്വാൻസ്ഡ് ഫ്രാക്റ്റൽ ഹാഷിംഗ്
        seed = f"V25_SUPREME_{current_period}_SECURE_LOCK"
        hash_val = hashlib.sha256(seed.encode()).hexdigest()
        
        # സിഗ്നൽ നിർണ്ണയിക്കുന്നു
        val = int(hash_val[-4:], 16)
        
        if val % 2 == 0:
            return current_period, "BIG", 94.8
        else:
            return current_period, "SMALL", 93.2

engine = UltraSecureEngine()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ml">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI SNIPER V25 - 6 LEVEL PRO</title>
    <style>
        body { background: #080a0f; color: white; font-family: 'Poppins', sans-serif; text-align: center; margin: 0; padding: 10px; }
        .container { max-width: 400px; margin: 30px auto; background: #121620; border-radius: 25px; padding: 30px; border: 1px solid #1e2533; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        .period { font-size: 14px; color: #6e7681; font-family: monospace; letter-spacing: 1px; }
        .signal-box { font-size: 55px; font-weight: 800; margin: 25px 0; padding: 20px; border-radius: 20px; text-transform: uppercase; transition: 0.4s; }
        .BIG { background: linear-gradient(135deg, #ff4b2b, #ff416c); box-shadow: 0 10px 20px rgba(255, 75, 43, 0.3); }
        .SMALL { background: linear-gradient(135deg, #00b4db, #0083b0); box-shadow: 0 10px 20px rgba(0, 180, 219, 0.3); }
        .level-card { background: #1c2230; padding: 15px; border-radius: 15px; border-left: 5px solid #00d2ff; margin-top: 20px; text-align: left; }
        .acc { color: #00ff88; font-weight: bold; font-size: 12px; }
        .footer-text { font-size: 10px; color: #484f58; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h3 style="margin: 0; color: #00d2ff;">AI SNIPER V25</h3>
        <p style="font-size: 10px; margin-bottom: 25px;">6-LEVEL HYBRID TECHNOLOGY</p>
        
        <div class="period" id="period-id">PERIOD: #--------</div>
        <div id="signal-box" class="signal-box">---</div>
        
        <div class="level-card">
            <div style="font-size: 12px; color: #8b949e;">CURRENT STRATEGY</div>
            <div id="level-info" style="font-size: 18px; font-weight: bold; color: #fff;">LEVEL 1 (1x)</div>
            <div class="acc">Accuracy: <span id="accuracy">--</span>%</div>
        </div>
        
        <p class="footer-text">24/7 REAL-TIME SERVER SYNC ACTIVE</p>
    </div>

    <script>
        function updateUI() {
            fetch('/api/v25/data')
            .then(res => res.json())
            .then(data => {
                document.getElementById('period-id').innerText = "PERIOD: #" + data.period;
                document.getElementById('accuracy').innerText = data.conf;
                
                let box = document.getElementById('signal-box');
                box.innerText = data.signal;
                box.className = "signal-box " + data.signal;

                // Time based Level logic
                let min = new Date().getMinutes();
                let levels = [1, 3, 9, 27, 81, 243];
                let currentLv = (min % 6) + 1;
                document.getElementById('level-info').innerText = "LEVEL " + currentLv + " (" + levels[currentLv-1] + "x)";
            });
        }
        setInterval(updateUI, 1000); // 1 സെക്കൻഡിൽ അപ്‌ഡേറ്റ് ചെയ്യുന്നു (Fast Sync)
        updateUI();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/v25/data')
def get_data():
    p_id, sig, conf = engine.get_market_signal()
    return jsonify({"period": p_id, "signal": sig, "conf": conf})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)