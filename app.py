import streamlit as st
from groq import Groq
import base64
import json
from PIL import Image
import io

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="StyleSense – AI Fashion Advisor",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hero Banner ── */
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at 70% 30%, rgba(229,160,90,0.15) 0%, transparent 60%);
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e5a05a, #f5c97a, #e5a05a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.1;
    }
    .hero-sub {
        color: rgba(255,255,255,0.7);
        font-size: 1.05rem;
        margin-top: 0.6rem;
        font-weight: 300;
        letter-spacing: 0.04em;
    }
    .badge-row {
        display: flex;
        gap: 0.6rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 1.2rem;
    }
    .badge {
        background: rgba(229,160,90,0.18);
        border: 1px solid rgba(229,160,90,0.4);
        color: #f5c97a;
        border-radius: 20px;
        padding: 0.25rem 0.85rem;
        font-size: 0.78rem;
        font-weight: 500;
        letter-spacing: 0.05em;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121f 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(229,160,90,0.2);
    }
    [data-testid="stSidebar"] * { color: #e8e8f0 !important; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f5c97a !important;
        font-family: 'Playfair Display', serif !important;
    }

    /* ── Feature Cards ── */
    .feature-card {
        background: linear-gradient(135deg, #1e1e35 0%, #252540 100%);
        border: 1px solid rgba(229,160,90,0.25);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.2s, border-color 0.2s;
        cursor: default;
    }
    .feature-card:hover {
        transform: translateY(-3px);
        border-color: rgba(229,160,90,0.6);
    }
    .feature-icon { font-size: 2.2rem; margin-bottom: 0.5rem; }
    .feature-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: #f5c97a;
        margin-bottom: 0.3rem;
    }
    .feature-desc { font-size: 0.82rem; color: rgba(255,255,255,0.55); }

    /* ── Response Box ── */
    .ai-response {
        background: linear-gradient(135deg, #1a1a30 0%, #1e2040 100%);
        border: 1px solid rgba(229,160,90,0.3);
        border-left: 4px solid #e5a05a;
        border-radius: 12px;
        padding: 1.5rem 1.8rem;
        margin-top: 1.2rem;
        color: #e8e8f0;
        line-height: 1.75;
        font-size: 0.95rem;
    }
    .ai-response h3 { color: #f5c97a; font-family: 'Playfair Display', serif; margin-top: 0; }

    /* ── Section Headers ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    .section-header h2 {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: #f5c97a;
        margin: 0;
    }

    /* ── Tab Styling ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(26,26,46,0.8);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid rgba(229,160,90,0.2);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255,255,255,0.55);
        border-radius: 8px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e5a05a, #f5c97a) !important;
        color: #1a1a2e !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #e5a05a, #f5c97a);
        color: #1a1a2e;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.55rem 1.4rem;
        transition: opacity 0.2s, transform 0.15s;
        font-family: 'Inter', sans-serif;
    }
    .stButton > button:hover {
        opacity: 0.88;
        transform: translateY(-1px);
    }

    /* ── Inputs ── */
    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        background: rgba(26,26,46,0.9) !important;
        border: 1px solid rgba(229,160,90,0.3) !important;
        border-radius: 10px !important;
        color: #e8e8f0 !important;
    }
    .stSlider > div > div > div { background: #e5a05a !important; }

    /* ── Trend Tag ── */
    .trend-tag {
        display: inline-block;
        background: rgba(229,160,90,0.15);
        border: 1px solid rgba(229,160,90,0.35);
        color: #f5c97a;
        border-radius: 20px;
        padding: 0.2rem 0.7rem;
        font-size: 0.78rem;
        margin: 0.2rem;
        font-weight: 500;
    }

    /* ── History Card ── */
    .history-card {
        background: rgba(26,26,46,0.7);
        border: 1px solid rgba(229,160,90,0.2);
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.6rem;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.75);
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #e5a05a !important; }

    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.3);
        font-size: 0.78rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(229,160,90,0.1);
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "history": [],
        "api_key": "",
        "groq_client": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# Groq Helper
# ─────────────────────────────────────────────
def get_client():
    key = st.session_state.api_key.strip()
    if not key:
        return None
    if st.session_state.groq_client is None:
        st.session_state.groq_client = Groq(api_key=key)
    return st.session_state.groq_client


def call_groq(messages: list, model: str = "llama-3.3-70b-versatile", temperature: float = 0.8) -> str:
    client = get_client()
    if client is None:
        return "⚠️ Please enter your Groq API key in the sidebar to continue."
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=1500,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ Groq API Error: {str(e)}"


def call_groq_vision(image_b64: str, prompt: str, model: str = "meta-llama/llama-4-scout-17b-16e-instruct") -> str:
    client = get_client()
    if client is None:
        return "⚠️ Please enter your Groq API key in the sidebar to continue."
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                    {"type": "text", "text": prompt},
                ],
            }],
            temperature=0.7,
            max_tokens=1200,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ Groq Vision Error: {str(e)}"


