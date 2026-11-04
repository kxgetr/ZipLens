import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

SCRIPT = Path(__file__).with_name("ziplens.py")
def run(*args, ok=0):
    result = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
    assert result.returncode == ok, (args, result.stdout, result.stderr)
    return result

def git(*args):
    subprocess.run(["git", *args], check=True)

with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    from PIL import Image
    for color in ["red","blue"]:
        Image.new("RGB",(4,4),color).save("x.png")
        with zipfile.ZipFile(color+".zip","w") as z: z.write("x.png")
    row=json.loads(run("red.zip","blue.zip","--previews","imgs").stdout)[0]
    im=Image.open(row["preview"])
    assert im.getpixel((0,0))==(255,0,0) and im.getpixel((400,0))==(0,0,255)
