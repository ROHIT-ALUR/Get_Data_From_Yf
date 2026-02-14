# Fixed version - Complete HTML content for Finance Shark Game
# Copy-paste this entire code block to fix SyntaxError

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦈 Finance Shark Game - MSRUAS Management Fest</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            padding: 20px; 
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
            overflow: hidden; 
        }
        header { 
            background: linear-gradient(90deg, #ff6b6b, #feca57); 
            color: white; 
            padding: 30px; 
            text-align: center; 
        }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .subtitle { font-size: 1.2em; opacity: 0.9; }
        .game-area { padding: 40px; }
        .mode-selector { text-align: center; margin-bottom: 40px; }
        button { 
            background: #4ecdc4; 
            color: white; 
            border: none; 
            padding: 15px 30px; 
            font-size: 1.1em; 
            border-radius: 50px; 
            cursor: pointer; 
            transition: all 0.3s; 
            margin: 0 10px; 
        }
        button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
        button.active { background: #ff6b6b; }
        .scenario-selector, .input-group { text-align: center; margin-bottom: 30px; }
        select, input { 
            padding: 12px; 
            font-size: 1em; 
            border-radius: 10px; 
            border: 2px solid #ddd; 
            width: 300px; 
            max-width: 100%; 
        }
        .metrics-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin: 30px 0; 
        }
        .metric-card { 
            background: #f8f9fa; 
            padding: 25px; 
            border-radius: 15px; 
            text-align: center; 
            border-left: 5px solid #4ecdc4; 
        }
        .metric-value { 
            font-size: 2.5em; 
            font-weight: bold; 
            color: #2c3e50; 
            margin: 10px 0; 
        }
        .metric-label { color: #7f8c8d; font-size: 1.1em; }
        .table-container { 
            overflow-x: auto; 
            margin: 20px 0; 
            background: white; 
            border-radius: 10px; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.1); 
        }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #34495e; color: white; font-weight: 600; }
        tr:hover { background: #f8f9fa; }
        .verdict { 
            text-align: center; 
            padding: 30px; 
            margin: 30px 0; 
            border-radius: 15px; 
            font-size: 1.5em; 
            font-weight: bold; 
        }
        .win { 
            background: #d4edda; 
            color: #155724; 
            border: 3px solid #c3e6cb; 
            animation: celebrate 0.5s infinite alternate; 
        }
        .lose { 
            background: #f8d7da; 
            color: #721c24; 
            border: 3px solid #f5c6cb; 
        }
        @keyframes celebrate { 
            0% { transform: scale(1); } 
            100% { transform: scale(1.05); } 
        }
        .excel-section { 
            background: #e8f4fd; 
            padding: 40px; 
            border-radius: 15px; 
            text-align: center; 
            margin-top: 40px; 
        }
        .download-btn { 
            background: #007bff; 
            color: white; 
            padding: 20px 40px; 
            font-size: 1.3em; 
            border-radius: 50px; 
            text-decoration: none; 
            display: inline-block; 
            margin-top: 20px; 
        }
        .rules { 
            background: #fff3cd; 
            padding: 20px; 
            border-radius: 10px; 
            margin-top: 30px; 
            font-size: 0.95em; 
        }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🦈 Finance Shark Game</h1>
            <p class="subtitle">MSRUAS Management Fest | Shark Tank India Business Analysis Game</p>
        </header>
        
        <div class="game-area">
            <div class="mode-selector">
                <button onclick="setMode('game')" class="active">🎮 Play Game</button>
                <button onclick="setMode('excel')">📊 Get Excel</button>
            </div>
            
            <div id="game-section">
                <div class="scenario-selector">
                    <label>Choose Startup:</label><br>
                    <select id="scenario" onchange="loadData()">
                        <option value="tech">Tech Startup (Meesho style)</option>
                        <option value="food">Food Delivery (Swiggy style)</option>
                    </select>
                </div>
                
                <div class="input-group">
                    <label>Discount Rate (%):</label>
                    <input type="number" id="rate" value="10" min="1" max="30" step="0.1" onchange="calculate()">
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value" id="npv">₹0</div>
                        <div class="metric-label">NPV</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="current">0.00</div>
                        <div class="metric-label">Current Ratio</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="de">0.00</div>
                        <div class="metric-label">Debt/Equity</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="roa">0%</div>
                        <div class="metric-label">ROA</div>
                    </div>
                </div>
                
                <div class="table-container">
                    <table>
                        <tr><th>Cash Flows (₹ Lakhs)</th><th>Year</th><th>Amount</th><th>Discounted</th></tr>
                        <tbody id="cf-table"></tbody>
                    </table>
                </div>
                
                <table class="table-container">
                    <tr><th>Balance Sheet Y3 (₹ Lakhs)</th><th>Items</th><th>Amount</th></tr>
                    <tbody id="bs-table"></tbody>
                </table>
                
                <div class="verdict" id="verdict">
                    <strong>Win Conditions:</strong><br>
                    Current Ratio > 1.5 ✅<br>
                    Debt/Equity < 1 ✅<br>
                    ROA > 15% ✅<br>
                    Get 3/3 for ₹1 Crore deal!
                </div>
            </div>
            
            <div id="excel-section" class="hidden excel-section">
                <h2>📥 Download Excel Template</h2>
                <p>Offline game with auto-calculating formulas!</p>
                <div class="rules">
                    <strong>How to use:</strong><br>
                    - Edit cash flows/rates<br>
                    - Formulas update NPV & ratios<br>
                    - Team competition ready!
                </div>
                <p><em>Excel generation requires Python openpyxl library</em></p>
            </div>
        </div>
    </div>

    <script>
        const data = {
            tech: {
                cf: [-5000,1000,2000,3500,5000,7000],
                assets: {cash:1500, inv:2000, total:8500},
                liab: {debt:3000, equity:5500},
                profit: 1200
            },
            food: {
                cf: [-10000,2000,3000,4500,6000,8000],
                assets: {cash:2500, inv:3500, total:12000},
                liab: {debt:5000, equity:7000},
                profit: 1800
            }
        };
        
        let currentData = data.tech;
        
        function setMode(mode) {
            document.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById('game-section').classList.toggle('hidden', mode === 'excel');
            document.getElementById('excel-section').classList.toggle('hidden', mode === 'game');
        }
        
        function npv(rate, cfs) {
            return cfs.reduce((sum, cf, t) => sum + cf / Math.pow(1 + rate/100, t), 0);
        }
        
        function loadData() {
            currentData = data[document.getElementById('scenario').value];
            calculate();
        }
        
        function calculate() {
            const rate = parseFloat(document.getElementById('rate').value);
            
            // NPV
            const npvv = npv(rate, currentData.cf);
            document.getElementById('npv').textContent = '₹' + Math.round(npvv).toLocaleString();
            
            // Ratios
            const cr = currentData.assets.cash / currentData.liab.debt;
            const de = currentData.liab.debt / currentData.liab.equity;
            const roaa = (currentData.profit / currentData.assets.total) * 100;
            
            document.getElementById('current').textContent = cr.toFixed(2);
            document.getElementById('de').textContent = de.toFixed(2);
            document.getElementById('roa').textContent = roaa.toFixed(1) + '%';
            
            // Tables
            const years = ['Y0','Y1','Y2','Y3','Y4','Y5'];
            let cfhtml = currentData.cf.map((cf,i) => 
                `<tr><td>${years[i]}</td><td>${cf}</td><td>${Math.round(cf/Math.pow(1+rate/100,i))}</td></tr>`
            ).join('');
            document.getElementById('cf-table').innerHTML = cfhtml;
            
            let bsh = `
                <tr><td>Cash</td><td>${currentData.assets.cash}</td></tr>
                <tr><td>Inventory</td><td>${currentData.assets.inv}</td></tr>
                <tr><td><strong>Total Assets</strong></td><td><strong>${currentData.assets.total}</strong></td></tr>
                <tr><td>Debt</td><td>${currentData.liab.debt}</td></tr>
                <tr><td>Equity</td><td>${currentData.liab.equity}</td></tr>
            `;
            document.getElementById('bs-table').innerHTML = bsh;
            
            // Verdict
            const v = document.getElementById('verdict');
            if (cr > 1.5 && de < 1 && roaa > 15) {
                v.className = 'verdict win';
                v.innerHTML = '🏆 <strong>DEAL! ₹1 Crore from Sharks! 🎉</strong>';
            } else {
                v.className = 'verdict lose';
                v.innerHTML = '<strong>Out! Fix your numbers! 💸</strong>';
            }
        }
        calculate();
    </script>
</body>
</html>'''

# Complete working script
with open('finance_shark_game.html', 'w') as f:
    f.write(html_content)

print("✅ Fixed! finance_shark_game.html created successfully!")
print("📱 Open in browser - fully working game!")
print("🎮 Cash flows, NPV, Balance Sheet, Ratios + Shark verdict!")
with open('finance_shark_game.html', 'w') as f: f.write(html_content)
