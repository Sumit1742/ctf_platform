/* ============================================
   HackArena CTF — Terminal Dark Theme
   ============================================ */

:root {
  --bg:          #0a0e12;
  --bg2:         #0f1318;
  --bg3:         #141a21;
  --border:      #1e2a35;
  --border-glow: #00ff9d33;
  --green:       #00ff9d;
  --green-dim:   #00cc7a;
  --cyan:        #00d4ff;
  --red:         #ff4444;
  --amber:       #ffb800;
  --purple:      #a855f7;
  --text:        #c8d6e5;
  --text-dim:    #5a7a8a;
  --text-muted:  #3a5060;
  --mono:        'Share Tech Mono', monospace;
  --sans:        'Rajdhani', sans-serif;
  --radius:      4px;
  --radius-lg:   8px;

  --cat-web:       #378ADD;
  --cat-crypto:    #a855f7;
  --cat-osint:     #00ff9d;
  --cat-forensics: #ffb800;
  --cat-pwn:       #ff4444;
  --cat-misc:      #5a7a8a;
  --cat-rev:       #f472b6;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  font-size: 16px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

/* Scanline overlay */
.scanlines {
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.07) 2px,
    rgba(0,0,0,0.07) 4px
  );
  pointer-events: none;
  z-index: 9999;
}

/* ---- NAVBAR ---- */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  height: 56px;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  font-family: var(--mono);
  font-size: 1.1rem;
  color: var(--green);
  text-decoration: none;
  letter-spacing: 2px;
}

.nav-brand .bracket { color: var(--text-dim); }

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  list-style: none;
}

.nav-links a {
  color: var(--text-dim);
  text-decoration: none;
  font-family: var(--mono);
  font-size: 0.85rem;
  letter-spacing: 1px;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.active { color: var(--green); }

.nav-links a.active { border-bottom: 1px solid var(--green); }

.nav-user { color: var(--cyan) !important; }
.nav-logout { color: var(--red) !important; }

.score-badge {
  font-family: var(--mono);
  font-size: 0.8rem;
  color: var(--amber);
  background: rgba(255,184,0,0.08);
  border: 1px solid rgba(255,184,0,0.3);
  padding: 2px 10px;
  border-radius: var(--radius);
}

.btn-register {
  border: 1px solid var(--green) !important;
  color: var(--green) !important;
  padding: 4px 14px !important;
  border-radius: var(--radius) !important;
}

.btn-register:hover { background: rgba(0,255,157,0.08) !important; }

/* ---- MESSAGES ---- */
.messages { padding: 0.5rem 2rem; background: var(--bg2); }
.message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  margin-bottom: 4px;
  border-radius: var(--radius);
  font-family: var(--mono);
  font-size: 0.85rem;
  border-left: 3px solid;
}
.message-success { border-color: var(--green); background: rgba(0,255,157,0.06); color: var(--green); }
.message-error    { border-color: var(--red);   background: rgba(255,68,68,0.06);   color: var(--red); }
.message-info     { border-color: var(--cyan);  background: rgba(0,212,255,0.06);   color: var(--cyan); }
.msg-prefix { color: var(--text-dim); }
.msg-close  { margin-left: auto; background: none; border: none; color: inherit; cursor: pointer; font-size: 1rem; }

/* ---- MAIN ---- */
.main-content { flex: 1; padding: 2rem; max-width: 1280px; margin: 0 auto; width: 100%; }

/* ---- HOME ---- */
.home-hero {
  text-align: center;
  padding: 5rem 1rem;
}
.home-hero .glitch {
  font-family: var(--mono);
  font-size: clamp(2rem, 6vw, 4rem);
  color: var(--green);
  letter-spacing: 4px;
  display: block;
  margin-bottom: 1rem;
  text-shadow: 0 0 20px rgba(0,255,157,0.4);
}
.home-hero p {
  color: var(--text-dim);
  font-family: var(--mono);
  font-size: 1rem;
  margin-bottom: 2.5rem;
  letter-spacing: 1px;
}
.hero-btns { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }

/* ---- BUTTONS ---- */
.btn {
  display: inline-block;
  padding: 10px 28px;
  border-radius: var(--radius);
  font-family: var(--mono);
  font-size: 0.9rem;
  letter-spacing: 1px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
  border: 1px solid;
}
.btn-primary   { background: var(--green); color: var(--bg); border-color: var(--green); font-weight: 700; }
.btn-primary:hover { background: var(--green-dim); box-shadow: 0 0 16px rgba(0,255,157,0.3); }
.btn-outline   { background: transparent; color: var(--green); border-color: var(--green); }
.btn-outline:hover { background: rgba(0,255,157,0.08); }
.btn-danger    { background: transparent; color: var(--red); border-color: var(--red); }
.btn-danger:hover { background: rgba(255,68,68,0.08); }

