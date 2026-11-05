import pandas as pd


def clean_feature_name(feature_name):
    feature_name = str(feature_name)

    if feature_name.startswith("word__"):
        return (
            "word",
            feature_name[
                len("word__"):
            ],
        )

    if feature_name.startswith("char__"):
        return (
            "char",
            feature_name[
                len("char__"):
            ],
        )

    return (
        "unknown",
        feature_name,
    )


def explain_text(
    pipeline,
    text,
    top_n=8,
):

    # --------------------------------------------------------
    # Получаем FeatureUnion и LinearSVC
    # --------------------------------------------------------

    if "features" not in pipeline.named_steps:
        raise ValueError(
            "Pipeline ішінде 'features' табылмады."
        )

    if "classifier" not in pipeline.named_steps:
        raise ValueError(
            "Pipeline ішінде 'classifier' табылмады."
        )

    features = pipeline.named_steps[
        "features"
    ]

    classifier = pipeline.named_steps[
        "classifier"
    ]

    if not hasattr(
        classifier,
        "coef_",
    ):
        raise ValueError(
            "Classifier linear coefficients бермейді."
        )

    # --------------------------------------------------------
    # Transform input
    # --------------------------------------------------------

    transformed = features.transform(
        [
            str(text)
        ]
    )

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = int(
        classifier.predict(
            transformed
        )[0]
    )

    decision_score = float(
        classifier.decision_function(
            transformed
        )[0]
    )

    # --------------------------------------------------------
    # Feature names + coefficients
    # --------------------------------------------------------

    feature_names = (
        features
        .get_feature_names_out()
    )

    coefficients = (
        classifier
        .coef_[0]
    )

    if (
        len(feature_names)
        != len(coefficients)
    ):
        raise ValueError(
            "Feature name және coefficient саны сәйкес емес."
        )

    # --------------------------------------------------------
    # Только активные признаки данного текста
    # --------------------------------------------------------

    row = transformed.getrow(
        0
    )

    active_indices = (
        row.indices
    )

    active_values = (
        row.data
    )

    contributions = (
        active_values
        * coefficients[
            active_indices
        ]
    )

    rows = []

    for (
        feature_index,
        tfidf_value,
        contribution,
    ) in zip(
        active_indices,
        active_values,
        contributions,
    ):

        raw_name = (
            feature_names[
                feature_index
            ]
        )

        feature_type, feature = (
            clean_feature_name(
                raw_name
            )
        )

        model_weight = float(
            coefficients[
                feature_index
            ]
        )

        contribution = float(
            contribution
        )

        rows.append(
            {
                "feature":
                    feature,

                "feature_type":
                    feature_type,

                "tfidf_value":
                    float(
                        tfidf_value
                    ),

                "weight":
                    model_weight,

                "contribution":
                    contribution,

                "direction":
                    (
                        "prompt_injection"
                        if contribution > 0
                        else "no_prompt_injection"
                    ),
            }
        )

    dataframe = pd.DataFrame(
        rows
    )

    # --------------------------------------------------------
    # Если активных признаков нет
    # --------------------------------------------------------

    if dataframe.empty:

        return {
            "prediction":
                prediction,

            "decision_score":
                decision_score,

            "positive":
                pd.DataFrame(
                    columns=[
                        "feature",
                        "feature_type",
                        "tfidf_value",
                        "weight",
                        "contribution",
                        "direction",
                    ]
                ),

            "negative":
                pd.DataFrame(
                    columns=[
                        "feature",
                        "feature_type",
                        "tfidf_value",
                        "weight",
                        "contribution",
                        "direction",
                    ]
                ),
        }

    # --------------------------------------------------------
    # Для UI сначала используем WORD-признаки:
    # они понятнее пользователю.
    #
    # Если word-признаков почему-то нет,
    # используем все активные признаки.
    # --------------------------------------------------------

    word_features = dataframe[
        dataframe[
            "feature_type"
        ] == "word"
    ].copy()

    if word_features.empty:
        explainable_features = (
            dataframe.copy()
        )

    else:
        explainable_features = (
            word_features
        )

    # --------------------------------------------------------
    # Positive contributions:
    # в сторону Prompt Injection
    # --------------------------------------------------------

    positive = (
        explainable_features[
            explainable_features[
                "contribution"
            ] > 0
        ]
        .sort_values(
            by="contribution",
            ascending=False,
        )
        .head(
            top_n
        )
        .reset_index(
            drop=True
        )
    )

    # --------------------------------------------------------
    # Negative contributions:
    # в сторону No Prompt Injection
    # --------------------------------------------------------

    negative = (
        explainable_features[
            explainable_features[
                "contribution"
            ] < 0
        ]
        .sort_values(
            by="contribution",
            ascending=True,
        )
        .head(
            top_n
        )
        .reset_index(
            drop=True
        )
    )

    return {
        "prediction":
            prediction,

        "decision_score":
            decision_score,

        "positive":
            positive,

        "negative":
            negative,
    }