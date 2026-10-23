# Simulado CAC

Site de estudo para a prova teórica de capacidade técnica para manuseio de arma de fogo (CAC/PF). É uma página única, sem servidor: tudo roda no navegador e o progresso fica salvo no próprio navegador de cada pessoa.

O que o site tem:

- **Simulado da prova:** 20 questões na divisão do regulamento (6 de normas de segurança, 6 de nomenclatura e funcionamento, 5 de legislação, 3 de conduta no estande), aprovação com 12 acertos, gabarito comentado no fim.
- **Treino por tema:** escolha de temas, tipo e quantidade, com a explicação logo após cada resposta.
- **Revisar erros:** as questões erradas voltam até a pessoa acertar.
- **Partes da arma:** desenhos do revólver e da pistola para completar com o nome das peças.
- **Banco de questões:** consulta com busca e filtros.

## Como publicar

O site pronto é [`site/index.html`](site/index.html). Basta hospedar esse arquivo em qualquer lugar que sirva páginas estáticas (GitHub Pages, Netlify etc.) ou abri-lo direto no navegador.

## Como alterar

| Arquivo | O que é |
|---|---|
| `questoes_cac.json` | Banco original de questões |
| `questoes_complementares.json` | Questões complementares escritas para ampliar estande, segurança e legislação (revisar antes de divulgar) |
| `assets/grupos.json` | Questões que cobram o mesmo assunto; o sorteio usa no máximo uma de cada grupo por prova |
| `assets/revolver.png`, `assets/pistola.png` | Imagens originais dos desenhos |
| `prep_images.py` | Apaga os nomes das peças nas imagens e define onde fica cada lacuna |
| `template.html` | Layout, estilos e código do site |
| `build.py` | Junta tudo e gera o site |

Depois de mudar qualquer arquivo, gere o site de novo (precisa de Python 3; `prep_images.py` também precisa do Pillow):

```bash
python prep_images.py   # só se mudar as imagens ou as lacunas
python build.py
```

O `build.py` gera `site/index.html` e `simulado-cac.html` (a mesma página, sem o cabeçalho HTML, usada na publicação como Artifact do Claude).

## Aviso

Material de estudo independente, sem vínculo com a Polícia Federal. Confira sempre a legislação em vigor. Antes de tornar o site público, confirme que você pode usar as imagens dos desenhos.
