import os, re, pathlib, requests
from urllib.parse import urljoin

BASE = os.environ["YOUTRACK_URL"].rstrip("/")
H = {"Authorization": f"Bearer {os.environ['YOUTRACK_TOKEN']}", "Accept": "application/json"}
FIELDS = ("idReadable,summary,content,project(shortName),"
          "parentArticle(idReadable),attachments(name,url,size)")
MAX_SIZE = 95 * 1024 * 1024  # GitHub lehnt Dateien > 100 MB ab
out = pathlib.Path("kb")

def safe(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip() or "file"

def download(url: str, target: pathlib.Path):
    full = urljoin(BASE + "/", url)
    with requests.get(full, headers={"Authorization": H["Authorization"]},
                      stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(target, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)

skip, top = 0, 100
while True:
    r = requests.get(f"{BASE}/api/articles", headers=H,
                     params={"fields": FIELDS, "$skip": skip, "$top": top}, timeout=60)
    r.raise_for_status()
    batch = r.json()
    if not batch:
        break
    for a in batch:
        proj = a["project"]["shortName"]
        slug = re.sub(r"[^\w\-]+", "-", a["summary"]).strip("-")[:60]
        folder = out / proj / f"{a['idReadable']}-{slug}"
        folder.mkdir(parents=True, exist_ok=True)

        parent = (a.get("parentArticle") or {}).get("idReadable", "")
        (folder / "README.md").write_text(
            f"---\nid: {a['idReadable']}\nparent: {parent}\n---\n\n"
            f"# {a['summary']}\n\n{a.get('content') or ''}\n", encoding="utf-8")

        for att in a.get("attachments") or []:
            name = safe(att["name"])
            if (att.get("size") or 0) > MAX_SIZE:
                print(f"Übersprungen (zu groß): {a['idReadable']}/{name}")
                continue
            try:
                download(att["url"], folder / name)
            except requests.RequestException as e:
                print(f"Fehler bei {a['idReadable']}/{name}: {e}")
    skip += top