/* ---- CARDS ---- */
.card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
}
.card:hover { border-color: var(--border-glow); }

/* ---- CHALLENGE LIST ---- */
.challenge-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.challenge-header h1 {
  font-family: var(--mono);
  color: var(--green);
  font-size: 1.4rem;
  letter-spacing: 2px;
}

.progress-summary {
  font-family: var(--mono);
  color: var(--text-dim);
  font-size: 0.85rem;
}

.progress-summary span { color: var(--green); }

.category-section { margin-bottom: 2.5rem; }

.category-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}

.category-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.category-title h2 {
  font-family: var(--mono);
  font-size: 0.95rem;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.category-progress {
  margin-left: auto;
  font-family: var(--mono);
  font-size: 0.8rem;
  color: var(--text-dim);
}

.challenges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
}

.challenge-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  cursor: pointer;
  text-decoration: none;
  display: block;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}

.challenge-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 3px; height: 100%;
  background: var(--card-color, var(--green));
  opacity: 0.6;
}

.challenge-card:hover {
  border-color: var(--card-color, var(--green));
  background: var(--bg3);
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

.challenge-card.solved {
  opacity: 0.6;
  border-color: rgba(0,255,157,0.2);
}

.challenge-card.solved::before { background: var(--green); opacity: 1; }

.card-title {
  font-family: var(--sans);
  font-weight: 600;
  font-size: 1rem;
  color: var(--text);
  margin-bottom: 0.5rem;
  padding-left: 0.75rem;
}

.card-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-left: 0.75rem;
}

.card-pts {
  font-family: var(--mono);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--amber);
}

.card-diff {
  font-family: var(--mono);
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 2px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.diff-easy   { color: var(--green);  background: rgba(0,255,157,0.08);  border: 1px solid rgba(0,255,157,0.2); }
.diff-medium { color: var(--amber);  background: rgba(255,184,0,0.08);  border: 1px solid rgba(255,184,0,0.2); }
.diff-hard   { color: var(--red);    background: rgba(255,68,68,0.08);  border: 1px solid rgba(255,68,68,0.2); }

.card-solves {
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--text-muted);
  padding-left: 0.75rem;
  margin-top: 0.5rem;
}

.solved-badge {
  position: absolute;
  top: 0.6rem; right: 0.6rem;
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--green);
  background: rgba(0,255,157,0.1);
  border: 1px solid rgba(0,255,157,0.3);
  padding: 1px 6px;
  border-radius: 2px;
  letter-spacing: 1px;
}

/* ---- CHALLENGE DETAIL ---- */
.detail-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 2rem;
  align-items: start;
}

@media (max-width: 900px) { .detail-layout { grid-template-columns: 1fr; } }

.detail-main {}
.detail-sidebar {}

.detail-header {
  margin-bottom: 1.5rem;
}

.detail-header h1 {
  font-family: var(--sans);
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.75rem;
}

.detail-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.tag {
  font-family: var(--mono);
  font-size: 0.75rem;
  padding: 3px 10px;
  border-radius: 2px;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.tag-category { border: 1px solid; }
.tag-pts { color: var(--amber); background: rgba(255,184,0,0.08); border: 1px solid rgba(255,184,0,0.2); }
.tag-solves { color: var(--text-dim); background: var(--bg3); border: 1px solid var(--border); }

.detail-description {
  font-family: var(--sans);
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text);
  margin-bottom: 1.5rem;
  white-space: pre-wrap;
}

.detail-description code {
  font-family: var(--mono);
  background: var(--bg3);
  padding: 2px 6px;
  border-radius: var(--radius);
  color: var(--cyan);
  font-size: 0.9rem;
}

.connection-box {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-left: 3px solid var(--cyan);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
}

.connection-box label {
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--cyan);
  letter-spacing: 1px;
  display: block;
  margin-bottom: 0.4rem;
  text-transform: uppercase;
}

.connection-box code {
  font-family: var(--mono);
  color: var(--text);
  font-size: 0.95rem;
}

