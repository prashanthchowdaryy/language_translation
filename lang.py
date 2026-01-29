import streamlit as st
from mtranslate import translate
from gtts import gTTS
from datetime import datetime
import base64
import io

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="🌍 Translate AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# COMPREHENSIVE LANGUAGE DICTIONARY (ORGANIZED BY REGIONS)
# ============================================================================

LANGUAGE_GROUPS = {
    "🇮🇳 NORTH INDIAN": {
        "Hindi": "hi",
        "Punjabi": "pa",
        "Urdu": "ur",
        "Gujarati": "gu",
        "Kashmiri": "ks",
        "Sindhi": "sd",
        "Dogri": "doi",
    },
    "🇮🇳 SOUTH INDIAN": {
        "Tamil": "ta",
        "Telugu": "te",
        "Kannada": "kn",
        "Malayalam": "ml",
    },
    "🇮🇳 EASTERN": {
        "Bengali": "bn",
        "Assamese": "as",
        "Odia": "or",
    },
    "🇮🇳 CENTRAL": {
        "Marathi": "mr",
    },
    "🌍 INTERNATIONAL TOP 10": {
        "English": "en",
        "Mandarin Chinese": "zh-CN",
        "Spanish": "es",
        "French": "fr",
        "Arabic": "ar",
        "Portuguese": "pt",
        "Russian": "ru",
        "Japanese": "ja",
        "German": "de",
        "Korean": "ko",
    }
}

# Flatten for easy access
LANG_CODES = {}
for category, langs in LANGUAGE_GROUPS.items():
    LANG_CODES.update(langs)

# Speech supported languages
SPEECH_SUPPORTED_LANGS = {
    "en", "hi", "ta", "te", "kn", "ml", "mr", "bn", "gu", "pa", "or", "ur", "as",
    "es", "fr", "de", "pt", "ru", "ja", "ko", "ar", "zh-CN"
}

