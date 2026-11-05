from pathlib import Path

import pandas as pd
from datasets import load_dataset


# ============================================================
# 1. ПУТИ ПРОЕКТА
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
RESULTS_DIR = BASE_DIR / "results"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. НАСТРОЙКИ ДАТАСЕТА
# ============================================================

DATASET_NAME = "neuralchemy/Prompt-injection-dataset"
DATASET_CONFIG = "core"


# Категории атак, которые входят в основной эксперимент
PRIMARY_ATTACK_CATEGORIES = {
    "direct_injection",
    "prompt_injection",
    "instruction_override",
    "system_manipulation",
    "persona_replacement",
    "prompt_extraction",
    "system_extraction",
    "encoding_obfuscation",
    "token_smuggling",
    "token_injection",
    "payload_injection",
    "context_confusion",
    "output_manipulation",
    "response_manipulation",
}


# ============================================================
# 3. ЗАГРУЗКА ДАТАСЕТА
# ============================================================

def load_english_dataset():
    print("Ағылшын тіліндегі Prompt Injection датасеті жүктелуде...")

    dataset = load_dataset(
        DATASET_NAME,
        DATASET_CONFIG
    )

    return dataset


# ============================================================
# 4. ОБЩАЯ ИНФОРМАЦИЯ
# ============================================================

def show_dataset_info(dataset):
    print("\nДатасет сәтті жүктелді.")

    for split_name in dataset.keys():
        split = dataset[split_name]

        print(f"\n--- {split_name.upper()} ---")
        print("Жазбалар саны:", len(split))
        print("Бағандар:", split.column_names)


# ============================================================
# 5. ПРОВЕРКА КАЧЕСТВА ДАННЫХ
# ============================================================

def analyze_dataset(dataset):
    print("\n" + "=" * 60)
    print("ДЕРЕКТЕР ЖИЫНЫН ТАЛДАУ")
    print("=" * 60)

    for split_name in dataset.keys():
        dataframe = dataset[split_name].to_pandas()

        print(f"\n--- {split_name.upper()} ---")

        print("\nКласстардың таралуы:")
        print(dataframe["label"].value_counts(dropna=False))

        print("\nБос мәндер саны:")
        print(dataframe.isnull().sum())

        duplicate_count = dataframe.duplicated(
            subset=["text"]
        ).sum()

        print("\nҚайталанатын мәтіндер саны:")
        print(duplicate_count)


# ============================================================
# 6. СОХРАНЕНИЕ RAW
# ============================================================

def save_raw_dataset(dataset):
    print("\n" + "=" * 60)
    print("БАСТАПҚЫ ДЕРЕКТЕРДІ САҚТАУ")
    print("=" * 60)

    for split_name in dataset.keys():
        dataframe = dataset[split_name].to_pandas()

        output_path = RAW_DATA_DIR / f"english_{split_name}.csv"

        # Raw-файлы повторно не перезаписываем
        if output_path.exists():
            print(
                f"{output_path.name} файлы бұрыннан бар. "
                f"Қайта жазылмады."
            )
            continue

        dataframe.to_csv(
            output_path,
            index=False,
            encoding="utf-8"
        )

        print(
            f"{output_path.name}: "
            f"{len(dataframe)} жазба сақталды."
        )


# ============================================================
# 7. БАЗОВАЯ ПОДГОТОВКА PROCESSED
# ============================================================

def prepare_processed_dataset(dataset):
    print("\n" + "=" * 60)
    print("ӨҢДЕЛГЕН ДЕРЕКТЕР ЖИЫНЫН ДАЙЫНДАУ")
    print("=" * 60)

    required_columns = {
        "text",
        "label",
        "category",
        "group_id"
    }

    for split_name in dataset.keys():
        dataframe = dataset[split_name].to_pandas().copy()

        missing_columns = (
            required_columns - set(dataframe.columns)
        )

        if missing_columns:
            raise ValueError(
                f"Қажетті бағандар табылмады: "
                f"{sorted(missing_columns)}"
            )

        # Проверяем метки
        actual_labels = set(dataframe["label"].unique())

        if not actual_labels.issubset({0, 1}):
            raise ValueError(
                f"Белгісіз label мәндері: {actual_labels}"
            )

        # Сам текст prompt не изменяем
        dataframe["language"] = "en"
        dataframe["split"] = split_name

        output_path = (
            PROCESSED_DATA_DIR
            / f"english_{split_name}_processed.csv"
        )

        dataframe.to_csv(
            output_path,
            index=False,
            encoding="utf-8"
        )

        print(
            f"{output_path.name}: "
            f"{len(dataframe)} жазба сақталды."
        )


