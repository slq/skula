"""Package the Windows application and corresponding source, without local data.

Run from skula-app: python tools/prepare_release.py
The ZIP contains source, bundled icons, screenshots, licenses and launchers.
Python and pip are still required on the target computer.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import zipfile

project = Path(__file__).resolve().parents[1]
repo = project.parent
version_source = (project / "skula_app/__init__.py").read_text(encoding="utf-8-sig")
match = re.search(r'__version__\s*=\s*"(\d+\.\d+\.\d+)"', version_source)
if not match:
    raise SystemExit("Could not identify the desktop version")
version = match.group(1)
name = f"Skula-windows-{version}"
out_dir = project / "dist"
out_dir.mkdir(exist_ok=True)
archive = out_dir / f"{name}.zip"
listing = subprocess.run(
    ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", "skula-app"],
    cwd=repo, capture_output=True, text=True, encoding="utf-8", check=True
).stdout.splitlines()
allowed_roots = {"skula_app", "tests", "tools", "licenses", "docs"}
allowed_suffixes = {".py", ".md", ".cmd", ".txt", ".png", ".ini"}
files = []
for relative in sorted(set(listing)):
    path = repo / relative
    inner = path.relative_to(project)
    if not path.is_file() or path.is_symlink():
        continue
    if any(part in {".venv", "dist", "build", "__pycache__", ".pytest_cache", ".tools", ".git"} for part in inner.parts):
        continue
    if len(inner.parts) > 1 and inner.parts[0] not in allowed_roots:
        continue
    if path.name != "LICENSE" and path.suffix.lower() not in allowed_suffixes:
        continue
    files.append((path, inner.as_posix()))

required = {"Start.cmd", "Demo.cmd", "README.md", "LICENSE", "requirements.txt",
            "skula_app/__init__.py", "skula_app/theme.py", "skula_app/home_view.py",
            "skula_app/assets/brand.png", "docs/screenshots/start.png"}
if not required.issubset({inner for _, inner in files}):
    raise SystemExit("Incomplete application package")
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
    for path, inner in files:
        bundle.write(path, f"{name}/{inner}")
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix(".zip.sha256").write_text(f"{digest}  {archive.name}\n", encoding="ascii")
print(f"Desktop {version}: {len(files)} files, {archive.stat().st_size} bytes")
print(archive)
print(f"SHA256 {digest}")
