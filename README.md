# ComunicacionesBCRA
Código para la creación y actualización de un dataset de las comunicaciones accesibles a través de la web del [Banco Central de la República Argentina](https://www.bcra.gob.ar/SistemasFinancierosYdePagos/Buscador_de_comunicaciones.asp)

Los comunicados existentes egún el BCRA son de los siguientes tipos:
```
“A” | Tratan temas normativos de carácter permanente.

“B” | Se refieren a aspectos normativos de carácter reglamentario, transitorio o circunstancial.

“C” | Tienen carácter informativo o rectificativo.

“P” | Comunicados de prensa.
```

## Instalación
Instalamos BeautifulSoup para manipular el contenido HTML de la web

```
pip install bs4
```

Y luego clonamos el repositorio

```
git clone https://github.com/sandbox-ai/ComunicacionesBCRA
cd ComunicacionesBCRA
```

---
## Uso

### main()
Para scrappear todos los comunicados, podemos simplemente correr el `main()` de ComunicacionesBCRA:
```sh
python ComunicacionesBCRA.py
```

### scrape_pdfs_naive(tipo)
Crea dataset scrappeando los comunicados del tipo especificado

```python
from ComunicacionesBCRA import ScrapperBCRA

tipo = "A"
scrapper = ScrapperBCRA()
scrapper.scrape_pdfs_naive(tipo)
```

Esto creará una carpeta de nombre `tipo` en el directorio actual, y guardará todos los comunicados encontrados a partir del dia de la fecha. Podemos correr estas líneas con un dataset ya creado y se descargarán solamente los documentos que no tengamos.

### scrape_urls(tipo)
Si solamente quisieramos guardar las URLs al contenido y no los documentos en sí, podemos usar esta función:
```python
from ComunicacionesBCRA import ScrapperBCRA

tipo = "A"
scrapper = ScrapperBCRA()
scrape_pdfs_naive(tipo)
```

Esto creará un txt llamado `BCRA_{tipo}.txt` conteniendo las URLs relativas a los PDFs de los comunicados.

---
## [Dataset en Huggingface🤗](https://huggingface.co/datasets/marianbasti/ComunicacionesBCRA)
Actualizada diariamente

Estado de la última actualizacion: 
[![Update HuggingFace Dataset](https://github.com/sandbox-aiComunicacionesBCRA/actions/workflows/update_hf_dataset.yml/badge.svg)](https://github.com/sandbox-ai/ComunicacionesBCRA/actions/workflows/update_hf_dataset.yml)
