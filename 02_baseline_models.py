from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.base import clone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


# ============================================================
# 1. ПУТИ ПРОЕКТА
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. ФАЙЛЫ ДАТАСЕТА
# ============================================================

TRAIN_PATH = PROCESSED_DATA_DIR / "english_train_primary.csv"
VALIDATION_PATH = PROCESSED_DATA_DIR / "english_validation_primary.csv"
TEST_PATH = PROCESSED_DATA_DIR / "english_test_primary.csv"


# ============================================================
# 3. ЗАГРУЗКА ДАННЫХ
# ============================================================

def load_data():
    print("Деректер жүктелуде...")

    required_files = [
        TRAIN_PATH,
        VALIDATION_PATH,
        TEST_PATH,
    ]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Файл табылмады: {file_path.name}"
            )

    train_df = pd.read_csv(TRAIN_PATH)
    validation_df = pd.read_csv(VALIDATION_PATH)
    test_df = pd.read_csv(TEST_PATH)

    required_columns = {"text", "label"}

    for name, dataframe in [
        ("train", train_df),
        ("validation", validation_df),
        ("test", test_df),
    ]:
        missing_columns = (
            required_columns - set(dataframe.columns)
        )

        if missing_columns:
            raise ValueError(
                f"{name} ішінде қажетті бағандар жоқ: "
                f"{sorted(missing_columns)}"
            )

        if dataframe["text"].isnull().any():
            raise ValueError(
                f"{name} ішінде бос мәтіндер табылды."
            )

        labels = set(dataframe["label"].unique())

        if not labels.issubset({0, 1}):
            raise ValueError(
                f"{name} ішінде белгісіз label бар: {labels}"
            )

    print("Деректер сәтті жүктелді.")
    print("Train:", len(train_df))
    print("Validation:", len(validation_df))
    print("Test:", len(test_df))

    return train_df, validation_df, test_df


# ============================================================
# 4. BASELINE МОДЕЛЬДЕР
# ============================================================

def create_models():
    models = {
        "Logistic Regression": Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        ngram_range=(1, 2),
                        min_df=2,
                        max_df=0.98,
                        sublinear_tf=True,
                    ),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=1000,
                        random_state=42,
                    ),
                ),
            ]
        ),

        "Linear SVM": Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        ngram_range=(1, 2),
                        min_df=2,
                        max_df=0.98,
                        sublinear_tf=True,
                    ),
                ),
                (
                    "classifier",
                    LinearSVC(
                        random_state=42,
                    ),
                ),
            ]
        ),
    }

    return models


# ============================================================
# 5. МЕТРИКИ
# ============================================================

def calculate_metrics(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    accuracy = accuracy_score(y_true, y_pred)

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    if (fp + tn) > 0:
        false_positive_rate = fp / (fp + tn)
    else:
        false_positive_rate = 0.0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "false_positive_rate": false_positive_rate,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


# ============================================================
# 6. VALIDATION БОЙЫНША МОДЕЛЬДЕРДІ САЛЫСТЫРУ
# ============================================================

def compare_models(
    models,
    train_df,
    validation_df,
):
    print("\n" + "=" * 60)
    print("BASELINE МОДЕЛЬДЕРДІ САЛЫСТЫРУ")
    print("=" * 60)

    X_train = train_df["text"].astype(str)
    y_train = train_df["label"]

    X_validation = validation_df["text"].astype(str)
    y_validation = validation_df["label"]

    results = []

    for model_name, model in models.items():
        print(f"\nМодель: {model_name}")

        model.fit(
            X_train,
            y_train,
        )

        predictions = model.predict(
            X_validation
        )

        metrics = calculate_metrics(
            y_validation,
            predictions,
        )

        print(
            f"Accuracy: {metrics['accuracy']:.4f}"
        )
        print(
            f"Precision: {metrics['precision']:.4f}"
        )
        print(
            f"Recall: {metrics['recall']:.4f}"
        )
        print(
            f"F1-score: {metrics['f1_score']:.4f}"
        )
        print(
            "False Positive Rate: "
            f"{metrics['false_positive_rate']:.4f}"
        )

        results.append(
            {
                "model": model_name,
                **metrics,
            }
        )

    results_df = pd.DataFrame(results)

    output_path = (
        RESULTS_DIR
        / "baseline_validation_results.csv"
    )

    results_df.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
    )

    print(
        "\nValidation нәтижелері "
        "results бумасына сақталды."
    )

    return results_df


# ============================================================
# 7. ЕҢ ЖАҚСЫ МОДЕЛЬДІ ТАҢДАУ
# ============================================================

