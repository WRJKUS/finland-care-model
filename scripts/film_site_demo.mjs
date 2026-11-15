// Film a scripted Chrome agent using the live demo site for 15 s (CDP screencast), then encode film/paper/site_demo.mp4.
// The agent: picks Lapland, replays 2020 until the referral block turns dark (gap), reads the reason, opens the reasoning,
// opens the need (recommended action), copies the persistent link.
// Usage: node scripts/film_site_demo.mjs [url]   (no npm deps; Node >= 22; needs google-chrome and ffmpeg)
import { spawn, execFileSync } from 'node:child_process';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const URL0 = (process.argv[2] || 'https://equal-care-across-finland.vercel.app/') + '?county=14&t=2020-01';
const W = 1600, H = 900, DSF = 1.2, DUR = 15;      // 1600 px keeps the four pathway stages in one row; frames come out 1920 x 1080
const FR = mkdtempSync(path.join(tmpdir(), 'sitefilm-'));
const port = 9500 + Math.floor(Math.random() * 300);
const chrome = spawn('google-chrome', ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars', `--remote-debugging-port=${port}`, `--window-size=${W},${H}`,
  `--user-data-dir=${mkdtempSync(path.join(tmpdir(), 'sitefilm-prof-'))}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let tabs; for (let i = 0; i < 50; i++) { try { tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if (tabs.find(t => t.type === 'page')) break; } catch { } await sleep(200); }
const ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pend = new Map(), frames = [];
ws.onmessage = m => { const d = JSON.parse(m.data);
  if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); }
  if (d.method === 'Page.screencastFrame') { frames.push({ t: d.params.metadata.timestamp, data: d.params.data }); ws.send(JSON.stringify({ id: ++id, method: 'Page.screencastFrameAck', params: { sessionId: d.params.sessionId } })); } };
const cmd = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async e => (await cmd('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true })).result.result?.value;
await cmd('Page.enable');
await cmd('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: DSF, mobile: false });
await cmd('Page.navigate', { url: URL0 }); await sleep(3500);
// the agent's visible cursor, a click ripple and a small "agent" badge in the header
await ev(`(()=>{const c=document.createElement('div');c.id='agentc';c.style.cssText='position:fixed;left:820px;top:520px;width:30px;height:30px;z-index:99;pointer-events:none;transition:left .65s cubic-bezier(.4,0,.2,1),top .65s cubic-bezier(.4,0,.2,1)';
 c.innerHTML='<svg width="30" height="30" viewBox="0 0 24 24"><path d="M4 2l15 11-7 1-3 7z" fill="#fff" stroke="#1c2430" stroke-width="1.6" stroke-linejoin="round"/></svg>';document.body.appendChild(c);
 const b=document.createElement('div');b.style.cssText='position:fixed;left:345px;top:19px;z-index:99;background:#89CFF0;color:#0e3b5c;font:700 13px system-ui;padding:6px 14px;border-radius:999px';b.textContent='● Chrome agent · equal-care-across-finland.vercel.app';document.body.appendChild(b);
 window.__go=(el)=>{const r=el.getBoundingClientRect();const c=document.getElementById('agentc');c.style.left=(r.left+r.width/2-4)+'px';c.style.top=(r.top+r.height/2-4)+'px'};
 window.__tap=()=>{const c=document.getElementById('agentc');const p=document.createElement('div');p.style.cssText='position:fixed;z-index:98;pointer-events:none;border:3px solid #0e7c86;border-radius:50%;width:10px;height:10px;left:'+(parseFloat(c.style.left)-1)+'px;top:'+(parseFloat(c.style.top)-1)+'px;transition:all .45s ease-out;opacity:1';document.body.appendChild(p);requestAnimationFrame(()=>{p.style.width=p.style.height='48px';p.style.left=(parseFloat(c.style.left)-20)+'px';p.style.top=(parseFloat(c.style.top)-20)+'px';p.style.opacity=0});setTimeout(()=>p.remove(),600)};
})()`);
const go = async (sel, ms = 750) => { await ev(`__go(document.querySelector(${JSON.stringify(sel)}))`); await sleep(ms); };
const tap = async (sel, ms = 400) => { await ev(`__tap();(()=>{const e=document.querySelector(${JSON.stringify(sel)});e.dispatchEvent(new MouseEvent('click',{bubbles:true}))})()`); await sleep(ms); };
const REF = '.hb[data-sig="ref_assess_over90"]';
await cmd('Page.startScreencast', { format: 'jpeg', quality: 88, maxWidth: Math.round(W * DSF), maxHeight: Math.round(H * DSF), everyNthFrame: 1 });
const t0 = Date.now(); await sleep(500);
await go('#map path[data-c="21"]'); await tap('#map path[data-c="21"]', 450);                    // 1 pick Lapland
await go('#play'); await tap('#play', 0);                                                        // 2 replay 2020 ...
for (let i = 0; i < 120 && !(await ev(`D.months[S.t]>='2020-11'`)); i++) await sleep(40);        //   ... until the referral block has turned dark
await ev(`document.getElementById('play').click()`); await sleep(250);                           //   pause on the gap
await go(REF + ' .hwhy'); await sleep(1500);                                                     // 3 read "why a gap" in the block
await tap(REF + ' .hwhy', 2300);                                                                 // 4 open the full reasoning and history
await go('.hneed[data-open="act:ref_assess_over90"]'); await tap('.hneed[data-open="act:ref_assess_over90"]', 2300);   // 5 open the need: the recommended action
await go('#copy'); await tap('#copy', 900);                                                      // 6 a persistent link to exactly this view
while (Date.now() - t0 < DUR * 1000 + 300) await sleep(100);
await cmd('Page.stopScreencast'); await sleep(300);
const state = await ev(`location.search+' | '+D.months[S.t]`);
ws.close(); chrome.kill();
// constant-frame-rate encode from the screencast timestamps
const ts0 = frames[0].t, list = [];
frames.forEach((f, i) => { const n = `f${String(i).padStart(5, '0')}.jpg`; writeFileSync(path.join(FR, n), Buffer.from(f.data, 'base64')); list.push([n, f.t - ts0]); });
let concat = '';
list.forEach(([n, t], i) => { const next = i + 1 < list.length ? list[i + 1][1] : DUR; if (t >= DUR) return; concat += `file '${n}'\nduration ${Math.max(0.001, Math.min(next, DUR) - t).toFixed(3)}\n`; });
concat += `file '${list.filter(x => x[1] < DUR).pop()[0]}'\n`;
writeFileSync(path.join(FR, 'concat.txt'), concat);
const out = path.join(ROOT, 'film/paper/site_demo.mp4');
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(FR, 'concat.txt'), '-vf', 'fps=30,scale=1920:1080:flags=lanczos,format=yuv420p', '-t', String(DUR), '-c:v', 'libx264', '-crf', '20', '-movflags', '+faststart', out]);
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', '8.6', '-i', out, '-frames:v', '1', path.join(ROOT, 'film/paper/site_demo_poster.png')]);
console.log('frames', frames.length, '| final state', state, '→', out);