# ============================================================
# 8. СОЗДАНИЕ ОСНОВНОЙ ИССЛЕДОВАТЕЛЬСКОЙ ВЫБОРКИ
# ============================================================

def create_primary_research_dataset(dataset):
    print("\n" + "=" * 60)
    print("НЕГІЗГІ ЗЕРТТЕУ ДЕРЕКТЕР ЖИЫНЫН ҚАЛЫПТАСТЫРУ")
    print("=" * 60)

    summary_rows = []

    for split_name in dataset.keys():
        dataframe = dataset[split_name].to_pandas().copy()

        # Все нормальные примеры оставляем
        benign_mask = dataframe["label"] == 0

        # Из атак оставляем только категории,
        # соответствующие нашей основной задаче
        attack_mask = (
            (dataframe["label"] == 1)
            & dataframe["category"].isin(
                PRIMARY_ATTACK_CATEGORIES
            )
        )

        filtered = dataframe[
            benign_mask | attack_mask
        ].copy()

        filtered["language"] = "en"
        filtered["split"] = split_name

        # Понятное название класса
        filtered["class_name"] = filtered["label"].map(
            {
                0: "no_prompt_injection",
                1: "prompt_injection"
            }
        )

        benign_count = int(
            (filtered["label"] == 0).sum()
        )

        attack_count = int(
            (filtered["label"] == 1).sum()
        )

        total_count = len(filtered)

        output_path = (
            PROCESSED_DATA_DIR
            / f"english_{split_name}_primary.csv"
        )

        filtered.to_csv(
            output_path,
            index=False,
            encoding="utf-8"
        )

        summary_rows.append(
            {
                "split": split_name,
                "total": total_count,
                "no_prompt_injection": benign_count,
                "prompt_injection": attack_count,
            }
        )

        print(f"\n--- {split_name.upper()} ---")
        print("Барлығы:", total_count)
        print("No Prompt Injection:", benign_count)
        print("Prompt Injection:", attack_count)

        print("\nҚолданылған шабуыл категориялары:")

        attack_categories = filtered[
            filtered["label"] == 1
        ]["category"].value_counts()

        print(attack_categories)


    # Сохраняем краткую таблицу для будущего диплома
    summary_df = pd.DataFrame(summary_rows)

    summary_path = (
        RESULTS_DIR
        / "english_primary_dataset_summary.csv"
    )

    summary_df.to_csv(
        summary_path,
        index=False,
        encoding="utf-8"
    )

    print("\nЖиынтық кесте:")
    print(summary_df.to_string(index=False))

    print(
        "\nЖиынтық нәтиже "
        "results/english_primary_dataset_summary.csv "
        "файлына сақталды."
    )


# ============================================================
# 9. ПОКАЗ ПОНЯТНЫХ ПРИМЕРОВ
# ============================================================

def show_primary_examples(dataset):
    print("\n" + "=" * 60)
    print("НЕГІЗГІ ЗЕРТТЕУ МЫСАЛДАРЫ")
    print("=" * 60)

    dataframe = dataset["train"].to_pandas()

    benign_examples = dataframe[
        dataframe["label"] == 0
    ].head(3)

    attack_examples = dataframe[
        (dataframe["label"] == 1)
        & (
            dataframe["category"]
            == "direct_injection"
        )
    ].head(3)

    print("\n--- NO PROMPT INJECTION ---")

    for number, (_, row) in enumerate(
        benign_examples.iterrows(),
        start=1
    ):
        print(f"\n{number}-мысал:")
        print(row["text"])
        print("Категория:", row["category"])

    print("\n--- DIRECT PROMPT INJECTION ---")

    for number, (_, row) in enumerate(
        attack_examples.iterrows(),
        start=1
    ):
        print(f"\n{number}-мысал:")
        print(row["text"])
        print("Категория:", row["category"])


# ============================================================
# 10. ОСНОВНОЙ ЗАПУСК
# ============================================================

def main():
    try:
        dataset = load_english_dataset()

        show_dataset_info(dataset)

        analyze_dataset(dataset)

        save_raw_dataset(dataset)

        prepare_processed_dataset(dataset)

        create_primary_research_dataset(dataset)

        show_primary_examples(dataset)

        print("\n" + "=" * 60)
        print("ЖҰМЫС СӘТТІ АЯҚТАЛДЫ")
        print("=" * 60)

    except Exception as error:
        print("\nҚате пайда болды:")
        print(error)

        # Ошибку не скрываем
        raise


if __name__ == "__main__":
    main()