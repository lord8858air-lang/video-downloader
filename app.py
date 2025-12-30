from flask import Flask, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Downloader Any Video & Audio</title>

<style>
body{margin:0;background:#081f22;font-family:Arial;color:#fff}
.container{max-width:420px;margin:20px auto;padding:14px}
.card{background:#0b2e32;border-radius:18px;padding:20px}
.control{
 width:100%;height:56px;padding:0 16px;
 border-radius:14px;border:none;
 margin-top:12px;font-size:15px;
 appearance:none;-webkit-appearance:none
}
select.control{
 background:#f1f1f1 url("data:image/svg+xml;utf8,<svg fill='black' height='24' viewBox='0 0 24 24' width='24'><path d='M7 10l5 5 5-5z'/></svg>") no-repeat right 16px center;
 background-size:18px
}
button.control{background:#00ff99;font-weight:700}
</style>
</head>

<body>
<div class="container">
<div class="card">
<h2>🎬 Video Downloader</h2>

<input id="url" class="control" placeholder="Paste video URL">

<select id="type" class="control" onchange="changeQ()">
<option value="video">Video</option>
<option value="audio">Audio</option>
</select>

<select id="quality" class="control">
<option>360</option><option>720</option><option>1080</option>
</select>

<button class="control" onclick="go()">Download</button>
</div>
</div>

<script>
function changeQ(){
 let q=document.getElementById("quality");
 q.innerHTML="";
 if(type.value=="audio"){
  ["64","128","192","320"].forEach(x=>q.innerHTML+=`<option>${x}</option>`);
 }else{
  ["144","360","720","1080"].forEach(x=>q.innerHTML+=`<option>${x}</option>`);
 }
}

function go(){
 fetch("/download",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({
   url:url.value,
   type:type.value,
   quality:quality.value
  })
 }).then(r=>r.blob()).then(b=>{
  let a=document.createElement("a");
  a.href=URL.createObjectURL(b);
  a.download="download";
  a.click();
 });
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    uid = str(uuid.uuid4())
    out = os.path.join(DOWNLOAD_DIR, uid)

    if data["type"] == "audio":
        ydl_opts = {
          "format":"bestaudio",
          "outtmpl":out+".%(ext)s",
          "postprocessors":[{
            "key":"FFmpegExtractAudio",
            "preferredcodec":"mp3",
            "preferredquality":data["quality"]
          }]
        }
    else:
        ydl_opts = {
          "format":f"bestvideo[height<={data['quality']}]+bestaudio/best",
          "outtmpl":out+".%(ext)s",
          "merge_output_format":"mp4"
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([data["url"]])

    file = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(uid)][0]
    return send_file(os.path.join(DOWNLOAD_DIR,file), as_attachment=True)

import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
