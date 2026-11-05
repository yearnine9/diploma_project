from pathlib import Path

import pandas as pd


# ============================================================
# 1. ПУТИ
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

TRAIN_PATH = DATA_DIR / "english_train_primary.csv"
VALIDATION_PATH = DATA_DIR / "english_validation_primary.csv"
TEST_PATH = DATA_DIR / "english_test_primary.csv"


# ============================================================
# 2. ЗАГРУЗКА ДАННЫХ
# ============================================================

def load_datasets():
    print("Деректер жүктелуде...")

    paths = {
        "train": TRAIN_PATH,
        "validation": VALIDATION_PATH,
        "test": TEST_PATH,
    }

    dataframes = {}

    for split_name, path in paths.items():
        if not path.exists():
            raise FileNotFoundError(
                f"Файл табылмады: {path.name}"
            )

        dataframe = pd.read_csv(path)

        required_columns = {
            "text",
            "label",
            "group_id",
        }

        missing_columns = (
            required_columns - set(dataframe.columns)
        )

        if missing_columns:
            raise ValueError(
                f"{split_name}: қажетті бағандар жоқ: "
                f"{sorted(missing_columns)}"
            )

        dataframes[split_name] = dataframe

        print(
            f"{split_name}: {len(dataframe)} жазба"
        )

    return dataframes


# ============================================================
# 3. GROUP_ID БОЙЫНША ТЕКСЕРУ
# ============================================================

def check_group_id_overlap(dataframes):
    print("\n" + "=" * 60)
    print("GROUP_ID БОЙЫНША ҚАЙТАЛАНУДЫ ТЕКСЕРУ")
    print("=" * 60)

    train_groups = set(
        dataframes["train"]["group_id"].astype(str)
    )

    validation_groups = set(
        dataframes["validation"]["group_id"].astype(str)
    )

    test_groups = set(
        dataframes["test"]["group_id"].astype(str)
    )

    train_validation_overlap = (
        train_groups & validation_groups
    )

    train_test_overlap = (
        train_groups & test_groups
    )

    validation_test_overlap = (
        validation_groups & test_groups
    )

    print(
        "Train ↔ Validation overlap:",
        len(train_validation_overlap),
    )

    print(
        "Train ↔ Test overlap:",
        len(train_test_overlap),
    )

    print(
        "Validation ↔ Test overlap:",
        len(validation_test_overlap),
    )

    return (
        len(train_validation_overlap),
        len(train_test_overlap),
        len(validation_test_overlap),
    )


# ============================================================
# 4. МӘТІН БОЙЫНША ТЕКСЕРУ
# ============================================================

def normalize_text(series):
    return (
        series
        .astype(str)
        .str.strip()
        .str.casefold()
        .str.replace(
            r"\s+",
            " ",
            regex=True,
        )
    )


def check_text_overlap(dataframes):
    print("\n" + "=" * 60)
    print("МӘТІН БОЙЫНША ҚАЙТАЛАНУДЫ ТЕКСЕРУ")
    print("=" * 60)

    normalized = {}

    for split_name, dataframe in dataframes.items():
        normalized[split_name] = set(
            normalize_text(
                dataframe["text"]
            )
        )

    train_validation_overlap = (
        normalized["train"]
        & normalized["validation"]
    )

    train_test_overlap = (
        normalized["train"]
        & normalized["test"]
    )

    validation_test_overlap = (
        normalized["validation"]
        & normalized["test"]
    )

    print(
        "Train ↔ Validation мәтіндері:",
        len(train_validation_overlap),
    )

    print(
        "Train ↔ Test мәтіндері:",
        len(train_test_overlap),
    )

    print(
        "Validation ↔ Test мәтіндері:",
        len(validation_test_overlap),
    )

    return (
        len(train_validation_overlap),
        len(train_test_overlap),
        len(validation_test_overlap),
    )


# ============================================================
# 5. ҚОРЫТЫНДЫ
# ============================================================

def show_conclusion(group_overlaps, text_overlaps):
    print("\n" + "=" * 60)
    print("ТЕКСЕРУ ҚОРЫТЫНДЫСЫ")
    print("=" * 60)

    total_group_overlap = sum(group_overlaps)
    total_text_overlap = sum(text_overlaps)

    if total_group_overlap == 0 and total_text_overlap == 0:
        print(
            "Нәтиже: train, validation және test "
            "жиындары арасында қайталану анықталған жоқ."
        )
        print(
            "Экспериментті жалғастыруға болады."
        )

    else:
        print(
            "НАЗАР АУДАРЫҢЫЗ: жиындар арасында "
            "қайталану анықталды."
        )
        print(
            "Деректерді қайта бөлу қажет."
        )


# ============================================================
# 6. ОСНОВНОЙ ЗАПУСК
# ============================================================

def main():
    try:
        dataframes = load_datasets()

        group_overlaps = check_group_id_overlap(
            dataframes
        )

        text_overlaps = check_text_overlap(
            dataframes
        )

        show_conclusion(
            group_overlaps,
            text_overlaps,
        )

        print("\nТексеру сәтті аяқталды.")

    except Exception as error:
        print("\nҚате пайда болды:")
        print(error)
        raise


if __name__ == "__main__":
    main()