# ============================================================================
# PREMIUM CSS - PURPLE & GOLD LUXURY THEME
# ============================================================================

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Space+Mono:wght@400;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body {
            font-family: 'Poppins', sans-serif;
        }
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0015 0%, #1a0033 25%, #0d001a 50%, #150033 75%, #0a0015 100%);
            background-attachment: fixed;
            background-size: 400% 400%;
            animation: gradient-shift 15s ease infinite;
        }
        
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        [data-testid="stSidebar"] {
            background: rgba(10, 0, 21, 0.95) !important;
            backdrop-filter: blur(20px);
            border-right: 2px solid #d4af37;
            box-shadow: inset 0 0 30px rgba(212, 175, 55, 0.1);
        }
        
        [data-testid="stSidebarContent"] {
            padding: 20px;
        }
        
        /* MAIN CONTENT COLUMN FIX */
        [data-testid="stMainBlockContainer"] {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        /* TEXT AREA CONTAINER */
        .stTextArea {
            width: 100% !important;
        }
        
        .stTextArea > div {
            width: 100% !important;
        }
        
        /* TEXT AREA STYLING */
        .stTextArea textarea {
            width: 100% !important;
            border-radius: 15px !important;
            border: 2px solid #d4af37 !important;
            background: linear-gradient(135deg, rgba(26, 0, 51, 0.8) 0%, rgba(42, 0, 84, 0.8) 100%) !important;
            color: #ffffff !important;
            font-size: 15px !important;
            font-weight: 400 !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.1), inset 0 0 10px rgba(212, 175, 55, 0.05) !important;
            padding: 15px !important;
            font-family: 'Poppins', sans-serif !important;
            overflow: hidden !important;
            resize: none !important;
        }
        
        .stTextArea textarea:focus {
            border-color: #ffd700 !important;
            box-shadow: 0 0 40px rgba(212, 175, 55, 0.4), inset 0 0 15px rgba(212, 175, 55, 0.1), 0 0 20px rgba(138, 43, 226, 0.3) !important;
            outline: none !important;
        }
        
        /* BUTTON STYLING */
        .stButton > button {
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            border: 2px solid transparent !important;
            background: linear-gradient(135deg, #8a2be2 0%, #d4af37 100%) !important;
            color: #ffffff !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 6px 25px rgba(138, 43, 226, 0.4), 0 0 20px rgba(212, 175, 55, 0.2) !important;
            position: relative;
            overflow: hidden;
            width: 100% !important;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #ffd700 0%, #ff1493 100%);
            transition: left 0.4s ease;
            z-index: -1;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 35px rgba(138, 43, 226, 0.6), 0 0 30px rgba(212, 175, 55, 0.4) !important;
            border-color: #ffd700 !important;
        }
        
        .stButton > button:active {
            transform: translateY(-1px) !important;
        }
        
        /* AUDIO PLAYER */
        audio {
            width: 100% !important;
            border-radius: 10px !important;
            margin: 15px 0 !important;
        }
        
        /* GLASS CARD */
        .glass-card {
            background: linear-gradient(135deg, rgba(42, 0, 84, 0.3) 0%, rgba(26, 0, 51, 0.3) 100%);
            backdrop-filter: blur(25px);
            border: 2px solid #d4af37;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 15px 50px rgba(138, 43, 226, 0.3), inset 0 0 20px rgba(212, 175, 55, 0.05);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: visible;
            width: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .glass-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }
        
        .glass-card:hover {
            border-color: #ffd700;
            box-shadow: 0 20px 60px rgba(138, 43, 226, 0.5), inset 0 0 25px rgba(212, 175, 55, 0.1);
            transform: translateY(-2px);
        }
        
        /* TITLES */
        .title-main {
            text-align: center;
            font-size: 4em;
            font-weight: 800;
            background: linear-gradient(135deg, #d4af37 0%, #ffd700 30%, #8a2be2 70%, #d4af37 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            text-shadow: 0 0 40px rgba(212, 175, 55, 0.3);
            letter-spacing: -1px;
            font-family: 'Space Mono', monospace;
        }
        
        .subtitle {
            text-align: center;
            color: #d4af37;
            font-size: 1.15em;
            margin-bottom: 35px;
            font-weight: 300;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        
        /* STAT BOX */
        .stat-box {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.2) 0%, rgba(212, 175, 55, 0.1) 100%);
            border-left: 4px solid #ffd700;
            border-radius: 10px;
            padding: 14px 16px;
            margin: 15px 0;
            color: #ffffff;
            font-weight: 600;
            box-shadow: 0 5px 15px rgba(212, 175, 55, 0.2);
        }
        
        /* SUCCESS / WARNING MESSAGES */
        .success-msg {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.15) 0%, rgba(212, 175, 55, 0.1) 100%);
            border: 2px solid #d4af37;
            color: #ffd700;
            padding: 14px;
            border-radius: 12px;
            margin: 15px 0;
            font-weight: 600;
            box-shadow: 0 5px 20px rgba(212, 175, 55, 0.25);
        }
        
        .warning-msg {
            background: linear-gradient(135deg, rgba(255, 69, 0, 0.15) 0%, rgba(255, 140, 0, 0.1) 100%);
            border: 2px solid #ff6347;
            color: #ffb347;
            padding: 14px;
            border-radius: 12px;
            margin: 15px 0;
            font-weight: 600;
        }
        
        /* HISTORY ITEM */
        .history-item {
            background: linear-gradient(135deg, rgba(42, 0, 84, 0.5) 0%, rgba(26, 0, 51, 0.5) 100%);
            border-left: 3px solid #d4af37;
            padding: 12px 14px;
            border-radius: 8px;
            margin: 10px 0;
            color: #e0d5b7;
            font-size: 0.85em;
            transition: all 0.3s ease;
        }
        
        .history-item:hover {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.3) 0%, rgba(212, 175, 55, 0.15) 100%);
            border-left-color: #ffd700;
            box-shadow: 0 5px 15px rgba(212, 175, 55, 0.2);
        }
        
        /* FOOTER */
        .footer {
            text-align: center;
            color: #d4af37;
            padding: 25px;
            margin-top: 50px;
            border-top: 2px solid #d4af37;
            font-size: 0.95em;
            font-weight: 500;
            background: linear-gradient(to bottom, transparent, rgba(138, 43, 226, 0.1));
        }
        
        /* SECTION HEADER */
        .section-header {
            color: #ffd700;
            font-size: 1.2em;
            font-weight: 700;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* CATEGORY LABEL */
        .category-label {
            color: #ffd700;
            font-weight: 700;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 15px;
            margin-bottom: 10px;
            opacity: 0.9;
            border-bottom: 1px solid rgba(212, 175, 55, 0.3);
            padding-bottom: 8px;
        }
        
        /* SELECTED LANGUAGE BOX */
        .selected-lang-box {
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.2) 0%, rgba(212, 175, 55, 0.1) 100%);
            border: 2px solid #d4af37;
            border-radius: 12px;
            padding: 15px;
            margin: 15px 0;
            text-align: center;
            box-shadow: 0 5px 20px rgba(212, 175, 55, 0.25);
        }
        
        .selected-lang-label {
            color: #ffd700;
            font-weight: 700;
            font-size: 0.85em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        
        .selected-lang-name {
            color: #ffffff;
            font-size: 1.5em;
            font-weight: 800;
            margin-bottom: 8px;
        }
        
        .selected-lang-code {
            color: #d4af37;
            font-size: 0.85em;
        }
        
        /* DOWNLOAD BUTTON STYLING */
        [data-testid="stDownloadButton"] > button {
            background: linear-gradient(135deg, #00a86b 0%, #32cd32 100%) !important;
            border: 2px solid #00ff00 !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            width: 100% !important;
        }
        
        [data-testid="stDownloadButton"] > button:hover {
            box-shadow: 0 12px 35px rgba(0, 255, 0, 0.4) !important;
        }

        /* COLUMN FIX */
        [data-testid="stColumn"] > div {
            width: 100% !important;
        }
        
        /* CONTAINER FIX */
        [data-testid="element-container"] {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if "translation_history" not in st.session_state:
    st.session_state.translation_history = []

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "Hindi"

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "audio_data" not in st.session_state:
    st.session_state.audio_data = None

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def translate_text(text, target_lang_code):
    """Translate text using mtranslate"""
    try:
        result = translate(text, target_lang_code)
        return result, True
    except Exception as e:
        return str(e), False

def generate_speech(text, lang_code):
    """Generate speech using gTTS"""
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue(), True
    except Exception as e:
        return str(e), False

def add_to_history(source_text, translated_text, target_lang):
    """Add to translation history"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.translation_history.append({
        "time": timestamp,
        "source": source_text[:35] + "..." if len(source_text) > 35 else source_text,
        "target": target_lang,
        "translation": translated_text[:35] + "..." if len(translated_text) > 35 else translated_text
    })
    if len(st.session_state.translation_history) > 10:
        st.session_state.translation_history.pop(0)

# ============================================================================
# MAIN LAYOUT
# ============================================================================

# HEADER
st.markdown('<div class="title-main">🌍 TRANSLATE AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Premium Indian & International Language Translation</div>', unsafe_allow_html=True)

# SIDEBAR - LANGUAGE SELECTION
with st.sidebar:
    st.markdown('<div class="section-header">⚙️ CONTROL PANEL</div>', unsafe_allow_html=True)
    st.divider()
    
    # Language Selection by Categories
    for category, languages in LANGUAGE_GROUPS.items():
        st.markdown(f'<div class="category-label">{category}</div>', unsafe_allow_html=True)
        
        cols = st.columns(2, gap="small")
        lang_list = list(languages.keys())
        
        for idx, lang in enumerate(lang_list):
            with cols[idx % 2]:
                if st.button(lang, key=f"lang_{lang}", use_container_width=True):
                    st.session_state.selected_language = lang
                    st.rerun()
    
    selected_lang = st.session_state.selected_language
    
    # Selected Language Display
    st.divider()
    st.markdown(f'''
        <div class="selected-lang-box">
            <div class="selected-lang-label">Currently Selected</div>
            <div class="selected-lang-name">{selected_lang}</div>
            <div class="selected-lang-code">Code: <strong>{LANG_CODES[selected_lang]}</strong></div>
        </div>
    ''', unsafe_allow_html=True)
    
    if LANG_CODES[selected_lang] in SPEECH_SUPPORTED_LANGS:
        st.success("✅ Speech Supported")
    else:
        st.warning("⚠️ Speech Not Supported")
    
    # Translation History
    st.divider()
    st.markdown('<div class="section-header">📋 HISTORY</div>', unsafe_allow_html=True)
    
    if st.session_state.translation_history:
        for item in reversed(st.session_state.translation_history):
            st.markdown(f'''
                <div class="history-item">
                    <strong>{item['time']}</strong> • {item['target']}<br>
                    <span style="opacity: 0.75;">{item['source']}</span>
                </div>
            ''', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History", key="clear_history", use_container_width=True):
            st.session_state.translation_history = []
            st.rerun()
    else:
        st.markdown('<div style="color: rgba(255, 255, 255, 0.4); text-align: center; padding: 20px; font-size: 0.9em;">No translations yet</div>', unsafe_allow_html=True)

# MAIN CONTENT AREA
col1, col2 = st.columns(2, gap="large")

# LEFT COLUMN - SOURCE TEXT
with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📝 SOURCE TEXT</div>', unsafe_allow_html=True)
    
    input_text = st.text_area(
        label="Enter text",
        placeholder="Type or paste your text here...",
        height=280,
        label_visibility="collapsed",
        key="source_input",
        max_chars=5000
    )
    
    char_count = len(input_text)
    word_count = len(input_text.split()) if input_text.strip() else 0
    st.markdown(f'<div class="stat-box">📊 Characters: <strong>{char_count}</strong> | Words: <strong>{word_count}</strong></div>', unsafe_allow_html=True)
    
    btn_col1, btn_col2 = st.columns(2, gap="small")
    with btn_col1:
        if st.button("🔍 Auto-Detect", key="detect_btn", use_container_width=True):
            if input_text.strip():
                st.info("Language auto-detection enabled")
            else:
                st.warning("⚠️ Please enter text first")
    
    with btn_col2:
        if st.button("🗑️ Clear Text", key="clear_btn", use_container_width=True):
            st.session_state.source_input = ""
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN - TRANSLATED TEXT
with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🌐 TRANSLATED TEXT</div>', unsafe_allow_html=True)
    
    if input_text.strip():
        with st.spinner("✨ Translating..."):
            translated_text, success = translate_text(input_text, LANG_CODES[st.session_state.selected_language])
        
        if success:
            st.text_area(
                label="Translation",
                value=translated_text,
                height=280,
                disabled=True,
                label_visibility="collapsed"
            )
            
            st.markdown(f'<div class="success-msg">✅ Translation Successful!</div>', unsafe_allow_html=True)
            
            btn_col1, btn_col2, btn_col3 = st.columns(3, gap="small")
            
            with btn_col1:
                if st.button("📋 Copy", key="copy_btn", use_container_width=True):
                    st.success("Copied to clipboard!")
            
            with btn_col2:
                if st.button("💾 Add History", key="history_btn", use_container_width=True):
                    add_to_history(input_text, translated_text, st.session_state.selected_language)
                    st.success("Added to history!")
            
            with btn_col3:
                if st.button("🔊 Speak", key="speak_btn", use_container_width=True):
                    if LANG_CODES[st.session_state.selected_language] in SPEECH_SUPPORTED_LANGS:
                        with st.spinner("🎵 Generating audio..."):
                            audio_data, audio_success = generate_speech(translated_text, LANG_CODES[st.session_state.selected_language])
                        
                        if audio_success:
                            st.session_state.audio_data = audio_data
                            st.rerun()
                        else:
                            st.error("❌ Audio generation failed")
                    else:
                        st.warning(f"⚠️ Speech not supported for {st.session_state.selected_language}")
            
            # Display Audio Player if Audio Data Exists
            if st.session_state.audio_data:
                st.audio(st.session_state.audio_data, format="audio/mp3")
                
                st.download_button(
                    label="⬇️ Download Audio",
                    data=st.session_state.audio_data,
                    file_name=f"translation_{datetime.now().strftime('%H%M%S')}.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
            
            # Add to history automatically
            add_to_history(input_text, translated_text, st.session_state.selected_language)
        
        else:
            st.error(f"❌ Translation Error: {translated_text}")
    
    else:
        st.markdown('''
            <div style="text-align: center; padding: 80px 20px; color: rgba(212, 175, 55, 0.4);">
                <p style="font-size: 1.3em; font-weight: 300;">👈 Enter text to translate</p>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown('''
    <div class="footer">
        ✨ Built with ❤️ in India ✨
        <br>
        <small style="opacity: 0.7;">© 2026 Translate AI | 40+ Languages | Premium Translation Platform</small>
    </div>
''', unsafe_allow_html=True)