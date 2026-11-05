import pandas as pd
import streamlit as st

from predictor import MultilingualPromptInjectionDetector


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Prompt Injection Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# TEXT
# ============================================================

TEXT = {
    "kz": {
        "product": "Prompt Injection Detector",
        "subtitle": (
            "Қазақ, орыс және ағылшын тілдеріндегі "
            "сұрауларды талдау"
        ),
        "research": "Зерттеу прототипі",
        "input_label": "Мәтінді енгізіңіз",
        "placeholder": "Тексерілетін сұрауды жазыңыз...",
        "analyze": "Тексеру",
        "counter": "таңба",
        "empty": "Тексеру үшін мәтін енгізіңіз.",
        "too_long": "Мәтін 10 000 таңбадан аспауы керек.",
        "attack": "Prompt Injection анықталды",
        "attack_desc": (
            "Модель мәтінде алдыңғы нұсқауларды өзгертуге "
            "немесе басымдықты ауыстыруға бағытталған белгілерді анықтады."
        ),
        "safe": "Prompt Injection анықталмады",
        "safe_desc": (
            "Модель мәтінді қалыпты пайдаланушы сұрауы "
            "ретінде жіктеді."
        ),
        "score": "Decision score",
        "score_note": (
            "Decision score ықтималдық емес. "
            "Оң мән Prompt Injection жағына, "
            "теріс мән No Prompt Injection жағына бағытталады."
        ),
        "why": "Модель неге осындай шешім қабылдады?",
        "positive": "Prompt Injection жағына әсер еткен белгілер",
        "negative": "No Prompt Injection жағына әсер еткен белгілер",
        "feature": "Белгі",
        "contribution": "Үлес",
        "none": "Көрсетілетін белгілер жоқ.",
        "about": "Жүйе туралы",
        "about_text": (
            "Модель Word TF-IDF және Character TF-IDF белгілерін "
            "Linear SVM классификаторымен біріктіреді. "
            "Explainable AI блогы жеке белгілердің шешімге қосқан үлесін көрсетеді."
        ),
        "limitation": (
            "Бұл зерттеу прототипі. Жаңа немесе күрделі қайта тұжырымдалған "
            "Prompt Injection шабуылдары қате жіктелуі мүмкін."
        ),
        "privacy": "Енгізілген мәтін файлға сақталмайды.",
        "footer": "Студенттік дипломдық жоба · Satbayev University",
        "error": "Мәтінді талдау кезінде қате пайда болды.",
    },

    "ru": {
        "product": "Prompt Injection Detector",
        "subtitle": (
            "Анализ запросов на казахском, русском "
            "и английском языках"
        ),
        "research": "Исследовательский прототип",
        "input_label": "Введите текст",
        "placeholder": "Введите запрос для проверки...",
        "analyze": "Проверить",
        "counter": "символов",
        "empty": "Введите текст для проверки.",
        "too_long": "Текст не должен превышать 10 000 символов.",
        "attack": "Обнаружен Prompt Injection",
        "attack_desc": (
            "Модель обнаружила признаки попытки изменить "
            "предыдущие инструкции или их приоритет."
        ),
        "safe": "Prompt Injection не обнаружен",
        "safe_desc": (
            "Модель классифицировала текст как обычный "
            "пользовательский запрос."
        ),
        "score": "Decision score",
        "score_note": (
            "Decision score не является вероятностью. "
            "Положительное значение направлено в сторону Prompt Injection, "
            "отрицательное — No Prompt Injection."
        ),
        "why": "Почему модель приняла такое решение?",
        "positive": "Признаки в сторону Prompt Injection",
        "negative": "Признаки в сторону No Prompt Injection",
        "feature": "Признак",
        "contribution": "Вклад",
        "none": "Нет признаков для отображения.",
        "about": "О системе",
        "about_text": (
            "Модель объединяет Word TF-IDF и Character TF-IDF "
            "с классификатором Linear SVM. "
            "Explainable AI показывает вклад отдельных признаков "
            "в итоговое решение."
        ),
        "limitation": (
            "Это исследовательский прототип. Новые или сложно "
            "перефразированные Prompt Injection атаки могут "
            "классифицироваться ошибочно."
        ),
        "privacy": "Введённый текст не сохраняется в файл.",
        "footer": "Студенческий дипломный проект · Satbayev University",
        "error": "Во время анализа текста произошла ошибка.",
    },

    "en": {
        "product": "Prompt Injection Detector",
        "subtitle": (
            "Analyze prompts in Kazakh, Russian and English"
        ),
        "research": "Research prototype",
        "input_label": "Enter text",
        "placeholder": "Enter a prompt to analyze...",
        "analyze": "Analyze",
        "counter": "characters",
        "empty": "Enter text to analyze.",
        "too_long": "Text must not exceed 10,000 characters.",
        "attack": "Prompt Injection detected",
        "attack_desc": (
            "The model detected patterns associated with attempts "
            "to override or reprioritize previous instructions."
        ),
        "safe": "No Prompt Injection detected",
        "safe_desc": (
            "The model classified the text as a normal user prompt."
        ),
        "score": "Decision score",
        "score_note": (
            "Decision score is not a probability. "
            "Positive values point toward Prompt Injection, "
            "negative values toward No Prompt Injection."
        ),
        "why": "Why did the model make this decision?",
        "positive": "Features toward Prompt Injection",
        "negative": "Features toward No Prompt Injection",
        "feature": "Feature",
        "contribution": "Contribution",
        "none": "No features to display.",
        "about": "About",
        "about_text": (
            "The model combines Word TF-IDF and Character TF-IDF "
            "features with a Linear SVM classifier. "
            "Explainable AI shows how individual features "
            "contributed to the decision."
        ),
        "limitation": (
            "This is a research prototype. Novel or heavily "
            "paraphrased Prompt Injection attacks may be misclassified."
        ),
        "privacy": "Entered text is not saved to a file.",
        "footer": "Student bachelor project · Satbayev University",
        "error": "An error occurred while analyzing the text.",
    },
}


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* NORMAL PRODUCT FONT */