/* Flag submit */
.submit-box {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.submit-box h3 {
  font-family: var(--mono);
  color: var(--green);
  font-size: 0.9rem;
  letter-spacing: 2px;
  margin-bottom: 1rem;
}

.flag-input-row {
  display: flex;
  gap: 0.5rem;
}

.flag-input {
  flex: 1;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 10px 14px;
  color: var(--green);
  font-family: var(--mono);
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.flag-input:focus { border-color: var(--green); box-shadow: 0 0 8px rgba(0,255,157,0.1); }
.flag-input::placeholder { color: var(--text-muted); }

.submit-result {
  margin-top: 0.75rem;
  font-family: var(--mono);
  font-size: 0.9rem;
  min-height: 24px;
  padding: 6px 10px;
  border-radius: var(--radius);
}

.result-correct { color: var(--green); background: rgba(0,255,157,0.07); border-left: 2px solid var(--green); }
.result-wrong   { color: var(--red);   background: rgba(255,68,68,0.07);   border-left: 2px solid var(--red); }
.result-info    { color: var(--amber); background: rgba(255,184,0,0.07);   border-left: 2px solid var(--amber); }

.solved-banner {
  background: rgba(0,255,157,0.05);
  border: 1px solid rgba(0,255,157,0.3);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-align: center;
  font-family: var(--mono);
  color: var(--green);
  margin-bottom: 1rem;
}

/* Hints */
.hints-box {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
}

.hints-box h3 {
  font-family: var(--mono);
  font-size: 0.85rem;
  color: var(--text-dim);
  letter-spacing: 2px;
  margin-bottom: 1rem;
  text-transform: uppercase;
}

.hint-item {
  margin-bottom: 0.5rem;
  background: var(--bg3);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  overflow: hidden;
  transition: border-color 0.2s;
}

.hint-item:hover { border-color: rgba(255,184,0,0.3); }

.hint-toggle {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.7rem 1rem;
  cursor: pointer;
  user-select: none;
}

.hint-arrow {
  font-size: 0.65rem;
  color: var(--amber);
  transition: transform 0.2s ease;
  display: inline-block;
}

.hint-label {
  font-family: var(--mono);
  font-size: 0.82rem;
  color: var(--text-dim);
  letter-spacing: 1px;
}

.hint-toggle:hover .hint-label { color: var(--amber); }

.hint-body {
  max-height: 0px;
  opacity: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, opacity 0.25s ease;
  padding: 0 1rem;
}

.hint-text {
  font-family: var(--mono);
  font-size: 0.85rem;
  color: var(--amber);
  line-height: 1.6;
  padding-top: 0.5rem;
  border-top: 1px solid var(--border);
}

/* ---- SCOREBOARD ---- */
.scoreboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.scoreboard-header h1 {
  font-family: var(--mono);
  color: var(--green);
  font-size: 1.4rem;
  letter-spacing: 2px;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--mono);
  font-size: 0.8rem;
  color: var(--text-dim);
}

.live-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--green);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(0,255,157,0.4); }
  50% { opacity: 0.6; box-shadow: 0 0 0 6px rgba(0,255,157,0); }
}

.scoreboard-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--mono);
}

.scoreboard-table th {
  text-align: left;
  font-size: 0.75rem;
  color: var(--text-muted);
  letter-spacing: 2px;
  text-transform: uppercase;
  padding: 0.6rem 1rem;
  border-bottom: 1px solid var(--border);
}

.scoreboard-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  font-size: 0.9rem;
  transition: background 0.15s;
}

.scoreboard-table tr:hover td { background: var(--bg3); }

.rank-cell {
  color: var(--text-muted);
  width: 60px;
  font-size: 0.85rem;
}

.rank-1 { color: #ffd700; }
.rank-2 { color: #c0c0c0; }
.rank-3 { color: #cd7f32; }

.username-cell a {
  color: var(--cyan);
  text-decoration: none;
  font-weight: 600;
}
.username-cell a:hover { color: var(--green); }

.username-cell.is-you a { color: var(--green); }
.you-badge {
  font-size: 0.65rem;
  color: var(--green);
  background: rgba(0,255,157,0.1);
  border: 1px solid rgba(0,255,157,0.3);
  padding: 1px 6px;
  border-radius: 2px;
  margin-left: 6px;
}

.score-cell {
  color: var(--amber);
  font-weight: 700;
  font-size: 1rem;
}

.country-cell { color: var(--text-dim); font-size: 0.8rem; }
.affil-cell   { color: var(--text-dim); font-size: 0.8rem; }

/* ---- AUTH FORMS ---- */
.auth-container {
  max-width: 440px;
  margin: 4rem auto;
}

.auth-title {
  font-family: var(--mono);
  color: var(--green);
  font-size: 1.3rem;
  letter-spacing: 3px;
  margin-bottom: 0.5rem;
  text-align: center;
}

.auth-subtitle {
  font-family: var(--mono);
  color: var(--text-muted);
  font-size: 0.8rem;
  text-align: center;
  margin-bottom: 2rem;
}

.auth-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-family: var(--mono);
  font-size: 0.8rem;
  color: var(--text-dim);
  letter-spacing: 1px;
  margin-bottom: 0.4rem;
  text-transform: uppercase;
}

.form-input {
  width: 100%;
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 10px 14px;
  color: var(--text);
  font-family: var(--mono);
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus { border-color: var(--green); }

.form-errors {
  font-family: var(--mono);
  font-size: 0.8rem;
  color: var(--red);
  margin-top: 0.3rem;
}

.form-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-family: var(--mono);
  font-size: 0.85rem;
  color: var(--text-dim);
}

.form-footer a { color: var(--green); text-decoration: none; }

/* ---- PASSWORD SHOW/HIDE TOGGLE ---- */
.password-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-wrapper .form-input {
  padding-right: 44px;
}

.toggle-pw {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 4px;
  display: flex;
  align-items: center;
  transition: color 0.2s;
  outline: none;
}

.toggle-pw:hover { color: var(--green); }

/* ---- PROFILE ---- */
.profile-header {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
}

.profile-avatar {
  width: 80px; height: 80px;
  border-radius: var(--radius-lg);
  background: var(--bg3);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--mono);
  font-size: 2rem;
  color: var(--green);
  flex-shrink: 0;
  overflow: hidden;
}
.profile-avatar img { width: 100%; height: 100%; object-fit: cover; }

.profile-info h1 {
  font-family: var(--mono);
  font-size: 1.5rem;
  color: var(--green);
  letter-spacing: 2px;
  margin-bottom: 0.3rem;
}

.profile-meta {
  font-family: var(--mono);
  font-size: 0.8rem;
  color: var(--text-dim);
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.5rem;
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  text-align: center;
}

.stat-value {
  font-family: var(--mono);
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--green);
  display: block;
}

