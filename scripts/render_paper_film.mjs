// Render film/paper/presentation.html to film/paper/paper_film.mp4, frame by frame over the Chrome DevTools Protocol (no npm deps; Node >= 22).
// Env PAGE / OUTFILE pick another page (e.g. film/paper/county_twin.html -> film/paper/county_twin_21.mp4).
// Usage: node scripts/render_paper_film.mjs [fps=30] [stills: t1,t2,...]
import { spawn } from 'node:child_process';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const fps = +(process.argv[2] || 30), stills = process.argv[3] ? process.argv[3].split(',').map(Number) : null;
const port = 9300 + Math.floor(Math.random() * 500);
const chrome = spawn('google-chrome', ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars', `--remote-debugging-port=${port}`, '--window-size=1920,1080',
  `--user-data-dir=${mkdtempSync(path.join(tmpdir(), 'pfilm-'))}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let tabs; for (let i = 0; i < 50; i++) { try { tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if (tabs.find(t => t.type === 'page')) break; } catch { } await sleep(200); }
const ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const pend = new Map(); ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } };
const cmd = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
await cmd('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
await cmd('Page.enable');
await cmd('Page.navigate', { url: 'file://' + path.join(ROOT, process.env.PAGE || 'film/paper/presentation.html') + '?capture=1' });
await sleep(1500);
await cmd('Runtime.evaluate', { expression: 'document.fonts.ready.then(()=>1)', awaitPromise: true });
const dur = (await cmd('Runtime.evaluate', { expression: 'DURATION', returnByValue: true })).result.result.value;
const frame = async t => { await cmd('Runtime.evaluate', { expression: `render(${t})` });
  const r = await cmd('Runtime.evaluate', { expression: `document.getElementById('c').toDataURL('image/png')`, returnByValue: true });
  return Buffer.from(r.result.result.value.split(',')[1], 'base64'); };
if (stills) {
  const fs = await import('node:fs');
  for (const t of stills) fs.writeFileSync(path.join(process.env.OUT || '/tmp', `still_${t}.png`), await frame(t));
} else {
  const out = path.join(ROOT, process.env.OUTFILE || 'film/paper/paper_film.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.round(dur * fps);
  for (let k = 0; k < N; k++) { const b = await frame(k / fps); if (!ff.stdin.write(b)) await new Promise(r => ff.stdin.once('drain', r)); if (k % 300 === 0) console.log('frame', k, '/', N); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log('wrote', out, dur, 's');
}
ws.close(); chrome.kill();