def save_history(category: str, query: str, response: str):
    st.session_state.history.insert(0, {"cat": category, "q": query[:80], "r": response[:200]})
    if len(st.session_state.history) > 15:
        st.session_state.history = st.session_state.history[:15]


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 👗 StyleSense")
    st.markdown("*Your Generative AI Fashion Advisor*")
    st.divider()

    st.markdown("### 🔑 API Configuration")
    api_input = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at console.groq.com",
        value=st.session_state.api_key,
    )
    if api_input != st.session_state.api_key:
        st.session_state.api_key = api_input
        st.session_state.groq_client = None

    if st.session_state.api_key:
        st.success("✅ API Key set")
    else:
        st.info("Enter your Groq API key above")

    st.divider()
    st.markdown("### ⚙️ Preferences")
    gender = st.selectbox("Style Profile", ["Women's Fashion", "Men's Fashion", "Unisex / Gender-Neutral"])
    age_group = st.selectbox("Age Group", ["Teen (13-19)", "Young Adult (20-35)", "Adult (36-55)", "Mature (55+)"])
    budget = st.select_slider("Budget Range", options=["Budget", "Mid-Range", "Premium", "Luxury"], value="Mid-Range")
    style_persona = st.multiselect(
        "Style Persona",
        ["Minimalist", "Bohemian", "Streetwear", "Classic", "Edgy", "Romantic", "Athleisure", "Business Casual"],
        default=["Classic"],
    )

    st.divider()
    st.markdown("### 🌍 Current Season")
    season = st.selectbox("Season", ["Spring/Summer", "Fall/Winter", "All-Season"])

    st.divider()
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.success("History cleared!")


# ─────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-title">✨ StyleSense</p>
    <p class="hero-sub">Generative AI–Powered Fashion Recommendation System</p>
    <div class="badge-row">
        <span class="badge">🤖 Groq LLM</span>
        <span class="badge">👁️ Vision AI</span>
        <span class="badge">🎨 Outfit Generator</span>
        <span class="badge">📈 Trend Insights</span>
        <span class="badge">💬 Style Chat</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Feature Cards