def select_best_model(results_df):
    best_row = results_df.loc[
        results_df["f1_score"].idxmax()
    ]

    best_model_name = best_row["model"]

    print("\n" + "=" * 60)
    print("ЕҢ ЖАҚСЫ BASELINE МОДЕЛЬ")
    print("=" * 60)

    print("Модель:", best_model_name)
    print(
        "Validation F1-score:",
        f"{best_row['f1_score']:.4f}",
    )

    return best_model_name


# ============================================================
# 8. FINAL МОДЕЛЬ ЖӘНЕ TEST
# ============================================================

def train_and_test_best_model(
    models,
    best_model_name,
    train_df,
    validation_df,
    test_df,
):
    print("\n" + "=" * 60)
    print("TEST ЖИЫНЫНДАҒЫ ҚОРЫТЫНДЫ БАҒАЛАУ")
    print("=" * 60)

    combined_df = pd.concat(
        [
            train_df,
            validation_df,
        ],
        ignore_index=True,
    )

    X_train_final = combined_df["text"].astype(str)
    y_train_final = combined_df["label"]

    X_test = test_df["text"].astype(str)
    y_test = test_df["label"]

    final_model = clone(
        models[best_model_name]
    )

    final_model.fit(
        X_train_final,
        y_train_final,
    )

    predictions = final_model.predict(
        X_test
    )

    metrics = calculate_metrics(
        y_test,
        predictions,
    )

    print("Модель:", best_model_name)

    print(
        f"Accuracy: {metrics['accuracy']:.4f}"
    )
    print(
        f"Precision: {metrics['precision']:.4f}"
    )
    print(
        f"Recall: {metrics['recall']:.4f}"
    )
    print(
        f"F1-score: {metrics['f1_score']:.4f}"
    )
    print(
        "False Positive Rate: "
        f"{metrics['false_positive_rate']:.4f}"
    )

    print("\nConfusion Matrix:")
    print(
        f"TN={metrics['tn']}  "
        f"FP={metrics['fp']}  "
        f"FN={metrics['fn']}  "
        f"TP={metrics['tp']}"
    )

    # Сохраняем метрики
    test_results = pd.DataFrame(
        [
            {
                "model": best_model_name,
                **metrics,
            }
        ]
    )

    test_results_path = (
        RESULTS_DIR
        / "baseline_test_results.csv"
    )

    test_results.to_csv(
        test_results_path,
        index=False,
        encoding="utf-8",
    )

    # Сохраняем только нашу обученную модель
    model_path = (
        MODELS_DIR
        / "english_baseline_model.joblib"
    )

    joblib.dump(
        final_model,
        model_path,
    )

    print(
        "\nМодель models/"
        "english_baseline_model.joblib "
        "файлына сақталды."
    )

    return final_model, predictions, metrics


# ============================================================
# 9. CONFUSION MATRIX ГРАФИГІ
# ============================================================

def save_confusion_matrix(metrics):
    matrix = [
        [metrics["tn"], metrics["fp"]],
        [metrics["fn"], metrics["tp"]],
    ]

    figure, axis = plt.subplots(
        figsize=(6, 5)
    )

    image = axis.imshow(matrix)

    axis.set_title(
        "Baseline модельдің Confusion Matrix нәтижесі"
    )

    axis.set_xlabel(
        "Болжанған класс"
    )

    axis.set_ylabel(
        "Нақты класс"
    )

    axis.set_xticks(
        [0, 1],
        labels=[
            "No Prompt Injection",
            "Prompt Injection",
        ],
    )

    axis.set_yticks(
        [0, 1],
        labels=[
            "No Prompt Injection",
            "Prompt Injection",
        ],
    )

    for row in range(2):
        for column in range(2):
            axis.text(
                column,
                row,
                matrix[row][column],
                ha="center",
                va="center",
            )

    figure.colorbar(
        image,
        ax=axis,
    )

    figure.tight_layout()

    output_path = (
        RESULTS_DIR
        / "baseline_confusion_matrix.png"
    )

    figure.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    print(
        "Confusion Matrix графигі "
        "results бумасына сақталды."
    )


# ============================================================
# 10. ОСНОВНОЙ ЗАПУСК
# ============================================================

def main():
    try:
        train_df, validation_df, test_df = load_data()

        models = create_models()

        validation_results = compare_models(
            models,
            train_df,
            validation_df,
        )

        best_model_name = select_best_model(
            validation_results
        )

        final_model, predictions, test_metrics = (
            train_and_test_best_model(
                models,
                best_model_name,
                train_df,
                validation_df,
                test_df,
            )
        )

        save_confusion_matrix(
            test_metrics
        )

        print("\n" + "=" * 60)
        print("BASELINE ЭКСПЕРИМЕНТ СӘТТІ АЯҚТАЛДЫ")
        print("=" * 60)

    except Exception as error:
        print("\nҚате пайда болды:")
        print(error)
        raise


if __name__ == "__main__":
    main()