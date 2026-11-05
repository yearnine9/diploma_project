"use strict";


/* =========================================================
   TRANSLATIONS
========================================================= */

const translations = {

    kk: {

        brandSubtitle:
            "Көптілді LLM қауіпсіздігі",

        navPlayground:
            "Playground",

        navAnalytics:
            "Аналитика",

        navMethod:
            "Әдіс",

        modelActive:
            "Модель белсенді",

        heroCode:
            "01 / КӨПТІЛДІ LLM ҚАУІПСІЗДІГІ",

        heroTitle:
            "Prompt Injection шабуылдарын түсіндірілетін ML арқылы анықтау",

        heroDescription:
            "Қазақ, орыс және ағылшын тілдеріндегі LLM сұрауларын Hybrid TF-IDF, Linear SVM және Explainable AI негізінде талдау.",

        openPlayground:
            "Playground ашу",

        playgroundTitle:
            "Prompt Security Playground",

        playgroundDescription:
            "Модельге нақты сұрау жіберіп, классификация мен XAI нәтижесін тексеріңіз.",

        promptPlaceholder:
            "Тексерілетін сұрауды енгізіңіз...",

        privacy:
            "Мәтін файлға сақталмайды",

        analyze:
            "Талдау",

        waiting:
            "КҮТУ",

        analyzing:
            "ТАЛДАУ",

        completed:
            "АЯҚТАЛДЫ",

        awaitingInput:
            "Сұрау күтілуде",

        awaitingDescription:
            "Классификация мен XAI нәтижелері осы жерде көрсетіледі.",

        safeStatus:
            "NO PROMPT INJECTION",

        attackStatus:
            "PROMPT INJECTION",

        safeTitle:
            "Prompt Injection анықталмады",

        attackTitle:
            "Prompt Injection анықталды",

        safeDescription:
            "Модель мәтінді қалыпты пайдаланушы сұрауы ретінде жіктеді.",

        attackDescription:
            "Модель алдыңғы нұсқауларды өзгертуге немесе олардың басымдығын ауыстыруға бағытталған белгілерді анықтады.",

        decisionScore:
            "DECISION SCORE",

        decisionBoundary:
            "DECISION BOUNDARY",

        classification:
            "Классификация",

        xaiTitle:
            "Explainable AI",

        xaiDescription:
            "Модель шешіміне әсер еткен нақты мәтіндік белгілер.",

        towardAttack:
            "Prompt Injection жағына",

        towardSafe:
            "No Prompt Injection жағына",

        noFeatures:
            "Айқын белгілер табылмады.",

        xaiNote:
            "XAI модель шешімін түсіндіруге көмектеседі, бірақ толық семантикалық түсінудің дәлелі емес.",

        analyticsTitle:
            "Көптілді модельді бағалау",

        analyticsDescription:
            "Жабық multilingual test жиынтығындағы нақты эксперименттік нәтижелер.",

        closedTest:
            "Жабық тест",

        languagePerformance:
            "Тілдер бойынша F1",

        stressTest:
            "Robustness Stress Test",

        stressNote:
            "36 жаңа қолмен құрылған мысал. Модельді қайта оқытуға немесе threshold баптауға қолданылмаған.",

        methodTitle:
            "Detection Pipeline",

        methodDescription:
            "Сұраудан классификация мен түсіндірмеге дейінгі әдіс.",

        methodInput:
            "Кіріс",

        methodInputDescription:
            "Көптілді пайдаланушы сұрауы.",

        methodClassifier:
            "Бинарлық классификация.",

        methodXai:
            "Локалды feature contribution.",

        methodResearchNote:
            "Бұл әдіс LLM-нің өзінен тәуелсіз алдын ала қауіпсіздік қабаты ретінде жұмыс істейді.",

        researchDetails:
            "Зерттеу туралы",

        researchTitle:
            "Көптілді LLM жүйелеріндегі Prompt Injection шабуылдарын машиналық оқыту және Explainable AI негізінде анықтау әдісін әзірлеу",

        researchPrototype:
            "Студенттік зерттеу прототипі",

        limitation:
            "Жүйе абсолютті қауіпсіздік кепілдігі емес. Жаңа немесе күрделі қайта тұжырымдалған шабуылдар қате жіктелуі мүмкін.",

        footerProject:
            "Prompt Injection анықтау жүйесі",

        footerUniversity:
            "Студенттік дипломдық жоба · Satbayev University",

        emptyText:
            "Талдау үшін мәтін енгізіңіз.",

        tooLong:
            "Мәтін 10 000 таңбадан аспауы керек.",

        analysisFailed:
            "Мәтінді талдау мүмкін болмады.",

        characters:
            "таңба"
    },


    ru: {

        brandSubtitle:
            "Безопасность многоязычных LLM",

        navPlayground:
            "Playground",

        navAnalytics:
            "Аналитика",

        navMethod:
            "Метод",

        modelActive:
            "Модель активна",

        heroCode:
            "01 / БЕЗОПАСНОСТЬ МНОГОЯЗЫЧНЫХ LLM",

        heroTitle:
            "Обнаружение Prompt Injection с помощью интерпретируемого ML",

        heroDescription:
            "Анализ LLM-запросов на казахском, русском и английском языках с помощью Hybrid TF-IDF, Linear SVM и Explainable AI.",

        openPlayground:
            "Открыть Playground",

        playgroundTitle:
            "Prompt Security Playground",

        playgroundDescription:
            "Отправьте реальный запрос модели и получите классификацию и XAI-объяснение.",

        promptPlaceholder:
            "Введите запрос для анализа...",

        privacy:
            "Текст не сохраняется в файл",

        analyze:
            "Анализировать",

        waiting:
            "ОЖИДАНИЕ",

        analyzing:
            "АНАЛИЗ",

        completed:
            "ГОТОВО",

        awaitingInput:
            "Ожидание запроса",

        awaitingDescription:
            "Здесь появятся классификация и XAI-результаты.",

        safeStatus:
            "NO PROMPT INJECTION",

        attackStatus:
            "PROMPT INJECTION",

        safeTitle:
            "Prompt Injection не обнаружен",

        attackTitle:
            "Обнаружен Prompt Injection",

        safeDescription:
            "Модель классифицировала текст как обычный пользовательский запрос.",

        attackDescription:
            "Модель обнаружила признаки попытки изменить предыдущие инструкции или их приоритет.",

        decisionScore:
            "DECISION SCORE",

        decisionBoundary:
            "DECISION BOUNDARY",

        classification:
            "Классификация",

        xaiTitle:
            "Explainable AI",

        xaiDescription:
            "Реальные текстовые признаки, повлиявшие на решение модели.",

        towardAttack:
            "В сторону Prompt Injection",

        towardSafe:
            "В сторону No Prompt Injection",

        noFeatures:
            "Выраженные признаки не найдены.",

        xaiNote:
            "XAI помогает интерпретировать решение модели, но не является доказательством полного семантического понимания текста.",

        analyticsTitle:
            "Оценка многоязычной модели",

        analyticsDescription:
            "Реальные экспериментальные результаты на закрытом multilingual test-наборе.",

        closedTest:
            "Закрытый тест",

        languagePerformance:
            "F1 по языкам",

        stressTest:
            "Robustness Stress Test",

        stressNote:
            "36 новых вручную составленных примеров. Они не использовались для переобучения модели или настройки threshold.",

        methodTitle:
            "Detection Pipeline",

        methodDescription:
            "Путь от пользовательского запроса до классификации и объяснения.",

        methodInput:
            "Ввод",

        methodInputDescription:
            "Многоязычный пользовательский запрос.",

        methodClassifier:
            "Бинарная классификация.",

        methodXai:
            "Локальный вклад признаков.",

        methodResearchNote:
            "Метод работает как независимый предварительный защитный слой до передачи запроса в LLM.",

        researchDetails:
            "Об исследовании",

        researchTitle:
            "Разработка метода обнаружения атак Prompt Injection в многоязычных LLM-системах на основе машинного обучения и Explainable AI",

        researchPrototype:
            "Студенческий исследовательский прототип",

        limitation:
            "Система не является абсолютной гарантией безопасности. Новые или сложно перефразированные атаки могут классифицироваться ошибочно.",

        footerProject:
            "Система обнаружения Prompt Injection",

        footerUniversity:
            "Студенческий дипломный проект · Satbayev University",

        emptyText:
            "Введите текст для анализа.",

        tooLong:
            "Текст не должен превышать 10 000 символов.",

        analysisFailed:
            "Не удалось выполнить анализ текста.",

        characters:
            "символов"
    },


    en: {

        brandSubtitle:
            "Multilingual LLM Security",

        navPlayground:
            "Playground",

        navAnalytics:
            "Analytics",

        navMethod:
            "Method",

        modelActive:
            "Model active",

        heroCode:
            "01 / MULTILINGUAL LLM SECURITY",

        heroTitle:
            "Detecting Prompt Injection with interpretable machine learning",

        heroDescription:
            "Analyze LLM prompts in Kazakh, Russian and English using Hybrid TF-IDF, Linear SVM and Explainable AI.",

        openPlayground:
            "Open Playground",

        playgroundTitle:
            "Prompt Security Playground",

        playgroundDescription:
            "Send a real prompt to the model and inspect its classification and XAI explanation.",

        promptPlaceholder:
            "Enter a prompt for analysis...",

        privacy:
            "Text is not saved to a file",

        analyze:
            "Analyze",

        waiting:
            "WAITING",

        analyzing:
            "ANALYZING",

        completed:
            "COMPLETE",

        awaitingInput:
            "Awaiting prompt",

        awaitingDescription:
            "Classification and XAI results will appear here.",

        safeStatus:
            "NO PROMPT INJECTION",

        attackStatus:
            "PROMPT INJECTION",

        safeTitle:
            "No Prompt Injection detected",

        attackTitle:
            "Prompt Injection detected",

        safeDescription:
            "The model classified the text as a normal user prompt.",

        attackDescription:
            "The model detected patterns associated with attempts to override or reprioritize previous instructions.",

        decisionScore:
            "DECISION SCORE",

        decisionBoundary:
            "DECISION BOUNDARY",

        classification:
            "Classification",

        xaiTitle:
            "Explainable AI",

        xaiDescription:
            "Actual text features that influenced the model decision.",

        towardAttack:
            "Toward Prompt Injection",

        towardSafe:
            "Toward No Prompt Injection",

        noFeatures:
            "No strong features were found.",

        xaiNote:
            "XAI helps interpret the model decision but does not demonstrate complete semantic understanding.",

        analyticsTitle:
            "Multilingual Model Evaluation",

        analyticsDescription:
            "Real experimental results from the closed multilingual test set.",

        closedTest:
            "Closed test",

        languagePerformance:
            "F1 by language",

        stressTest:
            "Robustness Stress Test",

        stressNote:
            "36 newly written manual examples. They were not used for retraining or threshold tuning.",

        methodTitle:
            "Detection Pipeline",

        methodDescription:
            "From multilingual user prompt to classification and explanation.",

        methodInput:
            "Input",

        methodInputDescription:
            "Multilingual user prompt.",

        methodClassifier:
            "Binary classification.",

        methodXai:
            "Local feature contributions.",

        methodResearchNote:
            "The method acts as an independent security layer before a user prompt is forwarded to an LLM.",

        researchDetails:
            "Research details",

        researchTitle:
            "Development of a Machine Learning and Explainable AI-Based Method for Detecting Prompt Injection Attacks in Multilingual LLM Systems",

        researchPrototype:
            "Student research prototype",

        limitation:
            "The system is not an absolute security guarantee. Novel or heavily paraphrased attacks may be misclassified.",

        footerProject:
            "Prompt Injection Detection System",

        footerUniversity:
            "Student bachelor project · Satbayev University",

        emptyText:
            "Enter text to analyze.",

        tooLong:
            "Text must not exceed 10,000 characters.",

        analysisFailed:
            "The text could not be analyzed.",

        characters:
            "characters"
    }
};


/* =========================================================
   STATE
========================================================= */

let currentLanguage =
    localStorage.getItem(
        "pi-shield-language"
    ) || "kk";


let lastResult = null;


/* =========================================================
   DOM
========================================================= */

const promptInput =
    document.getElementById(
        "promptInput"
    );

const analyzeButton =
    document.getElementById(
        "analyzeButton"
    );

const charCounter =
    document.getElementById(
        "charCounter"
    );

const errorMessage =
    document.getElementById(
        "errorMessage"
    );

const emptyAnalysis =
    document.getElementById(
        "emptyAnalysis"
    );

const analysisResult =
    document.getElementById(
        "analysisResult"
    );

const analysisStateLabel =
    document.getElementById(
        "analysisStateLabel"
    );

const resultStatusText =
    document.getElementById(
        "resultStatusText"
    );

const resultTitle =
    document.getElementById(
        "resultTitle"
    );

const resultDescription =
    document.getElementById(
        "resultDescription"
    );

const decisionScore =
    document.getElementById(
        "decisionScore"
    );

const classificationLabel =
    document.getElementById(
        "classificationLabel"
    );

const xaiSection =
    document.getElementById(
        "xaiSection"
    );

const positiveFeatures =
    document.getElementById(
        "positiveFeatures"
    );

const negativeFeatures =
    document.getElementById(
        "negativeFeatures"
    );


/* =========================================================
   TRANSLATION
========================================================= */

function t(key) {

    return (
        translations[currentLanguage][key]
        || key
    );
}


function applyTranslations() {

    document.documentElement.lang =
        currentLanguage;


    document
        .querySelectorAll(
            "[data-i18n]"
        )
        .forEach(
            element => {

                const key =
                    element.dataset.i18n;

                element.textContent =
                    t(key);
            }
        );


    document
        .querySelectorAll(
            "[data-i18n-placeholder]"
        )
        .forEach(
            element => {

                const key =
                    element.dataset.i18nPlaceholder;

                element.placeholder =
                    t(key);
            }
        );


    document
        .querySelectorAll(
            ".language-button"
        )
        .forEach(
            button => {

                button.classList.toggle(
                    "active",
                    button.dataset.language
                        === currentLanguage
                );
            }
        );


    updateCounter();


    if (lastResult) {

        renderResult(
            lastResult
        );
    }
}


/* =========================================================
   LANGUAGE
========================================================= */

document
    .querySelectorAll(
        ".language-button"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    currentLanguage =
                        button.dataset.language;

                    localStorage.setItem(
                        "pi-shield-language",
                        currentLanguage
                    );

                    applyTranslations();
                }
            );
        }
    );


