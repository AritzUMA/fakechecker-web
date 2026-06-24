#!/usr/bin/env python3
"""
build_site.py — corre en GitHub Actions.
Lee verdicts.json y genera index.html con estetica vintage de los 2000.
Sin frameworks, sin dependencias. HTML + CSS inline puro.
"""
import json
import html
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = json.loads((BASE / "verdicts.json").read_text(encoding="utf-8")) if (BASE / "verdicts.json").exists() else {"stats": {}, "verdicts": []}
if isinstance(DATA, list):
    stats = {}
    verdicts = DATA
else:
    stats = DATA.get("stats", {})
    verdicts = DATA.get("verdicts", [])
    if not verdicts:
        for k, v in DATA.items():
            if k != "stats" and isinstance(v, list):
                verdicts = v
                break

# colores chillones por veredicto, estilo terminal 2000
VERDICT_STYLE = {
    "supported":                ("#00FF00", "#003300", "VERDADERO"),
    "contradicted":             ("#FF3333", "#330000", "FALSO"),
    "misleading_or_exaggerated":("#FFCC00", "#332b00", "ENGAÑOSO"),
    "outdated":                 ("#FF9900", "#331f00", "DESACTUALIZADO"),
    "insufficient_evidence":    ("#999999", "#1a1a1a", "SIN EVIDENCIA"),
    "_default":                  ("#999999", "#1a1a1a", "OTRO"),
    "La afirmación es falsa.":   ("#ff3b3b", "#1a0000", "FALSO"),
}

def esc(s):
    return html.escape(str(s or ""))

filas = []
for v in verdicts:
    color, bg, etiqueta = VERDICT_STYLE.get(v["verdict"], ("#CCCCCC", "#222", v["verdict"]))
    outlets = ", ".join(v.get("outlets", [])) or "&mdash;"
    conf_pct = int(float(v.get("confidence", 0)) * 100)
    filas.append(f"""
    <tr>
      <td class="tw">{esc(v['tweet'])[:280]}</td>
      <td class="vd"><span style="color:{color};background:{bg};">&#9658; {etiqueta}</span></td>
      <td class="cf">{conf_pct}%</td>
      <td class="rs">{esc(v['reasoning'])[:220]}</td>
      <td class="ou">{esc(outlets)}</td>
      <td class="fc">{esc(v['fecha'])}</td>
    </tr>""")

filas_html = "\n".join(filas) if filas else '<tr><td colspan="6" style="text-align:center;padding:40px;">Aún no hay verificaciones. El robot está trabajando...</td></tr>'

html_out = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>:: FAKECHECKER :: Verificador de Bulos ::</title>
<style>
  body {{
    background:#000080;
    color:#C0C0C0;
    font-family:"Courier New",Courier,monospace;
    margin:0; padding:0;
    background-image:repeating-linear-gradient(0deg,#000080,#000080 2px,#00007a 2px,#00007a 4px);
  }}
  .frame {{ max-width:980px; margin:0 auto; padding:8px; }}
  .titlebar {{
    background:linear-gradient(90deg,#000080,#1084d0);
    color:#fff; font-weight:bold; padding:4px 8px;
    border:2px outset #fff; font-size:14px;
  }}
  .panel {{ background:#C0C0C0; color:#000; border:2px outset #fff; padding:10px; margin-top:6px; }}
  h1 {{
    font-family:"Impact","Arial Black",sans-serif; color:#FF00FF;
    text-shadow:2px 2px #00FFFF; text-align:center; font-size:34px;
    margin:6px 0; letter-spacing:1px;
  }}
  marquee {{ background:#000; color:#00FF00; border:1px inset #808080; padding:3px; font-size:13px; }}
  .stats {{ text-align:center; margin:8px 0; }}
  .stats b {{ font-size:20px; }}
  .badge {{ display:inline-block; padding:3px 8px; margin:3px; border:2px outset #fff; font-weight:bold; font-size:13px; }}
  table {{ width:100%; border-collapse:collapse; background:#fff; color:#000; font-size:12px; }}
  th {{ background:#000080; color:#fff; padding:5px; border:1px solid #000; text-align:left; }}
  td {{ padding:5px; border:1px solid #999; vertical-align:top; }}
  tr:nth-child(even) {{ background:#E0E0E0; }}
  .tw {{ width:28%; font-style:italic; }}
  .vd span {{ padding:2px 6px; font-weight:bold; white-space:nowrap; }}
  .cf {{ text-align:center; font-weight:bold; }}
  .rs {{ width:26%; font-size:11px; }}
  .ou {{ font-size:11px; color:#000080; }}
  .fc {{ font-size:10px; color:#555; white-space:nowrap; }}
  .footer {{ text-align:center; font-size:11px; color:#fff; margin:10px 0; }}
  a {{ color:#FFFF00; }}
  .counter {{ background:#000; color:#0F0; font-family:monospace; padding:2px 6px; border:1px inset #888; }}
</style>
</head>
<body>
<div class="frame">

  <div class="titlebar">&#128279; C:\\WINDOWS\\fakechecker.exe &mdash; Verificador Automático de Bulos</div>

  <div class="panel">
    <h1>~ FAKECHECKER ~</h1>
    <marquee scrollamount="4">&#9888; Detectando desinformación en español las 24 horas &#9888; Sistema de verificación automática con IA &#9888; Proyecto de investigación &mdash; Universidad de Málaga &#9888; Los tweets están anonimizados &#9888;</marquee>

    <div class="stats">
      <span class="badge" style="background:#C0C0C0;">VERIFICADOS: <b>{stats.get('total',0)}</b> / 2000</span>
      <span class="badge" style="background:#00FF00;">VERDADERO: {stats.get('supported',0)}</span>
      <span class="badge" style="background:#FF3333;color:#fff;">FALSO: {stats.get('contradicted',0)}</span>
      <span class="badge" style="background:#FFCC00;">ENGAÑOSO: {stats.get('misleading',0)}</span>
      <span class="badge" style="background:#999999;color:#fff;">SIN EVIDENCIA: {stats.get('insufficient',0)}</span>
    </div>
    <p style="text-align:center;font-size:11px;">
      Última actualización: <span class="counter">{esc(stats.get('actualizado','---'))}</span>
    </p>
  </div>

  <div class="panel" style="overflow-x:auto;">
    <table>
      <tr>
        <th>AFIRMACIÓN (tweet anonimizado)</th>
        <th>VEREDICTO</th>
        <th>CONF.</th>
        <th>RAZONAMIENTO</th>
        <th>FUENTES</th>
        <th>FECHA</th>
      </tr>
      {filas_html}
    </table>
  </div>

  <div class="footer">
    <p>&#9881; Generado automáticamente vía GitHub Actions &mdash; Mejor visto en Netscape Navigator 4.0 a 800&times;600 &#9881;</p>
    <p>&copy; 2026 Proyecto fakechecker &mdash; Los veredictos son automáticos y pueden contener errores.</p>
  </div>

</div>
</body>
</html>"""

(BASE / "index.html").write_text(html_out, encoding="utf-8")
print(f"✅ index.html generado con {len(verdicts)} veredictos")
