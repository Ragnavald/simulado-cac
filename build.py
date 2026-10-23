"""Gera o site a partir de template.html + questoes_cac.json + assets/partes.json.
Uso: python build.py   (rode antes python prep_images.py se mudar as imagens ou as lacunas)
Saídas: simulado-cac.html (versão para o Artifact) e site/index.html (página completa para hospedar)."""
import base64, json, pathlib
root = pathlib.Path(__file__).parent

def blob(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", r"<\/")

data = json.loads((root / "questoes_cac.json").read_text(encoding="utf-8"))
# questões complementares (questoes_complementares.json) entram no mesmo banco
extra = json.loads((root / "questoes_complementares.json").read_text(encoding="utf-8"))["questoes"]
data["questoes"] += extra
data["total"] = len(data["questoes"])
# grupos de questões sobre o mesmo assunto (assets/grupos.json)
ids = {q["id"] for q in data["questoes"]}
grupo_de = {}
for nome, membros in json.loads((root / "assets" / "grupos.json").read_text(encoding="utf-8")).items():
    if nome.startswith("_"):
        continue
    for qid in membros:
        assert qid in ids, f"grupos.json: {qid} não existe no banco"
        assert qid not in grupo_de, f"grupos.json: {qid} está em dois grupos"
        grupo_de[qid] = nome
for q in data["questoes"]:
    if q["id"] in grupo_de:
        q["grupo"] = grupo_de[q["id"]]

partes = json.loads((root / "assets" / "partes.json").read_text(encoding="utf-8"))
for arma in partes.values():
    png = (root / "assets" / arma["img"]).read_bytes()
    arma["img"] = "data:image/png;base64," + base64.b64encode(png).decode()

page = (root / "template.html").read_text(encoding="utf-8")
page = page.replace("/*__DATA__*/", blob(data)).replace("/*__PARTES__*/", blob(partes))
(root / "simulado-cac.html").write_text(page, encoding="utf-8")
(root / "site").mkdir(exist_ok=True)
full = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '</head>\n<body>\n' + page + '\n</body>\n</html>\n')
(root / "site" / "index.html").write_text(full, encoding="utf-8")
print(len(data["questoes"]), "questões,", sum(len(a["zonas"]) for a in partes.values()), "lacunas;", len(page.encode()), "bytes")