html,
body,
[class*="css"],
.stApp,
button,
input,
textarea,
select {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif !important;
}


/* PAGE */

.stApp {
    background: #f7f8fa;
    color: #171a21;
}

.block-container {
    max-width: 1080px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}


/* REMOVE STREAMLIT CHROME */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0;
}

section[data-testid="stSidebar"] {
    display: none;
}

button[data-testid="stSidebarCollapsedControl"] {
    display: none;
}


/* HEADER */

.product-name {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #111827;
}

.product-subtitle {
    margin-top: 0.18rem;
    font-size: 0.88rem;
    color: #7b8494;
}

.prototype-label {
    font-size: 0.76rem;
    color: #8892a2;
    text-align: right;
}


/* LANGUAGE */

div[data-testid="stRadio"] > div {
    display: flex;
    justify-content: flex-end;
    gap: 4px;
}

div[data-testid="stRadio"] label {
    padding: 0.26rem 0.58rem;
    border-radius: 7px;
}

div[data-testid="stRadio"] label:hover {
    background: #edf2f8;
}


/* MAIN PANEL */

.workspace {
    margin-top: 2rem;
    margin-bottom: 1.4rem;

    padding: 2rem;

    background: #ffffff;

    border: 1px solid #e3e7ed;
    border-radius: 16px;

    box-shadow:
        0 8px 28px rgba(19, 33, 55, 0.045);
}

.workspace-title {
    font-size: 1.8rem;
    line-height: 1.2;
    font-weight: 700;
    letter-spacing: -0.035em;
    color: #111827;
}

.workspace-description {
    max-width: 650px;

    margin-top: 0.55rem;

    color: #6f7886;
    line-height: 1.55;
}


/* TEXT AREA */

div[data-testid="stTextArea"] textarea {
    min-height: 210px;

    background: #ffffff;

    border: 1px solid #dfe4ea;
    border-radius: 12px;

    font-size: 1rem;

    box-shadow: none;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #2869c7;

    box-shadow:
        0 0 0 3px rgba(40, 105, 199, 0.08);
}


