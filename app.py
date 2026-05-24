import streamlit as st
from google import genai
from google.genai import types
import io

# ──────────────────────────────────────────────
# CONFIG DA PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Figurinha Copa 2026 🎴",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CSS PERSONALIZADO
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* Fundo escuro estilizado */
    .stApp {
        background: linear-gradient(160deg, #0a1628 0%, #0d2137 50%, #0a1628 100%);
    }

    /* Título principal */
    h1 {
        color: #FFD700 !important;
        text-align: center;
        font-size: 2.4rem !important;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(255,215,0,0.4);
    }

    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: #00E5E5;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    /* Cards de seção */
    .card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
    }

    /* Botão principal */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #000 !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        letter-spacing: 1.5px;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.8rem 2rem !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(255,180,0,0.45) !important;
        transition: all 0.2s ease !important;
    }

    /* Botão download */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00C853, #00897B) !important;
        color: #fff !important;
        font-weight: 700 !important;
        border-radius: 25px !important;
        width: 100% !important;
    }

    /* Labels */
    label {
        color: #00E5E5 !important;
        font-weight: 600 !important;
    }

    /* Input */
    .stTextInput input {
        background: rgba(255,255,255,0.08) !important;
        color: #fff !important;
        border: 1px solid rgba(0,229,229,0.3) !important;
        border-radius: 10px !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(0,229,229,0.3) !important;
        border-radius: 10px !important;
        color: #fff !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10,22,40,0.95) !important;
        border-right: 1px solid rgba(0,229,229,0.2);
    }

    /* Rodapé */
    .footer {
        text-align: center;
        color: #4a6080;
        font-size: 0.75rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR — API KEY + DICAS
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuração")
    api_key = st.text_input(
        "🔑 API Key do Google Gemini:",
        type="password",
        placeholder="Cole sua chave aqui...",
        help="Obtenha grátis em: aistudio.google.com/apikey",
    )
    if api_key:
        st.success("✅ Chave configurada!")
    else:
        st.info("👆 Cole sua API Key para começar")
        st.markdown("[📎 Pegar API Key grátis](https://aistudio.google.com/apikey)", unsafe_allow_html=False)

    st.markdown("---")
    st.markdown("### 📸 Dicas de foto")
    st.markdown("""
- ✅ Boa iluminação (luz natural)
- ✅ Foto frontal / olhando pra frente
- ✅ Fundo limpo ou neutro
- ✅ Mínimo 400 x 500 pixels
- ❌ Evite selfies com filtro
- ❌ Evite fotos de lado ou de perfil
""")
    st.markdown("---")
    st.markdown("### ⚙️ Sobre o app")
    st.markdown("Powered by **Google Gemini 2.0 Flash**")
    st.markdown("Modelo de IA multimodal com geração de imagens")

# ──────────────────────────────────────────────
# CABEÇALHO
# ──────────────────────────────────────────────
st.markdown("# ⚽ Figurinha da Copa 2026")
st.markdown('<p class="subtitle">Crie sua figurinha Panini personalizada com Inteligência Artificial!</p>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FORMULÁRIO
# ──────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 👤 Seus dados na figurinha")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    player_name = st.text_input(
        "Nome do jogador:",
        placeholder="SEU NOME",
        max_chars=20,
        help="Aparece na parte de baixo da figurinha"
    ).upper()

with col2:
    country = st.selectbox(
        "País:",
        ["BRASIL", "PORTUGAL", "ARGENTINA", "ESPANHA", "ITALIA", "FRANCA", "ALEMANHA", "MEXICO"],
    )

with col3:
    country_code_map = {
        "BRASIL": "BRA", "PORTUGAL": "POR", "ARGENTINA": "ARG",
        "ESPANHA": "ESP", "ITALIA": "ITA", "FRANCA": "FRA",
        "ALEMANHA": "GER", "MEXICO": "MEX",
    }
    st.text_input("Código:", value=country_code_map.get(country, "BRA"), disabled=True)

st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# UPLOAD DE FOTO
# ──────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📷 Sua foto")

uploaded_file = st.file_uploader(
    "Arraste a foto ou clique para escolher:",
    type=["jpg", "jpeg", "png", "webp"],
    help="Formatos aceitos: JPG, PNG, WEBP",
)
st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# PREVIEW ANTES DE GERAR
# ──────────────────────────────────────────────
col_orig, col_result = st.columns(2)

if uploaded_file:
    with col_orig:
        st.markdown("**📷 Foto original:**")
        st.image(uploaded_file, use_container_width=True)

# ──────────────────────────────────────────────
# BOTÃO GERAR
# ──────────────────────────────────────────────
st.markdown("---")

btn_disabled = not uploaded_file or not api_key

if not api_key:
    st.warning("⚠️ Configure sua API Key na barra lateral (esquerda) para continuar.")

if not uploaded_file and api_key:
    st.info("📸 Envie sua foto acima para começar!")

gerar = st.button(
    "🎴 GERAR MINHA FIGURINHA!",
    type="primary",
    disabled=btn_disabled,
    use_container_width=True,
)

# ──────────────────────────────────────────────
# GERAÇÃO COM GEMINI
# ──────────────────────────────────────────────
def build_prompt(name: str, country: str, code: str) -> str:
    return f"""
You are a professional graphic designer creating a Panini FIFA World Cup 2026 sticker card.

Your task: Transform the person in the provided photo into a complete, official-looking Panini FIFA World Cup 2026 collectible sticker card.

═══ CARD STRUCTURE ═══

**OVERALL CARD:**
- Sticker card proportions: portrait orientation, slightly taller than wide (like a real Panini sticker)
- Rounded corners (like a real collectible card)
- The entire image should BE the sticker card — not a photo of a person with a sticker overlay

**BACKGROUND:**
- Bright teal/cyan background (#00B4B4 to #008080)
- Large decorative number "26" in the background (dark green, large, partially cropped by edges)
- Green organic blob shapes or swooshes behind the player

**TOP RIGHT CORNER:**
- FIFA World Cup 26 logo: white trophy silhouette icon, "26" in large stylized text, "FIFA" text below it — all inside a small white box/badge

**PLAYER (center of card):**
- Show the person from the waist up, centered on the card
- Realistically preserve their face and likeness from the uploaded photo
- Dress them in a bright yellow (#FFD700) and green (#009B3A) Brazilian national soccer jersey with "CBF" badge and Nike logo, OR keep their clothing if it's already sporty
- Pose: confident, slightly angled, like an official soccer player portrait
- Lighting: professional studio sports photography

**RIGHT SIDE PANEL (vertical strip):**
- Circular flag badge of {country} at top of right panel
- Letters "{code}" stacked vertically in bold teal text with white outline

**BOTTOM BANNER:**
- Dark teal/dark green rounded pill-shaped banner
- Player name in bold white uppercase text: "{name if name else 'SEU NOME'}"
- Below name in smaller text: birthdate | height ~1.75m | weight ~70kg

**VERY BOTTOM STRIP:**
- Dark background narrow strip
- Team/club text in white (e.g., "SANTOS FC (BRA)")
- Small PANINI logo on the right side (stylized bird mascot + "PANINI" text) in yellow/orange

═══ STYLE ═══
- Vibrant, saturated colors
- High production quality — this should look like an ACTUAL Panini sticker you'd find in a pack
- Clean, graphic design aesthetic
- The person's face must remain recognizable

Generate ONLY the sticker card image. Do not add any frame, shadow, or background outside the card itself.
"""

if gerar and uploaded_file and api_key:
    code = country_code_map.get(country, "BRA")

    with st.spinner("🎨 Gerando sua figurinha... aguarde alguns segundos..."):
        try:
            client = genai.Client(api_key=api_key)

            # Lê a imagem enviada
            image_bytes = uploaded_file.read()
            mime = uploaded_file.type or "image/jpeg"

            prompt_text = build_prompt(player_name, country, code)

            # Chama o Gemini com geração de imagem
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[
                    types.Part.from_text(prompt_text),
                    types.Part.from_bytes(data=image_bytes, mime_type=mime),
                ],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                ),
            )

            # Extrai a imagem gerada
            generated_image_data = None
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    generated_image_data = part.inline_data.data
                    break

            if generated_image_data:
                with col_result:
                    st.markdown("**🎴 Sua Figurinha:**")
                    st.image(generated_image_data, use_container_width=True)

                st.success("✅ Figurinha gerada com sucesso!")

                safe_name = (player_name or "jogador").replace(" ", "_")
                st.download_button(
                    label="⬇️ BAIXAR FIGURINHA (PNG)",
                    data=generated_image_data,
                    file_name=f"figurinha_{safe_name}_copa2026.png",
                    mime="image/png",
                    use_container_width=True,
                )

                st.balloons()

            else:
                st.error("❌ O modelo não retornou uma imagem. Tente novamente com uma foto diferente.")
                # Mostra texto de resposta se houver
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "text") and part.text:
                        st.info(f"Resposta da IA: {part.text}")

        except Exception as e:
            err = str(e)
            st.error(f"❌ Erro ao gerar figurinha: {err}")
            if "API_KEY" in err.upper() or "invalid" in err.lower() or "credential" in err.lower():
                st.warning("🔑 Verifique se sua API Key está correta.")
            elif "quota" in err.lower() or "429" in err:
                st.warning("⏳ Limite de requisições atingido. Aguarde 1 minuto e tente novamente.")
            elif "400" in err:
                st.warning("📸 Tente com uma foto de melhor qualidade ou diferente formato.")

# ──────────────────────────────────────────────
# RODAPÉ
# ──────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Studio Digital • Criador de Figurinhas Copa 2026 • Powered by Google Gemini AI<br>
    Este app é para uso criativo/entretenimento. Não é afiliado à FIFA ou Panini.
</div>
""", unsafe_allow_html=True)
