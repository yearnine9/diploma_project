from flask import Flask, jsonify, render_template, request

from app.predictor import MultilingualPromptInjectionDetector


# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)


# Ограничиваем максимальный размер входящего запроса.
# Пользовательский текст дополнительно ограничен 10 000 символами.
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024


# ============================================================
# MODEL
# ============================================================

detector = MultilingualPromptInjectionDetector()


# ============================================================
# HELPERS
# ============================================================

def dataframe_to_records(dataframe):
    """
    Преобразует XAI DataFrame в безопасный для JSON список.

    Во frontend передаются только:
    - feature
    - contribution

    Внутренние параметры модели не раскрываются.
    """

    if dataframe is None:
        return []

    if dataframe.empty:
        return []

    records = []

    for _, row in dataframe.iterrows():

        records.append(
            {
                "feature": str(
                    row["feature"]
                ),

                "contribution": float(
                    row["contribution"]
                ),
            }
        )

    return records


# ============================================================
# MAIN PAGE
# ============================================================

@app.route("/")
def index():
    """
    Главная страница веб-приложения.
    """

    return render_template(
        "index.html"
    )


# ============================================================
# ANALYSIS API
# ============================================================

@app.route(
    "/api/analyze",
    methods=["POST"],
)
def analyze():
    """
    Получает пользовательский текст,
    выполняет классификацию и возвращает:

    - prediction
    - label
    - decision_score
    - positive XAI features
    - negative XAI features
    """

    try:

        # ----------------------------------------------------
        # READ JSON
        # ----------------------------------------------------

        payload = request.get_json(
            silent=True
        )

        if not isinstance(
            payload,
            dict,
        ):

            return jsonify(
                {
                    "ok": False,
                    "error": "invalid_request",
                }
            ), 400


        # ----------------------------------------------------
        # TEXT VALIDATION
        # ----------------------------------------------------

        text = str(
            payload.get(
                "text",
                ""
            )
        ).strip()


        if not text:

            return jsonify(
                {
                    "ok": False,
                    "error": "empty_text",
                }
            ), 400


        if len(text) > 10000:

            return jsonify(
                {
                    "ok": False,
                    "error": "text_too_long",
                }
            ), 400


        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        result = detector.predict(
            text
        )


        # ----------------------------------------------------
        # XAI
        # ----------------------------------------------------

        positive_features = (
            dataframe_to_records(
                result[
                    "positive_features"
                ]
            )
        )

        negative_features = (
            dataframe_to_records(
                result[
                    "negative_features"
                ]
            )
        )


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify(
            {
                "ok": True,

                "prediction": int(
                    result[
                        "prediction"
                    ]
                ),

                "label": str(
                    result[
                        "label"
                    ]
                ),

                "decision_score": float(
                    result[
                        "decision_score"
                    ]
                ),

                "positive_features":
                    positive_features,

                "negative_features":
                    negative_features,
            }
        )


    except Exception:

        # Не передаём пользователю:
        # - traceback
        # - локальные пути
        # - внутренние ошибки модели
        # - структуру файлов проекта

        return jsonify(
            {
                "ok": False,
                "error": "analysis_failed",
            }
        ), 500


# ============================================================
# REQUEST TOO LARGE
# ============================================================

@app.errorhandler(413)
def request_too_large(error):

    return jsonify(
        {
            "ok": False,
            "error": "request_too_large",
        }
    ), 413


# ============================================================
# NOT FOUND
# ============================================================

@app.errorhandler(404)
def not_found(error):

    # Для неизвестных API-маршрутов возвращаем JSON.
    if request.path.startswith(
        "/api/"
    ):

        return jsonify(
            {
                "ok": False,
                "error": "not_found",
            }
        ), 404

    return (
        "Page not found",
        404,
    )


# ============================================================
# SECURITY HEADERS
# ============================================================

@app.after_request
def add_security_headers(response):
    """
    Базовые security headers для локального web-прототипа.
    """

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"

    response.headers[
        "X-Frame-Options"
    ] = "DENY"

    response.headers[
        "Referrer-Policy"
    ] = "no-referrer"

    response.headers[
        "Cache-Control"
    ] = (
        "no-store, no-cache, "
        "must-revalidate, max-age=0"
    )

    response.headers[
        "Pragma"
    ] = "no-cache"

    return response


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )