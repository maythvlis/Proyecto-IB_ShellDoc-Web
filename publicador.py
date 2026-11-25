#!/usr/bin/env python3
"""
publicador.py - Hilo 4 (funcionalidad extra) de ShellDoc Web.

Publica presentacion.html en GitHub Pages (rama gh-pages) usando git.
Este modulo NO crea semaforos: el coordinador le llama a publicar_sitio()
despues de haber hecho acquire() sobre el semaforo correspondiente.

Configuracion (variables de entorno):
  SHELLDOC_REPO_URL  URL del repositorio destino, p. ej.
                     https://github.com/USUARIO/shelldoc-web.git
                     (si no se define, se usa 'git remote get-url origin'
                     dentro de la carpeta del proyecto)
  GITHUB_TOKEN       Token personal (scope 'repo'). Opcional si ya hay SSH
                     o un credential helper configurado.

Uso independiente (prueba):  python3 publicador.py
"""
import os
import re
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HTML = "presentacion.html"
RECURSOS = ("presentacion_files", "site_libs")  # carpetas que deja renderizador.py
RAMA = "gh-pages"
TIMEOUT_GIT = 120


class PublicacionError(Exception):
    """Error controlado durante la publicacion."""


def log(msg):
    print(f"[{threading.current_thread().name}] {msg}", flush=True)


def _git(args, cwd, env=None):
    """Ejecuta git y devuelve stdout; lanza PublicacionError si falla."""
    try:
        r = subprocess.run(["git", *args], cwd=cwd, env=env, text=True,
                           capture_output=True, timeout=TIMEOUT_GIT)
    except subprocess.TimeoutExpired:
        raise PublicacionError(f"git {args[0]} excedio {TIMEOUT_GIT}s")
    if r.returncode != 0:
        # Nunca mostrar el token en los mensajes
        err = (r.stderr or r.stdout).strip()
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            err = err.replace(token, "***")
        raise PublicacionError(f"git {args[0]} fallo: {err}")
    return r.stdout.strip()


def _obtener_remoto(base):
    url = os.environ.get("SHELLDOC_REPO_URL")
    if not url:
        try:
            url = _git(["remote", "get-url", "origin"], cwd=base)
        except PublicacionError:
            raise PublicacionError(
                "No hay repositorio destino: define SHELLDOC_REPO_URL "
                "o configura 'git remote add origin ...'")
    return url


def _url_con_token(url):
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://"):
        return url.replace("https://", f"https://x-access-token:{token}@", 1)
    return url


def _url_publica(url):
    """Deduce https://USUARIO.github.io/REPO/ desde la URL del remoto."""
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?/?$", url)
    if not m:
        return None
    usuario, repo = m.groups()
    return f"https://{usuario}.github.io/{repo}/"


def verificar_prerequisitos(base):
    if shutil.which("git") is None:
        raise PublicacionError("git no esta instalado (sudo apt install git)")
    html = base / HTML
    if not html.is_file() or html.stat().st_size == 0:
        raise PublicacionError(f"{HTML} no existe o esta vacio: no se publica")


def publicar_sitio(base_dir=BASE_DIR):
    """
    Publica presentacion.html en GitHub Pages.
    Devuelve la URL publica (o None si no se pudo deducir).
    Lanza PublicacionError ante cualquier fallo.
    """
    base = Path(base_dir)
    log("Verificando prerrequisitos de publicacion...")
    verificar_prerequisitos(base)

    url_remoto = _obtener_remoto(base)
    url_push = _url_con_token(url_remoto)

    # Se arma el sitio en una carpeta temporal: nunca se toca el proyecto
    with tempfile.TemporaryDirectory(prefix="shelldoc_pages_") as tmp:
        sitio = Path(tmp)
        log("Preparando archivos del sitio (index.html + recursos)...")
        shutil.copy2(base / HTML, sitio / "index.html")
        for carpeta in RECURSOS:
            if (base / carpeta).is_dir():
                shutil.copytree(base / carpeta, sitio / carpeta)
        (sitio / ".nojekyll").touch()

        env = dict(os.environ, GIT_TERMINAL_PROMPT="0")  # nunca pedir clave
        _git(["init", "-q"], sitio, env)
        _git(["checkout", "-q", "-b", RAMA], sitio, env)
        _git(["add", "-A"], sitio, env)
        _git(["-c", "user.name=ShellDoc Bot",
              "-c", "user.email=shelldoc@localhost",
              "commit", "-q", "-m", "Publicacion automatica ShellDoc Web"],
             sitio, env)
        log(f"Enviando a la rama '{RAMA}' del repositorio...")
        _git(["push", "-q", "--force", url_push, f"{RAMA}:{RAMA}"], sitio, env)

    url_web = _url_publica(url_remoto)
    log(f"Publicacion completada. URL: {url_web or '(ver Settings > Pages)'}")
    return url_web


if __name__ == "__main__":
    threading.current_thread().name = "Hilo-4-Publicador"
    try:
        publicar_sitio()
    except PublicacionError as e:
        log(f"ERROR: {e}")
        raise SystemExit(1)
