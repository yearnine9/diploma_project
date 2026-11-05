from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODELS_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"

MODEL_PATH = (
    MODELS_DIR
    / "multilingual_final_model.joblib"
)

PREDICTIONS_PATH = (
    RESULTS_DIR
    / "multilingual_final_test_predictions.csv"
)

GLOBAL_FEATURES_PATH = (
    RESULTS_DIR
    / "multilingual_xai_global_features.csv"
)

GLOBAL_FIGURE_PATH = (
    RESULTS_DIR
    / "multilingual_xai_global_features.png"
)

LOCAL_EXPLANATIONS_PATH = (
    RESULTS_DIR
    / "multilingual_xai_local_explanations.csv"
)

LOCAL_SUMMARY_PATH = (
    RESULTS_DIR
    / "multilingual_xai_examples_summary.csv"
)


# ============================================================
# 2. SETTINGS
# ============================================================

TOP_GLOBAL = 20
TOP_LOCAL = 10

LANGUAGES = [
    "en",
    "kz",
    "ru",
]


# ============================================================
# 3. LOAD MODEL
# ============================================================

def load_model():

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            "multilingual_final_model.joblib табылмады."
        )

    package = joblib.load(
        MODEL_PATH
    )

    if "model" not in package:

        raise ValueError(
            "Model package ішінде 'model' жоқ."
        )

    model = package[
        "model"
    ]

    print("\n" + "=" * 72)
    print("MULTILINGUAL XAI")
    print("=" * 72)

    print(
        "Model:",
        package.get(
            "model_name",
            "unknown",
        )
    )

    print(
        "Task:",
        package.get(
            "task",
            "unknown",
        )
    )

    return package, model


# ============================================================
# 4. GET LINEAR COMPONENTS
# ============================================================

def get_model_components(
    model,
):

    if (
        "features"
        not in model.named_steps
    ):

        raise ValueError(
            "Pipeline ішінде 'features' табылмады."
        )

    if (
        "classifier"
        not in model.named_steps
    ):

        raise ValueError(
            "Pipeline ішінде 'classifier' табылмады."
        )

    features = model.named_steps[
        "features"
    ]

    classifier = model.named_steps[
        "classifier"
    ]

    if not hasattr(
        classifier,
        "coef_",
    ):

        raise ValueError(
            "Classifier linear coefficients бермейді."
        )

    feature_names = (
        features
        .get_feature_names_out()
    )

    coefficients = (
        classifier
        .coef_[
            0
        ]
    )

    if (
        len(feature_names)
        != len(coefficients)
    ):

        raise ValueError(
            "Feature name және coefficient саны сәйкес емес."
        )

    print(
        "Features:",
        len(
            feature_names
        )
    )

    return (
        features,
        classifier,
        feature_names,
        coefficients,
    )


# ============================================================
# 5. CLEAN FEATURE NAME
# ============================================================

def parse_feature(
    feature_name,
):

    feature_name = str(
        feature_name
    )

    if feature_name.startswith(
        "word__"
    ):

        return (
            "word",
            feature_name[
                len(
                    "word__"
                ):
            ],
        )

    if feature_name.startswith(
        "char__"
    ):

        return (
            "char",
            feature_name[
                len(
                    "char__"
                ):
            ],
        )

    return (
        "unknown",
        feature_name,
    )


# ============================================================
# 6. GLOBAL EXPLANATION
# ============================================================