cols = st.columns(5)
features = [
    ("👗", "Outfit Builder", "Generate complete looks"),
    ("📸", "Image Analysis", "Analyze your wardrobe"),
    ("💬", "Style Advisor", "Personalized guidance"),
    ("🔥", "Trend Reports", "What's hot right now"),
    ("🔄", "Outfit Remix", "Reimagine your pieces"),
]
for col, (icon, title, desc) in zip(cols, features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────
tabs = st.tabs(["👗 Outfit Builder", "📸 Image Analyzer", "💬 Style Advisor", "🔥 Trend Insights", "🔄 Outfit Remix", "📋 History"])


# ════════════════════════════════════════════════
# TAB 1 – OUTFIT BUILDER
# ════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header"><h2>👗 Outfit Builder</h2></div>', unsafe_allow_html=True)
    st.markdown("*Describe an occasion and get a complete, curated outfit recommendation.*")

    c1, c2 = st.columns([3, 2])
    with c1:
        occasion = st.text_area(
            "Describe your occasion or event",
            placeholder="e.g. Rooftop birthday dinner in summer, semi-formal dress code...",
            height=110,
        )
        col_a, col_b = st.columns(2)
        with col_a:
            color_pref = st.text_input("Color Preferences", placeholder="e.g. earthy tones, pastels, monochrome")
        with col_b:
            avoid = st.text_input("Items to Avoid", placeholder="e.g. heels, tight fits, loud prints")

    with c2:
        weather = st.selectbox("Weather / Climate", ["Warm & Sunny", "Hot & Humid", "Cool & Breezy", "Cold", "Rainy"])
        formality = st.select_slider("Formality Level", options=["Casual", "Smart Casual", "Business Casual", "Semi-Formal", "Formal"])
        creativity = st.slider("Creativity Level", 0.1, 1.0, 0.75, 0.05, help="Higher = more bold & experimental")

    if st.button("✨ Generate Outfit", key="outfit_btn"):
        if not occasion.strip():
            st.warning("Please describe your occasion first.")
        else:
            persona_str = ", ".join(style_persona) if style_persona else "Classic"
            system_prompt = f"""You are StyleSense, an elite AI fashion stylist with deep expertise in global fashion trends, 
color theory, body styling, and wardrobe curation. You provide highly personalized, detailed, and on-trend outfit recommendations.
Always structure your response clearly with sections: 🎯 The Look, 👕 Top, 👖 Bottom/Full Outfit, 👟 Footwear, 
👜 Accessories, 💄 Hair & Beauty (optional), 💡 Styling Tips, 💰 Budget Estimate."""

            user_msg = f"""Create a complete outfit recommendation for:
- Occasion: {occasion}
- Style Profile: {gender}, {age_group}
- Style Persona: {persona_str}
- Budget: {budget}
- Season: {season}
- Weather: {weather}
- Formality: {formality}
- Color Preferences: {color_pref if color_pref else 'Open to suggestions'}
- Items to Avoid: {avoid if avoid else 'None'}

Provide a detailed, fashionable, and wearable outfit with specific clothing items, brands (at the {budget} price point), 
and styling advice. Be specific and inspiring."""

            with st.spinner("Curating your perfect outfit..."):
                response = call_groq(
                    [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
                    temperature=creativity,
                )
            st.markdown(f'<div class="ai-response"><h3>✨ Your Curated Outfit</h3>{response}</div>', unsafe_allow_html=True)
            save_history("Outfit Builder", occasion, response)


# ════════════════════════════════════════════════
# TAB 2 – IMAGE ANALYZER
# ════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header"><h2>📸 Image Analyzer</h2></div>', unsafe_allow_html=True)
    st.markdown("*Upload a clothing item or outfit photo for AI-powered style analysis.*")

    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")

    if uploaded:
        img = Image.open(uploaded)
        col_img, col_opts = st.columns([1, 1])
        with col_img:
            st.image(img, caption="Your uploaded image", use_container_width=True)
        with col_opts:
            analysis_type = st.selectbox("What would you like to know?", [
                "Complete Style Analysis",
                "Color Palette & Coordination",
                "Occasion Suitability",
                "Styling Suggestions & Improvements",
                "Similar Items & Alternatives",
                "Trend Assessment",
            ])
            extra_context = st.text_area("Additional context (optional)", placeholder="e.g. I'm attending a wedding, I'm petite...")

        if st.button("🔍 Analyze Image", key="img_btn"):
            # Convert to base64
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            img_b64 = base64.b64encode(buf.getvalue()).decode()

            persona_str = ", ".join(style_persona) if style_persona else "Classic"
            prompt = f"""You are StyleSense, a world-class AI fashion stylist and image analyst.
Analyze this fashion image and provide a {analysis_type}.

User Profile: {gender}, {age_group}, {budget} budget, {persona_str} style persona, {season} season.
Additional context: {extra_context if extra_context else 'None provided.'}

Structure your response with clear sections, emoji headers, and actionable advice.
Be specific about colors, cuts, fabrics, and styling opportunities."""

            with st.spinner("Analyzing your image with AI vision..."):
                response = call_groq_vision(img_b64, prompt)
            st.markdown(f'<div class="ai-response"><h3>🔍 Style Analysis</h3>{response}</div>', unsafe_allow_html=True)
            save_history("Image Analysis", analysis_type, response)
    else:
        st.info("📁 Upload a clothing item, outfit, or style inspiration image to get started.")


# ════════════════════════════════════════════════
# TAB 3 – STYLE ADVISOR (Chat)
# ════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header"><h2>💬 Style Advisor</h2></div>', unsafe_allow_html=True)
    st.markdown("*Ask anything about fashion — get expert AI advice tailored to you.*")

    # Quick prompts
    st.markdown("**Quick Questions:**")
    qcols = st.columns(4)
    quick_qs = [
        "What capsule wardrobe pieces should I own?",
        "How do I dress for my body type?",
        "What colors suit warm skin tones?",
        "How to style oversized clothes?",
    ]
    if "quick_q" not in st.session_state:
        st.session_state.quick_q = ""
    for i, (qcol, qq) in enumerate(zip(qcols, quick_qs)):
        with qcol:
            if st.button(f"💡 {qq[:25]}...", key=f"qq_{i}"):
                st.session_state.quick_q = qq

    question = st.text_area(
        "Your style question",
        value=st.session_state.quick_q,
        placeholder="e.g. How do I build a versatile wardrobe on a mid-range budget?",
        height=100,
    )
    if st.session_state.quick_q:
        st.session_state.quick_q = ""

    detail_level = st.radio("Response Detail", ["Concise", "Detailed", "Comprehensive"], horizontal=True, index=1)

    if st.button("💬 Get Style Advice", key="chat_btn"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            persona_str = ", ".join(style_persona) if style_persona else "Classic"
            detail_map = {"Concise": "brief (200-300 words)", "Detailed": "detailed (400-600 words)", "Comprehensive": "comprehensive (600-900 words)"}
            system_prompt = f"""You are StyleSense, a sophisticated AI fashion advisor combining the expertise of a personal stylist, 
fashion editor, and trend forecaster. You give warm, inclusive, practical, and inspiring fashion guidance.
Always personalize advice to the user's profile and be specific with actionable recommendations."""

            user_msg = f"""Fashion question: {question}

My Profile:
- Style Profile: {gender}, {age_group}
- Budget: {budget}
- Style Persona: {persona_str}
- Season: {season}

Please give a {detail_map[detail_level]} response with clear structure, practical tips, and specific examples."""

            with st.spinner("Your style advisor is thinking..."):
                response = call_groq(
                    [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
                    temperature=0.75,
                )
            st.markdown(f'<div class="ai-response"><h3>💬 Style Advice</h3>{response}</div>', unsafe_allow_html=True)
            save_history("Style Advisor", question, response)


# ════════════════════════════════════════════════
# TAB 4 – TREND INSIGHTS
# ════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header"><h2>🔥 Trend Insights</h2></div>', unsafe_allow_html=True)
    st.markdown("*Explore current fashion trends and get AI-curated insights.*")

    c1, c2 = st.columns([1, 1])
    with c1:
        trend_category = st.selectbox("Trend Category", [
            "Overall Fashion Trends",
            "Color Trends",
            "Fabric & Texture Trends",
            "Silhouette Trends",
            "Accessory Trends",
            "Footwear Trends",
            "Streetwear Trends",
            "Sustainable Fashion Trends",
            "Luxury Fashion Trends",
            "Workwear Trends",
        ])
    with c2:
        trend_region = st.selectbox("Fashion Region", ["Global / International", "Western", "Asian Fashion", "European High Fashion", "American Street Style"])

    include_tips = st.checkbox("Include 'How to Wear It' tips", value=True)

    if st.button("🔥 Get Trend Report", key="trend_btn"):
        persona_str = ", ".join(style_persona) if style_persona else "Classic"
        system_prompt = """You are StyleSense's Trend Intelligence Engine — a cutting-edge AI with encyclopedic knowledge of 
global fashion weeks, runway shows, street style, and emerging micro-trends. You deliver insightful, specific, and exciting trend reports."""

        user_msg = f"""Generate a comprehensive {trend_category} report for {season} season, {trend_region} perspective.

Target Profile: {gender}, {age_group}, {budget} budget, {persona_str} style persona.

Include:
1. 🌟 Top 5-7 Key Trends with detailed descriptions
2. 🎨 Key Colors / Textures driving each trend
3. 💡 Who's wearing it (celebrity/influencer examples)
{"4. 👗 How to Incorporate Each Trend into your wardrobe" if include_tips else ""}
5. 📊 Trend Longevity (Micro-trend vs. Macro-trend vs. Classic evolution)
6. 💰 Budget-friendly alternatives at {budget} price point

Make it feel like reading a premium fashion magazine feature."""

        with st.spinner("Analyzing global fashion trends..."):
            response = call_groq(
                [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
                temperature=0.85,
            )
        st.markdown(f'<div class="ai-response"><h3>🔥 {trend_category} — {season}</h3>{response}</div>', unsafe_allow_html=True)
        save_history("Trend Report", trend_category, response)


# ════════════════════════════════════════════════
# TAB 5 – OUTFIT REMIX
# ════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header"><h2>🔄 Outfit Remix</h2></div>', unsafe_allow_html=True)
    st.markdown("*Tell us what's in your wardrobe and we'll create multiple outfit combinations.*")

    wardrobe = st.text_area(
        "List your wardrobe items",
        placeholder="e.g.\n- White button-down shirt\n- Black skinny jeans\n- Beige trench coat\n- White sneakers\n- Brown leather loafers\n- Navy blazer\n- Striped tee",
        height=160,
    )

    c1, c2 = st.columns(2)
    with c1:
        num_outfits = st.slider("Number of Outfits to Generate", 2, 6, 3)
        remix_occasions = st.multiselect(
            "Target Occasions",
            ["Daily / Casual", "Work / Office", "Date Night", "Weekend Brunch", "Evening Out", "Travel", "Gym / Active"],
            default=["Daily / Casual", "Work / Office"],
        )
    with c2:
        remix_style = st.selectbox("Remix Style Direction", [
            "Keep it wearable & practical",
            "Push creative boundaries",
            "Minimalist & clean",
            "Maximalist & bold",
            "Mix high & low fashion",
        ])

    if st.button("🔄 Remix My Wardrobe", key="remix_btn"):
        if not wardrobe.strip():
            st.warning("Please list your wardrobe items first.")
        else:
            persona_str = ", ".join(style_persona) if style_persona else "Classic"
            occasions_str = ", ".join(remix_occasions) if remix_occasions else "general use"
            system_prompt = """You are StyleSense's Wardrobe Remix AI — a creative stylist who can transform any combination of 
clothing into stylish, cohesive outfits. You think like a personal stylist who knows every trick in the book."""

            user_msg = f"""Here is my wardrobe:
{wardrobe}

Create exactly {num_outfits} distinct outfit combinations for: {occasions_str}

Style Direction: {remix_style}
Profile: {gender}, {age_group}, {budget} budget, {persona_str} persona, {season} season.

For each outfit provide:
- 🏷️ Outfit Name & Occasion
- 👗 The Combination (specific items from the list)
- ✨ Styling Details (how to wear/layer each piece)
- 👟 Shoe & Accessory Pairing
- 🎨 Color Story
- 💡 Pro Tip

Make each outfit feel distinct, intentional, and achievable."""

            with st.spinner(f"Creating {num_outfits} outfit remixes..."):
                response = call_groq(
                    [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
                    temperature=0.9,
                )
            st.markdown(f'<div class="ai-response"><h3>🔄 Your Wardrobe Remixed</h3>{response}</div>', unsafe_allow_html=True)
            save_history("Outfit Remix", f"{num_outfits} outfits from wardrobe", response)


# ════════════════════════════════════════════════
# TAB 6 – HISTORY
# ════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header"><h2>📋 Session History</h2></div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("No history yet. Start exploring StyleSense features above!")
    else:
        st.markdown(f"*{len(st.session_state.history)} recent interactions*")
        for i, item in enumerate(st.session_state.history):
            with st.expander(f"[{item['cat']}] {item['q']}"):
                st.markdown(f'<div class="history-card">{item["r"]}...</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ✨ <strong>StyleSense</strong> · Powered by Groq LLM & Llama · Built with Streamlit<br>
    Fashion recommendations are AI-generated for inspiration purposes.
</div>
""", unsafe_allow_html=True)