/* =========================================================
   COUNTER
========================================================= */

function updateCounter() {

    charCounter.textContent =
        `${promptInput.value.length.toLocaleString()} / 10 000 ${t("characters")}`;
}


promptInput.addEventListener(
    "input",
    updateCounter
);


/* =========================================================
   ERROR
========================================================= */

function hideError() {

    errorMessage.classList.add(
        "hidden"
    );
}


function showError(message) {

    errorMessage.textContent =
        message;

    errorMessage.classList.remove(
        "hidden"
    );
}


/* =========================================================
   XAI FEATURES
========================================================= */

function renderFeatureList(
    container,
    features,
    type
) {

    container.replaceChildren();


    if (
        !Array.isArray(features)
        || features.length === 0
    ) {

        const empty =
            document.createElement(
                "div"
            );

        empty.className =
            "empty-features";

        empty.textContent =
            t("noFeatures");

        container.appendChild(
            empty
        );

        return;
    }


    const maxValue =
        Math.max(
            ...features.map(
                item =>
                    Math.abs(
                        Number(
                            item.contribution
                        )
                    )
            ),
            0.000001
        );


    features.forEach(
        item => {

            const contribution =
                Number(
                    item.contribution
                );


            const row =
                document.createElement(
                    "div"
                );

            row.className =
                "feature-row";


            const name =
                document.createElement(
                    "div"
                );

            name.className =
                "feature-name";

            name.textContent =
                String(
                    item.feature
                );

            name.title =
                String(
                    item.feature
                );


            const track =
                document.createElement(
                    "div"
                );

            track.className =
                "feature-track";


            const fill =
                document.createElement(
                    "div"
                );

            fill.className =
                `feature-fill ${type}`;


            const percentage =
                Math.max(
                    4,
                    (
                        Math.abs(
                            contribution
                        )
                        /
                        maxValue
                    )
                    * 100
                );


            fill.style.width =
                `${percentage}%`;


            track.appendChild(
                fill
            );


            const value =
                document.createElement(
                    "div"
                );

            value.className =
                "feature-value";

            value.textContent =
                contribution.toFixed(4);


            row.append(
                name,
                track,
                value
            );


            container.appendChild(
                row
            );
        }
    );
}


