"""Builds the static GitHub Pages site (privacy policy, terms, support) for Butaca."""
import html, pathlib, re

ROOT = pathlib.Path(__file__).parent
LEGAL = ROOT.parent / "Butaca" / "Resources" / "Legal"
CONTACT_EMAIL = "angelsoatwork@gmail.com"
CONTACT_PHONE = "+52 248 128 4457"

HEAD = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="assets/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="wrap">
<header class="top">
  <a class="brand" href="index.html"><img src="assets/icon.png" alt="">BUTACA</a>
  <nav>
    <a href="privacidad.html"{p}>Privacidad</a>
    <a href="terminos.html"{t}>Términos</a>
    <a href="soporte.html"{s}>Soporte</a>
  </nav>
</header>
"""

FOOT = """<footer>
  <p>© 2026 Angel Sosa · Butaca</p>
  <p style="margin-top:8px">Datos e imágenes de películas por <a href="https://www.themoviedb.org">TMDB</a><img src="assets/tmdb.svg" alt="TMDB">.
  Esta app usa TMDB y las APIs de TMDB, pero no está respaldada, certificada ni aprobada por TMDB.
  Disponibilidad en plataformas por <a href="https://www.justwatch.com">JustWatch</a>.</p>
</footer>
</div>
</body>
</html>
"""


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    text = text.replace(CONTACT_EMAIL, f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>')
    return text


def markdown(md: str) -> str:
    out, in_list, list_tag = [], False, "ul"
    for raw in md.splitlines():
        line = raw.strip()
        bullet = re.match(r"^(- |\d+\. )(.*)", line)
        if bullet:
            tag = "ol" if bullet.group(1)[0].isdigit() else "ul"
            if not in_list:
                out.append(f"<{tag}>"); in_list, list_tag = True, tag
            out.append(f"<li>{inline(bullet.group(2))}</li>")
            continue
        if in_list:
            out.append(f"</{list_tag}>"); in_list = False
        if line.startswith("# "):
            out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("_") and line.endswith("_"):
            out.append(f'<p class="updated">{inline(line.strip("_"))}</p>')
        elif line:
            out.append(f"<p>{inline(line)}</p>")
    if in_list:
        out.append(f"</{list_tag}>")
    return "\n".join(out)


def page(name: str, title: str, description: str, body: str, current: str = ""):
    marks = {k: (' aria-current="page"' if current == k else "") for k in "pts"}
    (ROOT / name).write_text(HEAD.format(title=title, description=description, **marks) + body + FOOT, encoding="utf-8")


page("index.html", "Butaca · Qué ver en pareja", "Guarda películas y series, recibe recomendaciones y hagan match para elegir qué ver juntos.", """
<section class="hero">
  <p class="kicker">Tu banco de películas y series</p>
  <h1>BUTACA</h1>
  <p>Guarda lo que quieres ver, descubre recomendaciones a tu gusto y, en pareja, deslicen hasta que los dos digan que sí.</p>
  <div class="pills"><span class="pill">Guarda</span><span class="pill">Descubre</span><span class="pill">Haz match</span></div>
  <a class="btn" href="soporte.html">Soporte <span>Contacto</span></a>
</section>
<section class="grid">
  <div class="feature"><h3>Tu banco</h3><p>Películas y series por ver y vistas, con progreso y calificación. Funciona sin internet.</p></div>
  <div class="feature"><h3>Para ti</h3><p>Recomendaciones que aprenden de lo que guardas, calificas y deslizas.</p></div>
  <div class="feature"><h3>Modo pareja</h3><p>Conecten sus teléfonos en la misma red, deslicen hasta 100 títulos y hagan match.</p></div>
  <div class="feature"><h3>Dónde verla</h3><p>Plataformas disponibles en tu país, reparto, tráiler y títulos parecidos.</p></div>
</section>
""")

for name, source, title, current in [
    ("privacidad.html", "privacy.md", "Aviso de privacidad · Butaca", "p"),
    ("terminos.html", "terms.md", "Términos de uso · Butaca", "t"),
]:
    md = (LEGAL / source).read_text(encoding="utf-8")
    page(name, title, title, f"<article>\n{markdown(md)}\n</article>\n", current)

page("soporte.html", "Soporte · Butaca", "Ayuda y contacto de Butaca.", f"""
<article>
<h1>Soporte</h1>
<p class="updated">Te respondemos lo antes posible.</p>
<div class="card">
  <h2 style="margin-top:0">Contacto</h2>
  <p><strong>Angel Sosa</strong></p>
  <p>Correo: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
  <p>Teléfono / WhatsApp: <a href="tel:+522481284457">{CONTACT_PHONE}</a></p>
</div>
<h2>Preguntas frecuentes</h2>
<p><strong>¿Necesito una cuenta?</strong> No. Puedes usar Butaca sin cuenta; iniciar sesión con Apple solo sirve para tener tu banco en todos tus dispositivos.</p>
<p><strong>¿Cómo funciona el modo pareja?</strong> Ambos abren Butaca → corazón → uno crea la sala y el otro se une estando en la misma red Wi‑Fi (o cerca por Bluetooth). Acepten el permiso de Red local.</p>
<p><strong>No encuentro la sala de mi pareja.</strong> Verifiquen que estén en la misma red y que Butaca tenga permiso en Ajustes → Privacidad → Red local.</p>
<p><strong>¿Cómo elimino mi cuenta o mis datos?</strong> En la app: avatar → Mi perfil → Cuenta → Eliminar cuenta (o "Borrar mis datos de la nube" si no iniciaste sesión).</p>
<p><strong>¿De dónde salen los datos de las películas?</strong> De TMDB; la disponibilidad en plataformas, de JustWatch.</p>
</article>
""", "s")
print("site built")
