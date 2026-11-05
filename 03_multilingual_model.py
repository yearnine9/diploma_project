from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"
RESULTS_DIR = BASE_DIR / "results"
MODELS_DIR = BASE_DIR / "models"

LOCK_PATH = (
    RESULTS_DIR
    / "multilingual_final_test.lock"
)

FINAL_MODEL_PATH = (
    MODELS_DIR
    / "multilingual_final_model.joblib"
)

FINAL_RESULTS_PATH = (
    RESULTS_DIR
    / "multilingual_final_test_results.csv"
)

FINAL_PREDICTIONS_PATH = (
    RESULTS_DIR
    / "multilingual_final_test_predictions.csv"
)

COMBINED_CM_PATH = (
    RESULTS_DIR
    / "multilingual_final_confusion_matrix.png"
)


# ============================================================
# 2. SETTINGS
# ============================================================

RANDOM_STATE = 42

SELECTED_MODEL_NAME = (
    "multilingual_hybrid_word_char_linear_svm"
)

LANGUAGE_ORDER = [
    "en",
    "kz",
    "ru",
]


# ============================================================
# 3. FILE RESOLVER
# ============================================================

def resolve_file(
    candidates,
    description,
):

    for filename in candidates:

        path = (
            PROCESSED_DIR
            / filename
        )

        if path.exists():
            return path

    raise FileNotFoundError(
        f"{description} табылмады. "
        f"Candidates: {candidates}"
    )


# ============================================================
# 4. RESOLVE DATASETS
# ============================================================

def resolve_dataset_paths():

    paths = {

        "en_train": resolve_file(
            [
                "english_train_primary.csv",
            ],
            "English train",
        ),

        "en_validation": resolve_file(
            [
                "english_validation_primary.csv",
            ],
            "English validation",
        ),

        "en_test": resolve_file(
            [
                "english_test_primary.csv",
            ],
            "English test",
        ),

        "kz_train": resolve_file(
            [
                "kazakh_train_final.csv",
                "kz_train_final.csv",
            ],
            "Kazakh train",
        ),

        "kz_validation": resolve_file(
            [
                "kazakh_validation_final.csv",
                "kz_validation_final.csv",
            ],
            "Kazakh validation",
        ),

        "kz_test": resolve_file(
            [
                "kazakh_test_final.csv",
                "kz_test_final.csv",
            ],
            "Kazakh test",
        ),

        "ru_train": resolve_file(
            [
                "russian_train_final.csv",
            ],
            "Russian train",
        ),

        "ru_validation": resolve_file(
            [
                "russian_validation_final.csv",
            ],
            "Russian validation",
        ),

        "ru_test": resolve_file(
            [
                "russian_test_final.csv",
            ],
            "Russian test",
        ),
    }

    print("\n" + "=" * 72)
    print("RESOLVED FINAL DATASETS")
    print("=" * 72)

    for name, path in (
        paths.items()
    ):

        print(
            f"{name}: "
            f"{path.name}"
        )

    return paths


# ============================================================
# 5. LOAD ONE SPLIT
# ============================================================

def load_split(
    path,
    language,
    split_name,
):

    dataframe = pd.read_csv(
        path
    )

    required = {
        "text",
        "label",
    }

    missing = (
        required
        - set(
            dataframe.columns
        )
    )

    if missing:

        raise ValueError(
            f"{path.name}: "
            f"missing columns "
            f"{sorted(missing)}"
        )

    dataframe = dataframe[
        [
            "text",
            "label",
        ]
    ].copy()

    if dataframe[
        "text"
    ].isna().any():

        raise ValueError(
            f"{path.name}: "
            f"text ішінде NaN бар."
        )

    dataframe[
        "text"
    ] = (
        dataframe[
            "text"
        ]
        .astype(str)
        .str.strip()
    )

    dataframe[
        "label"
    ] = (
        dataframe[
            "label"
        ]
        .astype(int)
    )

    invalid = (
        set(
            dataframe[
                "label"
            ].unique()
        )
        - {
            0,
            1,
        }
    )

    if invalid:

        raise ValueError(
            f"{path.name}: "
            f"invalid labels "
            f"{invalid}"
        )

    dataframe[
        "language"
    ] = language

    dataframe[
        "split"
    ] = split_name

    return dataframe


# ============================================================
# 6. LOAD FINAL DATA
# ============================================================

