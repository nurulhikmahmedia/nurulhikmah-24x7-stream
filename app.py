import os, subprocess, signal
from flask import Flask, redirect
app=Flask(__name__)
proc=None
def running(): return proc is not None and proc.poll() is None
@app.get("/")
def home():
    s="🔴 STREAMING" if running() else "● OFFLINE"
    return f"""<meta name=viewport content="width=device-width,initial-scale=1"><style>body{{font-family:Arial;background:#f4f6fa;padding:25px}}.c{{max-width:600px;margin:auto;background:white;padding:25px;border-radius:15px}}button{{width:100%;padding:16px;margin:8px 0;border:0;border-radius:9px;color:white;font-weight:bold;font-size:17px}}</style><div class=c><h1>Nurul Hikmah 24/7</h1><h2>{s}</h2><form method=post action=/start><button style="background:#07884d">▶ MULAI STREAM</button></form><form method=post action=/stop><button style="background:#c62828">■ STOP STREAM</button></form></div>"""
@app.post("/start")
def start():
    global proc
    if not running():
        v=os.environ.get("VIDEO_URL","").strip(); k=os.environ.get("YOUTUBE_STREAM_KEY","").strip()
        if v and k:
            proc=subprocess.Popen(["ffmpeg","-re","-stream_loop","-1","-i",v,"-vf","scale=-2:720,fps=30","-c:v","libx264","-preset","veryfast","-b:v","2500k","-maxrate","2500k","-bufsize","5000k","-g","60","-c:a","aac","-b:a","128k","-f","flv",f"rtmps://a.rtmps.youtube.com/live2/{k}"])
    return redirect("/")
@app.post("/stop")
def stop():
    global proc
    if running(): proc.send_signal(signal.SIGTERM)
    proc=None
    return redirect("/")
@app.get("/health")
def health(): return {"web":"ok","streaming":running()}
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT","10000")))
