"""Apaga os nomes das peças nas imagens originais (assets/revolver.png, assets/pistola.png),
recorta e grava assets/*-lacunas.png + assets/partes.json com a posição de cada lacuna.
Uso: python prep_images.py"""
import json, pathlib
from PIL import Image, ImageDraw

root = pathlib.Path(__file__).parent / "assets"

# (nome, área a apagar na imagem original, lacuna exibida na imagem original)
ARMAS = {
  "revolver": {
    "titulo": "Revólver", "arquivo": "revolver.png", "recorte": (55, 100, 545, 470), "cinza": True,
    "pecas": [
      ("Massa de mira",       (116,114,207,132), (116,112,207,134)),
      ("Tambor",              (245,112,290,130), (225,110,292,132)),
      ("Alça de mira",        (452,114,528,132), (452,112,530,134)),
      ("Cano",                (159,145,193,163), (129,143,193,165)),
      ("Dedal serrilhado",    (422,145,520,163), (422,143,530,165)),
      ("Cão",                 (456,174,488,191), (456,172,520,193)),
      ("Boca do cano",        (115,267,199,285), (115,265,198,287)),
      ("Vareta do extrator",  (66,301,173,319),  (62,299,173,321)),
      ("Guarda-mato",         (108,336,191,354), (98,334,191,356)),
      ("Gatilho",             (187,371,233,389), (165,369,233,391)),
      ("Cabo",                (127,408,166,425), (102,406,166,428)),
    ],
  },
  "pistola": {
    "titulo": "Pistola", "arquivo": "pistola.png", "recorte": (26, 56, 536, 334), "cinza": False,
    "pecas": [
      ("Slide (ferrolho)",                         (108,64,207,90)),
      ("Alça de mira",                             (211,64,300,90)),
      ("Registro de segurança e desarmador do cão",(309,64,526,90)),
      ("Massa de mira",                            (37,95,126,121)),
      ("Cão",                                      (480,99,526,127)),
      ("Cano",                                     (37,143,84,169)),
      ("Cabo",                                     (480,164,526,193)),
      ("Alavanca de desmontagem",                  (37,188,180,214)),
      ("Retém do ferrolho",                        (37,226,144,252)),
      ("Gatilho",                                  (37,261,91,290)),
      ("Guarda-mato",                              (181,295,261,325)),
      ("Retém do carregador",                      (268,295,387,325)),
      ("Carregador",                               (392,295,464,325)),
    ],
  },
}

out = {}
for key, a in ARMAS.items():
    src = Image.open(root / a["arquivo"]).convert("RGBA")
    img = Image.new("RGBA", src.size, (255, 255, 255, 255)); img.alpha_composite(src)
    img = img.convert("RGB"); d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = a["recorte"]; W, H = x1 - x0, y1 - y0
    zonas = []
    for i, p in enumerate(a["pecas"]):
        nome, apagar = p[0], p[1]
        lac = p[2] if len(p) > 2 else apagar
        d.rectangle(apagar, fill=(255, 255, 255))
        zonas.append({"id": f"{key}-{i}", "nome": nome,
                      "x": round((lac[0] - x0) / W * 100, 3), "y": round((lac[1] - y0) / H * 100, 3),
                      "w": round((lac[2] - lac[0]) / W * 100, 3), "h": round((lac[3] - lac[1]) / H * 100, 3)})
    img = img.crop(a["recorte"])
    img = img.convert("L") if a["cinza"] else img.quantize(48)
    nome_arq = f"{key}-lacunas.png"
    img.save(root / nome_arq, optimize=True)
    out[key] = {"titulo": a["titulo"], "img": nome_arq, "w": W, "h": H, "zonas": zonas}
(root / "partes.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print({k: len(v["zonas"]) for k, v in out.items()})