def load_final_data(
    paths,
):

    training_parts = []

    test_parts = []

    # English
    training_parts.append(
        load_split(
            paths[
                "en_train"
            ],
            "en",
            "train",
        )
    )

    training_parts.append(
        load_split(
            paths[
                "en_validation"
            ],
            "en",
            "validation",
        )
    )

    test_parts.append(
        load_split(
            paths[
                "en_test"
            ],
            "en",
            "test",
        )
    )

    # Kazakh
    training_parts.append(
        load_split(
            paths[
                "kz_train"
            ],
            "kz",
            "train",
        )
    )

    training_parts.append(
        load_split(
            paths[
                "kz_validation"
            ],
            "kz",
            "validation",
        )
    )

    test_parts.append(
        load_split(
            paths[
                "kz_test"
            ],
            "kz",
            "test",
        )
    )

    # Russian
    training_parts.append(
        load_split(
            paths[
                "ru_train"
            ],
            "ru",
            "train",
        )
    )

    training_parts.append(
        load_split(
            paths[
                "ru_validation"
            ],
            "ru",
            "validation",
        )
    )

    test_parts.append(
        load_split(
            paths[
                "ru_test"
            ],
            "ru",
            "test",
        )
    )

    train_full = pd.concat(
        training_parts,
        ignore_index=True,
        sort=False,
    )

    test = pd.concat(
        test_parts,
        ignore_index=True,
        sort=False,
    )

    return (
        train_full,
        test,
    )


# ============================================================
# 7. DATA DISTRIBUTION
# ============================================================

def show_distribution(
    dataframe,
    title,
):

    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

    table = (
        dataframe
        .groupby(
            [
                "language",
                "label",
            ]
        )
        .size()
        .unstack(
            fill_value=0
        )
    )

    print(
        table
    )

    print(
        "\nTotal:",
        len(dataframe)
    )


# ============================================================
# 8. LANGUAGE × CLASS SAMPLE WEIGHTS
# ============================================================

def add_sample_weights(
    dataframe,
):

    dataframe = (
        dataframe
        .copy()
    )

    counts = (
        dataframe
        .groupby(
            [
                "language",
                "label",
            ]
        )
        .size()
        .to_dict()
    )

    group_count = len(
        counts
    )

    target_total = (
        len(dataframe)
        / group_count
    )

    weights = []

    for _, row in (
        dataframe.iterrows()
    ):

        key = (
            row[
                "language"
            ],
            int(
                row[
                    "label"
                ]
            ),
        )

        weight = (
            target_total
            / counts[
                key
            ]
        )

        weights.append(
            weight
        )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    weights = (
        weights
        / weights.mean()
    )

    dataframe[
        "sample_weight"
    ] = weights

    print("\n" + "=" * 72)
    print("FINAL TRAINING SAMPLE WEIGHTS")
    print("=" * 72)

    print(
        dataframe
        .groupby(
            [
                "language",
                "label",
            ]
        )[
            "sample_weight"
        ]
        .agg(
            [
                "count",
                "mean",
                "sum",
            ]
        )
    )

    return dataframe


# ============================================================
# 9. FINAL FIXED MODEL
# ============================================================