/* BUTTON */

div.stButton > button[kind="primary"] {
    min-height: 44px;

    border: 0;
    border-radius: 9px;

    background: #165da8;
    color: white;

    font-weight: 600;

    box-shadow: none;
}

div.stButton > button[kind="primary"]:hover {
    background: #124f90;
}


/* META */

.input-meta {
    color: #969eaa;
    font-size: 0.78rem;
}


/* RESULT */

.result-wrap {
    margin-top: 1.8rem;
}

.result-card {
    padding: 1.45rem 1.55rem;

    border-radius: 14px;

    border: 1px solid;
}

.result-safe {
    background: #f2faf6;
    border-color: #cee9dc;
}

.result-danger {
    background: #fff5f5;
    border-color: #f0d2d5;
}

.result-label {
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}

.result-safe .result-label {
    color: #16754f;
}

.result-danger .result-label {
    color: #b93843;
}

.result-description {
    margin-top: 0.4rem;

    color: #606a78;

    line-height: 1.5;
}


/* SCORE */

.score-box {
    height: 100%;

    padding: 1.25rem 1.4rem;

    background: #ffffff;

    border: 1px solid #e1e6ec;
    border-radius: 14px;
}

.score-label {
    color: #8992a0;
    font-size: 0.76rem;
}

.score-value {
    margin-top: 0.25rem;

    color: #172033;

    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: -0.04em;
}


/* SECTION */

.section-title {
    margin-top: 1.5rem;
    margin-bottom: 0.3rem;

    font-size: 1.15rem;
    font-weight: 700;

    color: #171c25;
}

.section-text {
    color: #707987;
    line-height: 1.55;
}


/* TABLE */

div[data-testid="stDataFrame"] {
    border: 1px solid #e4e8ed;
    border-radius: 10px;
    overflow: hidden;
}


/* EXPANDER */

details {
    border-color: #e3e7ed !important;
    border-radius: 10px !important;
}


/* ABOUT */

.about-line {
    margin-top: 2.5rem;
    padding-top: 1.2rem;

    border-top: 1px solid #e5e8ec;

    color: #9098a4;

    font-size: 0.78rem;
}

.student-project {
    color: #6f7886;
}


/* MOBILE */