/* =========================================================
   RESULT
========================================================= */

function renderResult(data) {

    lastResult = data;


    const isAttack =
        Number(
            data.prediction
        ) === 1;


    emptyAnalysis.classList.add(
        "hidden"
    );


    analysisResult.classList.remove(
        "hidden",
        "safe",
        "attack"
    );


    analysisResult.classList.add(
        isAttack
            ? "attack"
            : "safe"
    );


    analysisStateLabel.textContent =
        t("completed");


    resultStatusText.textContent =
        isAttack
            ? t("attackStatus")
            : t("safeStatus");


    resultTitle.textContent =
        isAttack
            ? t("attackTitle")
            : t("safeTitle");


    resultDescription.textContent =
        isAttack
            ? t("attackDescription")
            : t("safeDescription");


    const score =
        Number(
            data.decision_score
        );


    decisionScore.textContent =
        (
            score > 0
                ? "+"
                : ""
        )
        +
        score.toFixed(4);


    classificationLabel.textContent =
        isAttack
            ? "Prompt Injection"
            : "No Prompt Injection";


    renderFeatureList(
        positiveFeatures,
        data.positive_features,
        "attack"
    );


    renderFeatureList(
        negativeFeatures,
        data.negative_features,
        "safe"
    );


    xaiSection.classList.remove(
        "hidden"
    );
}


/* =========================================================
   ANALYSIS
========================================================= */

async function analyzePrompt() {

    hideError();


    const text =
        promptInput.value.trim();


    if (!text) {

        showError(
            t("emptyText")
        );

        return;
    }


    if (text.length > 10000) {

        showError(
            t("tooLong")
        );

        return;
    }


    analyzeButton.disabled =
        true;


    analysisStateLabel.textContent =
        t("analyzing");


    xaiSection.classList.add(
        "hidden"
    );


    try {

        const response =
            await fetch(
                "/api/analyze",
                {
                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            {
                                text: text
                            }
                        )
                }
            );


        const data =
            await response.json();


        if (
            !response.ok
            || !data.ok
        ) {

            if (
                data.error ===
                "empty_text"
            ) {

                showError(
                    t("emptyText")
                );
            }

            else if (
                data.error ===
                "text_too_long"
            ) {

                showError(
                    t("tooLong")
                );
            }

            else {

                showError(
                    t("analysisFailed")
                );
            }


            analysisStateLabel.textContent =
                t("waiting");

            return;
        }


        renderResult(
            data
        );

    }

    catch {

        showError(
            t("analysisFailed")
        );


        analysisStateLabel.textContent =
            t("waiting");
    }

    finally {

        analyzeButton.disabled =
            false;
    }
}


/* =========================================================
   EVENTS
========================================================= */

analyzeButton.addEventListener(
    "click",
    analyzePrompt
);


promptInput.addEventListener(
    "keydown",
    event => {

        if (
            event.ctrlKey
            && event.key === "Enter"
        ) {

            event.preventDefault();

            analyzePrompt();
        }
    }
);


/* =========================================================
   RESEARCH DETAILS
========================================================= */

document
    .querySelectorAll(
        ".research-section details"
    )
    .forEach(
        details => {

            details.addEventListener(
                "toggle",
                () => {

                    const symbol =
                        details.querySelector(
                            ".details-symbol"
                        );

                    symbol.textContent =
                        details.open
                            ? "−"
                            : "+";
                }
            );
        }
    );


/* =========================================================
   INIT
========================================================= */

applyTranslations();

updateCounter();