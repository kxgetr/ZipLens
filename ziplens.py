"""Compare ZIP contents without extraction. Optionally export side-by-side image previews."""
import argparse,hashlib,json,zipfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument("old")
p.add_argument("new")
p.add_argument("--previews",type=Path)
a=p.parse_args()
def index(z):
    result={}
    for i in z.infolist():
        if i.is_dir(): continue
        if i.filename in result: p.error("duplicate member "+repr(i.filename))
        result[i.filename]=i
    return result
def digest(z,i):
    with z.open(i) as f: return hashlib.file_digest(f,"sha256").digest()
with zipfile.ZipFile(a.old) as old,zipfile.ZipFile(a.new) as new:
    left,right=index(old),index(new)
    rows=[]
    for path in sorted(left.keys()|right.keys()):
        kind="added" if path not in left else "removed" if path not in right else "changed"
        if kind=="changed" and left[path].file_size==right[path].file_size and digest(old,left[path])==digest(new,right[path]): continue
        row={"path":path,"status":kind}
        if a.previews and kind=="changed" and Path(path).suffix.lower() in {".png",".jpg",".jpeg",".webp",".gif"}:
            from PIL import Image
            canvas=Image.new("RGB",(800,400),"#292c35")
            try:
                for side,z in enumerate((old,new)):
                    with z.open(path) as stream,Image.open(stream) as im:
                        im.thumbnail((400,400))
                        canvas.paste(im.convert("RGB"),(side*400,0))
                a.previews.mkdir(exist_ok=True,parents=True)
                out=a.previews/(hashlib.sha256(path.encode()).hexdigest()+".png")
                canvas.save(out)
                row["preview"]=str(out)
            except (OSError,ValueError) as exc:
                row["preview_error"]=str(exc)
        rows.append(row)
    print(json.dumps(rows,indent=2))