def build_global_explanation(
    feature_names,
    coefficients,
):

    rows = []

    for feature_name, coefficient in zip(
        feature_names,
        coefficients,
    ):

        feature_type, feature = (
            parse_feature(
                feature_name
            )
        )

        rows.append(
            {
                "feature":
                    feature,

                "feature_type":
                    feature_type,

                "weight":
                    float(
                        coefficient
                    ),

                "direction":
                    (
                        "prompt_injection"
                        if coefficient > 0
                        else "no_prompt_injection"
                    ),
            }
        )

    dataframe = pd.DataFrame(
        rows
    )

    dataframe[
        "absolute_weight"
    ] = (
        dataframe[
            "weight"
        ]
        .abs()
    )

    dataframe = dataframe.sort_values(
        by="absolute_weight",
        ascending=False,
    ).reset_index(
        drop=True
    )

    dataframe.to_csv(
        GLOBAL_FEATURES_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("\n" + "=" * 72)
    print("GLOBAL XAI — TOP PROMPT INJECTION FEATURES")
    print("=" * 72)

    positive = (
        dataframe[
            dataframe[
                "weight"
            ] > 0
        ]
        .sort_values(
            "weight",
            ascending=False,
        )
        .head(
            TOP_GLOBAL
        )
    )

    print(
        positive[
            [
                "feature_type",
                "feature",
                "weight",
            ]
        ].to_string(
            index=False
        )
    )

    print("\n" + "=" * 72)
    print("GLOBAL XAI — TOP BENIGN FEATURES")
    print("=" * 72)

    negative = (
        dataframe[
            dataframe[
                "weight"
            ] < 0
        ]
        .sort_values(
            "weight",
            ascending=True,
        )
        .head(
            TOP_GLOBAL
        )
    )

    print(
        negative[
            [
                "feature_type",
                "feature",
                "weight",
            ]
        ].to_string(
            index=False
        )
    )

    return (
        dataframe,
        positive,
        negative,
    )


# ============================================================
# 7. GLOBAL FIGURE
# ============================================================

def save_global_figure(
    positive,
    negative,
):

    # Для картинки берём word-features,
    # потому что они легче интерпретируются в дипломе.

    positive_word = (
        positive[
            positive[
                "feature_type"
            ] == "word"
        ]
        .head(
            10
        )
        .copy()
    )

    negative_word = (
        negative[
            negative[
                "feature_type"
            ] == "word"
        ]
        .head(
            10
        )
        .copy()
    )

    plot_data = pd.concat(
        [
            negative_word,
            positive_word,
        ],
        ignore_index=True,
    )

    if len(
        plot_data
    ) == 0:

        print(
            "Word feature chart жасалмады: "
            "word features табылмады."
        )

        return

    plot_data = (
        plot_data
        .sort_values(
            "weight",
            ascending=True,
        )
    )

    fig, ax = plt.subplots(
        figsize=(
            10,
            8,
        )
    )

    ax.barh(
        plot_data[
            "feature"
        ],
        plot_data[
            "weight"
        ],
    )

    ax.axvline(
        0,
        linewidth=1,
    )

    ax.set_xlabel(
        "Linear SVM feature weight"
    )

    ax.set_ylabel(
        "Feature"
    )

    ax.set_title(
        "Global XAI: Multilingual Prompt Injection Detector"
    )

    plt.tight_layout()

    plt.savefig(
        GLOBAL_FIGURE_PATH,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(
        fig
    )


# ============================================================
# 8. LOCAL EXPLANATION
# ============================================================

def explain_text(
    text,
    features,
    classifier,
    feature_names,
    coefficients,
    top_n=TOP_LOCAL,
):

    transformed = features.transform(
        [
            str(
                text
            )
        ]
    )

    decision_score = float(
        classifier.decision_function(
            transformed
        )[
            0
        ]
    )

    prediction = int(
        classifier.predict(
            transformed
        )[
            0
        ]
    )

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
        *
        coefficients[
            active_indices
        ]
    )

    local_rows = []

    for feature_index, tfidf_value, contribution in zip(
        active_indices,
        active_values,
        contributions,
    ):

        raw_name = feature_names[
            feature_index
        ]

        feature_type, feature = (
            parse_feature(
                raw_name
            )
        )

        local_rows.append(
            {
                "feature":
                    feature,

                "feature_type":
                    feature_type,

                "tfidf_value":
                    float(
                        tfidf_value
                    ),

                "model_weight":
                    float(
                        coefficients[
                            feature_index
                        ]
                    ),

                "contribution":
                    float(
                        contribution
                    ),

                "direction":
                    (
                        "prompt_injection"
                        if contribution > 0
                        else "no_prompt_injection"
                    ),
            }
        )

    local = pd.DataFrame(
        local_rows
    )

    if len(
        local
    ) == 0:

        return {
            "prediction":
                prediction,

            "decision_score":
                decision_score,

            "positive":
                pd.DataFrame(),

            "negative":
                pd.DataFrame(),
        }

    positive = (
        local[
            local[
                "contribution"
            ] > 0
        ]
        .sort_values(
            "contribution",
            ascending=False,
        )
        .head(
            top_n
        )
    )

    negative = (
        local[
            local[
                "contribution"
            ] < 0
        ]
        .sort_values(
            "contribution",
            ascending=True,
        )
        .head(
            top_n
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


# ============================================================
# 9. LOAD FINAL TEST PREDICTIONS
# ============================================================

def load_predictions():

    if not PREDICTIONS_PATH.exists():

        raise FileNotFoundError(
            "multilingual_final_test_predictions.csv "
            "табылмады."
        )

    dataframe = pd.read_csv(
        PREDICTIONS_PATH
    )

    required = {
        "text",
        "label",
        "language",
        "predicted_label",
    }

    missing = (
        required
        - set(
            dataframe.columns
        )
    )

    if missing:

        raise ValueError(
            "Prediction file missing columns: "
            f"{sorted(missing)}"
        )

    return dataframe


# ============================================================
# 10. SELECT REPRESENTATIVE EXAMPLES
# ============================================================

def select_examples(
    predictions,
):

    selected_parts = []

    # --------------------------------------------------------
    # Выбираем первый корректно классифицированный
    # benign и attack пример каждого языка.
    #
    # Это используется только для post-hoc XAI,
    # а НЕ для настройки модели.
    # --------------------------------------------------------

    for language in LANGUAGES:

        language_data = predictions[
            predictions[
                "language"
            ] == language
        ].copy()

        for label in [
            0,
            1,
        ]:

            subset = language_data[
                (
                    language_data[
                        "label"
                    ] == label
                )
                &
                (
                    language_data[
                        "predicted_label"
                    ]
                    == label
                )
            ].copy()

            if len(
                subset
            ) == 0:

                print(
                    f"WARNING: "
                    f"{language}/{label} үшін "
                    f"correct example жоқ."
                )

                continue

            selected_parts.append(
                subset.head(
                    1
                )
            )

    if not selected_parts:

        raise ValueError(
            "XAI examples таңдалмады."
        )

    examples = pd.concat(
        selected_parts,
        ignore_index=True,
        sort=False,
    )

    return examples


# ============================================================
# 11. EXPLAIN REPRESENTATIVE EXAMPLES
# ============================================================

def explain_examples(
    examples,
    features,
    classifier,
    feature_names,
    coefficients,
):

    explanation_rows = []

    summary_rows = []

    for index, row in (
        examples.iterrows()
    ):

        example_id = (
            f"{row['language']}_"
            f"{int(row['label'])}_"
            f"{index + 1}"
        )

        explanation = explain_text(
            row[
                "text"
            ],
            features,
            classifier,
            feature_names,
            coefficients,
        )

        summary_rows.append(
            {
                "example_id":
                    example_id,

                "language":
                    row[
                        "language"
                    ],

                "true_label":
                    int(
                        row[
                            "label"
                        ]
                    ),

                "predicted_label":
                    int(
                        explanation[
                            "prediction"
                        ]
                    ),

                "decision_score":
                    explanation[
                        "decision_score"
                    ],

                "text":
                    row[
                        "text"
                    ],
            }
        )

        for direction_name in [
            "positive",
            "negative",
        ]:

            direction_df = explanation[
                direction_name
            ]

            if len(
                direction_df
            ) == 0:

                continue

            for rank, (
                _,
                feature_row,
            ) in enumerate(
                direction_df.iterrows(),
                start=1,
            ):

                explanation_rows.append(
                    {
                        "example_id":
                            example_id,

                        "language":
                            row[
                                "language"
                            ],

                        "true_label":
                            int(
                                row[
                                    "label"
                                ]
                            ),

                        "predicted_label":
                            int(
                                explanation[
                                    "prediction"
                                ]
                            ),

                        "decision_score":
                            explanation[
                                "decision_score"
                            ],

                        "evidence":
                            direction_name,

                        "rank":
                            rank,

                        "feature_type":
                            feature_row[
                                "feature_type"
                            ],

                        "feature":
                            feature_row[
                                "feature"
                            ],

                        "tfidf_value":
                            feature_row[
                                "tfidf_value"
                            ],

                        "model_weight":
                            feature_row[
                                "model_weight"
                            ],

                        "contribution":
                            feature_row[
                                "contribution"
                            ],
                    }
                )

    summary = pd.DataFrame(
        summary_rows
    )

    explanations = pd.DataFrame(
        explanation_rows
    )

    summary.to_csv(
        LOCAL_SUMMARY_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    explanations.to_csv(
        LOCAL_EXPLANATIONS_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    return (
        summary,
        explanations,
    )


# ============================================================
# 12. PRINT LOCAL EXAMPLES
# ============================================================

def print_local_examples(
    summary,
    explanations,
):

    print("\n" + "=" * 72)
    print("LOCAL XAI EXAMPLES")
    print("=" * 72)

    for _, example in (
        summary.iterrows()
    ):

        example_id = example[
            "example_id"
        ]

        print("\n" + "-" * 72)

        print(
            "Example:",
            example_id
        )

        print(
            "Language:",
            example[
                "language"
            ]
        )

        print(
            "True label:",
            int(
                example[
                    "true_label"
                ]
            )
        )

        print(
            "Prediction:",
            int(
                example[
                    "predicted_label"
                ]
            )
        )

        print(
            "Decision score:",
            f"{example['decision_score']:.4f}"
        )

        example_features = explanations[
            explanations[
                "example_id"
            ] == example_id
        ]

        positive = example_features[
            example_features[
                "evidence"
            ] == "positive"
        ]

        negative = example_features[
            example_features[
                "evidence"
            ] == "negative"
        ]

        print(
            "\nTop evidence for Prompt Injection:"
        )

        if len(
            positive
        ) > 0:

            print(
                positive[
                    [
                        "feature_type",
                        "feature",
                        "contribution",
                    ]
                ]
                .head(
                    5
                )
                .to_string(
                    index=False
                )
            )

        else:

            print(
                "No positive active features."
            )

        print(
            "\nTop evidence for No Prompt Injection:"
        )

        if len(
            negative
        ) > 0:

            print(
                negative[
                    [
                        "feature_type",
                        "feature",
                        "contribution",
                    ]
                ]
                .head(
                    5
                )
                .to_string(
                    index=False
                )
            )

        else:

            print(
                "No negative active features."
            )


# ============================================================
# 13. MAIN
# ============================================================

def main():

    try:

        RESULTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        (
            package,
            model,
        ) = load_model()

        (
            features,
            classifier,
            feature_names,
            coefficients,
        ) = get_model_components(
            model
        )

        (
            global_features,
            positive,
            negative,
        ) = build_global_explanation(
            feature_names,
            coefficients,
        )

        save_global_figure(
            positive,
            negative,
        )

        predictions = (
            load_predictions()
        )

        examples = (
            select_examples(
                predictions
            )
        )

        (
            summary,
            explanations,
        ) = explain_examples(
            examples,
            features,
            classifier,
            feature_names,
            coefficients,
        )

        print_local_examples(
            summary,
            explanations,
        )

        print("\n" + "=" * 72)
        print("XAI FILES SAVED")
        print("=" * 72)

        print(
            GLOBAL_FEATURES_PATH.name
        )

        print(
            GLOBAL_FIGURE_PATH.name
        )

        print(
            LOCAL_EXPLANATIONS_PATH.name
        )

        print(
            LOCAL_SUMMARY_PATH.name
        )

        print("\nМаңызды:")
        print(
            "Decision score — probability емес."
        )

        print(
            "Positive score → Prompt Injection жағына."
        )

        print(
            "Negative score → No Prompt Injection жағына."
        )

        print("\n" + "=" * 72)
        print("XAI STAGE COMPLETED")
        print("=" * 72)

    except Exception as error:

        print(
            "\nҚате пайда болды:"
        )

        print(error)

        raise


if __name__ == "__main__":
    main()