def build_final_model():

    word_features = TfidfVectorizer(
        analyzer="word",
        ngram_range=(
            1,
            2,
        ),
        lowercase=True,
        min_df=2,
        max_df=0.98,
        sublinear_tf=True,
    )

    char_features = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(
            3,
            5,
        ),
        lowercase=True,
        min_df=2,
        max_df=0.98,
        sublinear_tf=True,
    )

    model = Pipeline(
        [
            (
                "features",
                FeatureUnion(
                    [
                        (
                            "word",
                            word_features,
                        ),
                        (
                            "char",
                            char_features,
                        ),
                    ]
                ),
            ),

            (
                "classifier",
                LinearSVC(
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )

    return model


# ============================================================
# 10. METRICS
# ============================================================

def calculate_metrics(
    y_true,
    y_pred,
):

    tn, fp, fn, tp = (
        confusion_matrix(
            y_true,
            y_pred,
            labels=[
                0,
                1,
            ],
        )
        .ravel()
    )

    fpr = (
        fp
        / (
            fp
            + tn
        )
        if (
            fp
            + tn
        ) > 0
        else 0.0
    )

    return {
        "accuracy":
            accuracy_score(
                y_true,
                y_pred,
            ),

        "precision":
            precision_score(
                y_true,
                y_pred,
                zero_division=0,
            ),

        "recall":
            recall_score(
                y_true,
                y_pred,
                zero_division=0,
            ),

        "f1":
            f1_score(
                y_true,
                y_pred,
                zero_division=0,
            ),

        "fpr":
            fpr,

        "tn":
            int(tn),

        "fp":
            int(fp),

        "fn":
            int(fn),

        "tp":
            int(tp),
    }


# ============================================================
# 11. CONFUSION MATRIX
# ============================================================

def save_confusion_matrix(
    y_true,
    y_pred,
    title,
    output_path,
):

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=[
            0,
            1,
        ],
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=[
            "No Prompt Injection",
            "Prompt Injection",
        ],
    )

    fig, ax = plt.subplots(
        figsize=(
            7,
            6,
        )
    )

    display.plot(
        ax=ax,
        values_format="d",
    )

    ax.set_title(
        title
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(
        fig
    )


# ============================================================
# 12. FINAL TEST EVALUATION
# ============================================================

def evaluate_final_test(
    model,
    test,
):

    prediction = model.predict(
        test[
            "text"
        ].astype(str)
    )

    evaluated = (
        test.copy()
    )

    evaluated[
        "predicted_label"
    ] = prediction

    evaluated[
        "correct"
    ] = (
        evaluated[
            "label"
        ]
        ==
        evaluated[
            "predicted_label"
        ]
    )

    rows = []

    f1_values = []
    fpr_values = []

    print("\n" + "=" * 72)
    print("FINAL MULTILINGUAL CLOSED TEST")
    print("=" * 72)

    for language in LANGUAGE_ORDER:

        subset = evaluated[
            evaluated[
                "language"
            ] == language
        ].copy()

        metrics = calculate_metrics(
            subset[
                "label"
            ].astype(int),
            subset[
                "predicted_label"
            ].astype(int),
        )

        f1_values.append(
            metrics[
                "f1"
            ]
        )

        fpr_values.append(
            metrics[
                "fpr"
            ]
        )

        rows.append(
            {
                "scope":
                    language,

                **metrics,
            }
        )

        print(
            f"{language.upper()} | "
            f"Accuracy={metrics['accuracy']:.4f} | "
            f"Precision={metrics['precision']:.4f} | "
            f"Recall={metrics['recall']:.4f} | "
            f"F1={metrics['f1']:.4f} | "
            f"FPR={metrics['fpr']:.4f} | "
            f"TN={metrics['tn']} | "
            f"FP={metrics['fp']} | "
            f"FN={metrics['fn']} | "
            f"TP={metrics['tp']}"
        )

        save_confusion_matrix(
            subset[
                "label"
            ].astype(int),

            subset[
                "predicted_label"
            ].astype(int),

            (
                f"Multilingual Prompt Injection Detector\n"
                f"{language.upper()} Closed Test"
            ),

            RESULTS_DIR
            / (
                f"multilingual_final_"
                f"{language}_confusion_matrix.png"
            ),
        )

    combined_metrics = calculate_metrics(
        evaluated[
            "label"
        ].astype(int),
        evaluated[
            "predicted_label"
        ].astype(int),
    )

    macro_f1 = float(
        np.mean(
            f1_values
        )
    )

    macro_fpr = float(
        np.mean(
            fpr_values
        )
    )

    rows.append(
        {
            "scope":
                "combined",

            **combined_metrics,
        }
    )

    rows.append(
        {
            "scope":
                "macro_languages",

            "accuracy":
                np.nan,

            "precision":
                np.nan,

            "recall":
                np.nan,

            "f1":
                macro_f1,

            "fpr":
                macro_fpr,

            "tn":
                np.nan,

            "fp":
                np.nan,

            "fn":
                np.nan,

            "tp":
                np.nan,
        }
    )

    print("\n" + "-" * 72)

    print(
        f"Macro-F1 : "
        f"{macro_f1:.4f}"
    )

    print(
        f"Macro-FPR: "
        f"{macro_fpr:.4f}"
    )

    print(
        f"Combined Accuracy: "
        f"{combined_metrics['accuracy']:.4f}"
    )

    print(
        f"Combined F1      : "
        f"{combined_metrics['f1']:.4f}"
    )

    print(
        f"Combined FPR     : "
        f"{combined_metrics['fpr']:.4f}"
    )

    save_confusion_matrix(
        evaluated[
            "label"
        ].astype(int),

        evaluated[
            "predicted_label"
        ].astype(int),

        (
            "Multilingual Prompt Injection Detector\n"
            "Combined Closed Test"
        ),

        COMBINED_CM_PATH,
    )

    return (
        pd.DataFrame(
            rows
        ),
        evaluated,
        macro_f1,
        macro_fpr,
        combined_metrics,
    )


# ============================================================
# 13. LOCK
# ============================================================

def check_lock():

    if LOCK_PATH.exists():

        print("\n" + "=" * 72)
        print("FINAL TEST ALREADY COMPLETED")
        print("=" * 72)

        print(
            "multilingual_final_test.lock табылды."
        )

        print(
            "Closed test қайта іске қосылмайды."
        )

        raise RuntimeError(
            "Final multilingual test already locked."
        )


def create_lock():

    LOCK_PATH.write_text(
        (
            "FINAL MULTILINGUAL CLOSED TEST COMPLETED\n"
            f"Model: {SELECTED_MODEL_NAME}\n"
            "Do not reuse the closed test for tuning.\n"
        ),
        encoding="utf-8",
    )


# ============================================================
# 14. MAIN
# ============================================================

def main():

    try:

        RESULTS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        MODELS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Защита от случайного повторного открытия test.
        check_lock()

        paths = resolve_dataset_paths()

        (
            train_full,
            test,
        ) = load_final_data(
            paths
        )

        show_distribution(
            train_full,
            "FINAL TRAIN + VALIDATION DISTRIBUTION",
        )

        show_distribution(
            test,
            "CLOSED TEST DISTRIBUTION",
        )

        train_full = (
            add_sample_weights(
                train_full
            )
        )

        print("\n" + "=" * 72)
        print("FIXED MULTILINGUAL ARCHITECTURE")
        print("=" * 72)

        print(
            SELECTED_MODEL_NAME
        )

        print(
            "Selection basis: "
            "validation Macro-F1 = 0.9904"
        )

        model = build_final_model()

        print(
            "\nTraining final multilingual model..."
        )

        model.fit(
            train_full[
                "text"
            ].astype(str),

            train_full[
                "label"
            ].astype(int),

            classifier__sample_weight=(
                train_full[
                    "sample_weight"
                ].values
            ),
        )

        print(
            "Training completed."
        )

        (
            final_results,
            predictions,
            macro_f1,
            macro_fpr,
            combined_metrics,
        ) = evaluate_final_test(
            model,
            test,
        )

        # ----------------------------------------------------
        # SAVE RESULTS
        # ----------------------------------------------------

        final_results.to_csv(
            FINAL_RESULTS_PATH,
            index=False,
            encoding="utf-8-sig",
        )

        predictions.to_csv(
            FINAL_PREDICTIONS_PATH,
            index=False,
            encoding="utf-8-sig",
        )

        model_package = {
            "model":
                model,

            "model_name":
                SELECTED_MODEL_NAME,

            "languages":
                [
                    "en",
                    "kz",
                    "ru",
                ],

            "task":
                "multilingual_prompt_injection_detection",

            "features":
                "word_tfidf_plus_char_tfidf",

            "classifier":
                "LinearSVC",

            "training_data":
                "train_plus_validation_all_languages",

            "language_class_balanced_training":
                True,

            "selection_metric":
                "validation_macro_f1",

            "validation_macro_f1":
                0.9904,

            "final_test_macro_f1":
                macro_f1,

            "final_test_macro_fpr":
                macro_fpr,

            "final_test_combined_f1":
                combined_metrics[
                    "f1"
                ],

            "label_mapping": {
                0:
                    "no_prompt_injection",

                1:
                    "prompt_injection",
            },

            "test_used_for_model_selection":
                False,

            "closed_test_completed":
                True,
        }

        joblib.dump(
            model_package,
            FINAL_MODEL_PATH,
        )

        # Lock создаём только после
        # успешного сохранения результатов.
        create_lock()

        print("\n" + "=" * 72)
        print("FINAL FILES SAVED")
        print("=" * 72)

        print(
            "multilingual_final_model.joblib"
        )

        print(
            "multilingual_final_test_results.csv"
        )

        print(
            "multilingual_final_test_predictions.csv"
        )

        print(
            "multilingual_final_confusion_matrix.png"
        )

        print(
            "multilingual_final_en_confusion_matrix.png"
        )

        print(
            "multilingual_final_kz_confusion_matrix.png"
        )

        print(
            "multilingual_final_ru_confusion_matrix.png"
        )

        print(
            "multilingual_final_test.lock"
        )

        print("\n" + "=" * 72)
        print("MULTILINGUAL STAGE COMPLETED")
        print("=" * 72)

        print(
            "Closed multilingual test is now locked."
        )

    except Exception as error:

        print(
            "\nҚате пайда болды:"
        )

        print(error)

        raise


if __name__ == "__main__":
    main()