@media (max-width: 800px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .workspace {
        padding: 1.3rem;
    }

    .workspace-title {
        font-size: 1.5rem;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HTML HELPER
# ============================================================

def render_html(content):

    content = "\n".join(
        line.strip()
        for line in str(content).splitlines()
        if line.strip()
    )

    st.markdown(
        content,
        unsafe_allow_html=True,
    )


# ============================================================
# MODEL
# ============================================================

@st.cache_resource
def load_detector():

    return MultilingualPromptInjectionDetector()


try:

    detector = load_detector()

except Exception:

    st.error(
        "Model loading error."
    )

    st.stop()


# ============================================================
# LANGUAGE
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "kz"


language_map = {
    "KZ": "kz",
    "RU": "ru",
    "EN": "en",
}

reverse_language_map = {
    "kz": "KZ",
    "ru": "RU",
    "en": "EN",
}


# ============================================================
# HEADER
# ============================================================

header_left, header_center, header_right = st.columns(
    [
        2.7,
        1,
        1.15,
    ]
)


with header_left:

    render_html(
        """
<div class="product-name">
Prompt Injection Detector
</div>

<div class="product-subtitle">
Multilingual ML security prototype
</div>
"""
    )


with header_right:

    language_option = st.radio(
        "Language",
        [
            "KZ",
            "RU",
            "EN",
        ],
        index=[
            "KZ",
            "RU",
            "EN",
        ].index(
            reverse_language_map[
                st.session_state.language
            ]
        ),
        horizontal=True,
        label_visibility="collapsed",
    )


st.session_state.language = (
    language_map[
        language_option
    ]
)

T = TEXT[
    st.session_state.language
]


with header_center:

    render_html(
        f"""
<div class="prototype-label">
{T["research"]}
</div>
"""
    )


# ============================================================
# INTRO
# ============================================================

render_html(
    f"""
<div class="workspace">

<div class="workspace-title">
{T["product"]}
</div>

<div class="workspace-description">
{T["subtitle"]}
</div>

</div>
"""
)


# ============================================================
# INPUT
# ============================================================

user_text = st.text_area(
    T["input_label"],
    placeholder=T["placeholder"],
    height=220,
)


button_col, count_col, privacy_col = st.columns(
    [
        1,
        0.7,
        2.2,
    ]
)


with button_col:

    analyze = st.button(
        T["analyze"],
        type="primary",
        use_container_width=True,
    )


with count_col:

    st.caption(
        f"{len(user_text):,} / 10 000 "
        f"{T['counter']}"
    )


with privacy_col:

    st.caption(
        T["privacy"]
    )


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    cleaned_text = user_text.strip()

    if not cleaned_text:

        st.warning(
            T["empty"]
        )

    elif len(cleaned_text) > 10000:

        st.warning(
            T["too_long"]
        )

    else:

        try:

            result = detector.predict(
                cleaned_text
            )

            prediction = result[
                "prediction"
            ]

            decision_score = result[
                "decision_score"
            ]

            positive = result[
                "positive_features"
            ]

            negative = result[
                "negative_features"
            ]


            # =================================================
            # RESULT
            # =================================================

            result_col, score_col = st.columns(
                [
                    2.6,
                    1,
                ]
            )


            with result_col:

                if prediction == 1:

                    render_html(
                        f"""
<div class="result-card result-danger">

<div class="result-label">
{T["attack"]}
</div>

<div class="result-description">
{T["attack_desc"]}
</div>

</div>
"""
                    )

                else:

                    render_html(
                        f"""
<div class="result-card result-safe">

<div class="result-label">
{T["safe"]}
</div>

<div class="result-description">
{T["safe_desc"]}
</div>

</div>
"""
                    )


            with score_col:

                render_html(
                    f"""
<div class="score-box">

<div class="score-label">
{T["score"]}
</div>

<div class="score-value">
{decision_score:.4f}
</div>

</div>
"""
                )


            st.caption(
                T["score_note"]
            )


            # =================================================
            # XAI
            # =================================================

            with st.expander(
                T["why"],
                expanded=True,
            ):

                positive_col, negative_col = st.columns(2)


                with positive_col:

                    st.markdown(
                        f"**{T['positive']}**"
                    )

                    if positive.empty:

                        st.caption(
                            T["none"]
                        )

                    else:

                        positive_table = (
                            positive[
                                [
                                    "feature",
                                    "contribution",
                                ]
                            ]
                            .copy()
                        )

                        positive_table.columns = [
                            T["feature"],
                            T["contribution"],
                        ]

                        positive_table[
                            T["contribution"]
                        ] = (
                            positive_table[
                                T["contribution"]
                            ]
                            .round(4)
                        )

                        st.dataframe(
                            positive_table,
                            hide_index=True,
                            use_container_width=True,
                        )


                with negative_col:

                    st.markdown(
                        f"**{T['negative']}**"
                    )

                    if negative.empty:

                        st.caption(
                            T["none"]
                        )

                    else:

                        negative_table = (
                            negative[
                                [
                                    "feature",
                                    "contribution",
                                ]
                            ]
                            .copy()
                        )

                        negative_table.columns = [
                            T["feature"],
                            T["contribution"],
                        ]

                        negative_table[
                            T["contribution"]
                        ] = (
                            negative_table[
                                T["contribution"]
                            ]
                            .round(4)
                        )

                        st.dataframe(
                            negative_table,
                            hide_index=True,
                            use_container_width=True,
                        )


        except Exception:

            st.error(
                T["error"]
            )


# ============================================================
# ABOUT
# ============================================================

with st.expander(
    T["about"]
):

    st.write(
        T["about_text"]
    )

    st.info(
        T["limitation"]
    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    f"""
<div class="about-line">

<div>
{T["footer"]}
</div>

</div>
"""
)