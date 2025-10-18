import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator

# -------------------------
# BLOQUE DE PERSONALIZACIÓN
# (solo cambia estos valores para personalizar)
# -------------------------
APP_TITLE = "TRADUCTOR · AURA"
APP_SUBHEADER = "Habla — yo traduzco y te devuelvo audio y texto."
SIDEBAR_TITLE = "Configuración del Traductor"
SIDEBAR_TEXT = (
    "Presiona el botón y, cuando escuches la señal, habla lo que quieras traducir. "
    "Luego selecciona los idiomas y el acento deseado."
)
BUTTON_LABEL = "Escuchar  🎙️"
IMAGE_WIDTH = 300

# Colores / fondo (puedes poner colores hex o gradientes CSS)
BG_GRADIENT = "linear-gradient(135deg, #0f172a 0%, #0ea5e9 100%)"  # azul profundo -> celeste
SIDEBAR_BG_OPACITY = "0.06"  # transparencia del fondo de la barra lateral
TITLE_COLOR = "#ffffff"
TEXT_COLOR = "#f1f5f9"

# -------------------------
# Aplicar estilo (CSS) — solo valores arriba si quieres cambiar
# -------------------------
page_style = f"""
<style>
/* Fondo principal con gradiente */
[data-testid="stAppViewContainer"] > .main {{
  background: {BG_GRADIENT};
  background-attachment: fixed;
}}

/* Texto global */
h1, h2, h3, .css-1v3fvcr, .css-1d391kg {{
  color: {TITLE_COLOR} !important;
}}

/* Sidebar ligero/transparente */
[data-testid="stSidebar"] {{
  background: rgba(255,255,255,{SIDEBAR_BG_OPACITY});
  backdrop-filter: blur(6px);
  border-radius: 12px;
}}

/* Personaliza el widget de audio/markdown para resaltar sobre el fondo */
.stAudio {{
  background: rgba(255,255,255,0.03);
  padding: 8px;
  border-radius: 8px;
}}

/* Ajustes de texto normal */
[class*="stText"], .css-1v3fvcr {{
  color: {TEXT_COLOR} !important;
}}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# -------------------------
# Interfaz (idéntica en lógica a la tuya, solo usa los valores personalizables)
# -------------------------
st.title(APP_TITLE)
st.subheader(APP_SUBHEADER)

image = Image.open('imagen.png')
st.image(image, width=IMAGE_WIDTH)

with st.sidebar:
    st.subheader(SIDEBAR_TITLE)
    st.write(SIDEBAR_TEXT)

st.write("Toca el botón y di lo que quieres traducir")

# label del botón usando el valor personalizado
stt_button = Button(label=BUTTON_LABEL, width=300, height=50)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
    try:
        os.mkdir("temp")
    except:
        pass
    st.title("Texto a Audio")
    translator = Translator()
    
    text = str(result.get("GET_TEXT"))
    in_lang = st.selectbox(
        "Selecciona el lenguaje de Entrada",
        (
            "Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés",
            "Francés", "Alemán", "Italiano", "Portugués", "Ruso", "Árabe",
            "Hindi", "Turco", "Neerlandés", "Sueco", "Polaco", "Vietnamita",
            "Tailandés", "Indonesio", "Hebreo"
        ),
    )
    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "Coreano":
        input_language = "ko"
    elif in_lang == "Mandarín":
        input_language = "zh-cn"
    elif in_lang == "Japonés":
        input_language = "ja"
    elif in_lang == "Francés":
        input_language = "fr"
    elif in_lang == "Alemán":
        input_language = "de"
    elif in_lang == "Italiano":
        input_language = "it"
    elif in_lang == "Portugués":
        input_language = "pt"
    elif in_lang == "Ruso":
        input_language = "ru"
    elif in_lang == "Árabe":
        input_language = "ar"
    elif in_lang == "Hindi":
        input_language = "hi"
    elif in_lang == "Turco":
        input_language = "tr"
    elif in_lang == "Neerlandés":
        input_language = "nl"
    elif in_lang == "Sueco":
        input_language = "sv"
    elif in_lang == "Polaco":
        input_language = "pl"
    elif in_lang == "Vietnamita":
        input_language = "vi"
    elif in_lang == "Tailandés":
        input_language = "th"
    elif in_lang == "Indonesio":
        input_language = "id"
    elif in_lang == "Hebreo":
        input_language = "he"
    
    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        (
            "Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés",
            "Francés", "Alemán", "Italiano", "Portugués", "Ruso", "Árabe",
            "Hindi", "Turco", "Neerlandés", "Sueco", "Polaco", "Vietnamita",
            "Tailandés", "Indonesio", "Hebreo"
        ),
    )
    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Mandarín":
        output_language = "zh-cn"
    elif out_lang == "Japonés":
        output_language = "ja"
    elif out_lang == "Francés":
        output_language = "fr"
    elif out_lang == "Alemán":
        output_language = "de"
    elif out_lang == "Italiano":
        output_language = "it"
    elif out_lang == "Portugués":
        output_language = "pt"
    elif out_lang == "Ruso":
        output_language = "ru"
    elif out_lang == "Árabe":
        output_language = "ar"
    elif out_lang == "Hindi":
        output_language = "hi"
    elif out_lang == "Turco":
        output_language = "tr"
    elif out_lang == "Neerlandés":
        output_language = "nl"
    elif out_lang == "Sueco":
        output_language = "sv"
    elif out_lang == "Polaco":
        output_language = "pl"
    elif out_lang == "Vietnamita":
        output_language = "vi"
    elif out_lang == "Tailandés":
        output_language = "th"
    elif out_lang == "Indonesio":
        output_language = "id"
    elif out_lang == "Hebreo":
        output_language = "he"
    
    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )
    
    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Irlanda":
        tld = "ie"
    elif english_accent == "Sudáfrica":
        tld = "co.za"
    
    
    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text
    
    
    display_output_text = st.checkbox("Mostrar el texto")
    
    if st.button("convertir"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Tú audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    
        if display_output_text:
            st.markdown(f"## Texto de salida:")
            st.write(f" {output_text}")
    
    
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted ", f)

    remove_files(7)



