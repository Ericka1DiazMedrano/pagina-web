# Portal Académico: Área entre las Funciones
### Aplicaciones de la Integral Definida • Cálculo Integral

**Universidad Mariano Gálvez de Guatemala**  
Facultad de Ingeniería en Sistemas de Información y Ciencias de la Computación  
**Ciclo:** 2026  

---

## 👩‍🎓 Información Académica

- **Estudiante:** Zoila Ericka Amanda Díaz Medrano  
- **Cátedra:** Cálculo Integral  
- **Catedrático:** Lic. Juan Francisco Culajay Gaitán  

---

## 🚀 Características del Proyecto

1. **Marco Teórico Completo:**
   - Explicación de regiones tipo I ($dx$) y tipo II ($dy$).
   - Reglas de signos y puntos de corte.
2. **Graficador Interactivo y Calculadora (HTML5 Canvas):**
   - Trazado de funciones $f(x)$ y $g(x)$.
   - Sombrado dinámico del área acotada.
   - Cálculo simbólico y numérico mediante KaTeX y Math.js.
3. **Ejemplos Resueltos Paso a Paso:**
   - Ejemplos con cálculo detallado de integrales y puntos de intersección.
4. **Cuestionario Evaluativo Interactivo:**
   - Quiz con retroalimentación inmediata.
5. **Formulario y Cheatsheet Matemático:**
   - Reglas de integración inmediata y propiedades.
6. **Material Audiovisual Integrado:**
   - Reproductor multimedia HD con la exposición oficial en video (`video.mp4`).

---

## 💻 Visualización Local

Para abrir y utilizar este portal en cualquier computadora:
1. Clona este repositorio o descarga el código fuente:
   ```bash
   git clone https://github.com/Ericka1DiazMedrano/pagina-web.git
   ```
2. Ejecuta el servidor localmente con Python:
   ```bash
   python server.py
   ```
   Luego abre en tu navegador `http://localhost:10000` (o abre directamente el archivo `index.html`).

---

## ☁️ Despliegue en Render (como Web Service)

El proyecto está 100% configurado para desplegarse como un **Web Service** en [Render](https://render.com):

### Opción 1: Despliegue Automático con Blueprint (Recomendado)
1. Inicia sesión en tu cuenta de [Render.com](https://dashboard.render.com).
2. Haz clic en el botón **New +** y selecciona **Blueprint**.
3. Conecta tu repositorio `Ericka1DiazMedrano/pagina-web`.
4. Render detectará automáticamente el archivo `render.yaml` y configurará todo de forma automática.
5. Haz clic en **Apply** y tu aplicación estará en línea con HTTPS gratuito.

### Opción 2: Creación Manual de Web Service
Si prefieres crearlo manualmente:
1. En el Dashboard de Render, haz clic en **New +** > **Web Service**.
2. Conecta el repositorio `Ericka1DiazMedrano/pagina-web`.
3. Completa los siguientes campos:
   - **Name:** `pagina-web` (o el nombre que desees)
   - **Language / Runtime:** `Python 3`
   - **Branch:** `main`
   - **Region:** Elige la más cercana (ej. `Oregon (US West)` o `Ohio (US East)`)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python server.py`
   - **Plan:** `Free`
4. Haz clic en **Deploy Web Service**.