.stat-label {
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--text-muted);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-top: 0.3rem;
  display: block;
}

/* ---- FOOTER ---- */
.footer {
  padding: 1rem 2rem;
  border-top: 1px solid var(--border);
  text-align: center;
  font-family: var(--mono);
  font-size: 0.78rem;
  color: var(--text-muted);
}
.footer .green { color: var(--green); }

/* ---- UTILITIES ---- */
.green { color: var(--green); }
.cyan  { color: var(--cyan); }
.amber { color: var(--amber); }
.red   { color: var(--red); }
.mono  { font-family: var(--mono); }

.section-title {
  font-family: var(--mono);
  font-size: 0.85rem;
  color: var(--text-muted);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}

.text-center { text-align: center; }
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }

/* Solve history table */
.solves-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--mono);
  font-size: 0.85rem;
}
.solves-table th {
  text-align: left;
  color: var(--text-muted);
  font-size: 0.75rem;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid var(--border);
}
.solves-table td {
  padding: 0.6rem 0.75rem;
  border-bottom: 1px solid var(--border);
  color: var(--text-dim);
}
.solves-table td a { color: var(--cyan); text-decoration: none; }
.solves-table td a:hover { color: var(--green); }

/* ============================================================
   FLAG SUBMISSION  — handles the form on challenge detail page
   ============================================================ */
(function () {
  const form = document.getElementById('flag-form');
  if (!form) return;

  const input     = document.getElementById('flag-input');
  const resultBox = document.getElementById('submit-result');
  const btn       = document.getElementById('flag-submit-btn');
  const url       = form.dataset.url;
  const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const flag = input.value.trim();
    if (!flag) {
      showResult('error', '⚠ Flag cannot be empty.');
      return;
    }

    btn.disabled    = true;
    btn.textContent = 'checking…';
    resultBox.className = 'submit-result';
    resultBox.textContent = '';

    try {
      const res  = await fetch(url, {
        method:  'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken':  csrfToken,
        },
        body: JSON.stringify({ flag }),
      });

      const data = await res.json();

      switch (data.status) {
        case 'correct':
          showResult('correct', '✔ ' + data.message);
          input.disabled = true;
          btn.disabled   = true;
          btn.textContent = 'solved';
          // Reload after short delay so solved-banner shows
          setTimeout(() => location.reload(), 1800);
          break;

        case 'wrong':
          showResult('wrong', '✘ ' + data.message);
          input.select();
          btn.disabled    = false;
          btn.textContent = 'submit';
          break;

        case 'already_solved':
          showResult('correct', '★ ' + data.message);
          btn.disabled    = false;
          btn.textContent = 'submit';
          break;

        case 'rate_limited':
        case 'cooldown':
        case 'max_attempts':
          showResult('error', '⚠ ' + data.message);
          btn.disabled    = false;
          btn.textContent = 'submit';
          break;

        default:
          showResult('error', '⚠ ' + (data.message || 'Unexpected error.'));
          btn.disabled    = false;
          btn.textContent = 'submit';
      }
    } catch (err) {
      showResult('error', '⚠ Network error — please try again.');
      btn.disabled    = false;
      btn.textContent = 'submit';
    }
  });

  function showResult(type, msg) {
    resultBox.textContent  = msg;
    resultBox.className    = 'submit-result result-' + type;
    resultBox.style.display = 'block';
  }
})();


/* ============================================================
   SUBMIT RESULT STATE STYLES  (appended alongside JS above)
   ============================================================ */
