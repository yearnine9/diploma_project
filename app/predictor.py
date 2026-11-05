from pathlib import Path

import joblib
import pandas as pd


class MultilingualPromptInjectionDetector:

    def __init__(self):

        project_root = (
            Path(__file__)
            .resolve()
            .parent
            .parent
        )

        self.model_path = (
            project_root
            / "models"
            / "multilingual_final_model.joblib"
        )

        if not self.model_path.exists():
            raise FileNotFoundError(
                "multilingual_final_model.joblib not found."
            )

        package = joblib.load(
            self.model_path
        )

        if "model" not in package:
            raise ValueError(
                "Model package does not contain 'model'."
            )

        self.package = package
        self.model = package["model"]

        self.model_name = package.get(
            "model_name",
            "multilingual_prompt_injection_detector",
        )

        if "features" not in self.model.named_steps:
            raise ValueError(
                "Pipeline does not contain 'features'."
            )

        if "classifier" not in self.model.named_steps:
            raise ValueError(
                "Pipeline does not contain 'classifier'."
            )

        self.features = self.model.named_steps[
            "features"
        ]

        self.classifier = self.model.named_steps[
            "classifier"
        ]

        if not hasattr(
            self.classifier,
            "coef_",
        ):
            raise ValueError(
                "Classifier does not expose linear coefficients."
            )

        self.feature_names = (
            self.features
            .get_feature_names_out()
        )

        self.coefficients = (
            self.classifier
            .coef_[0]
        )

    @staticmethod
    def clean_feature_name(
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
                    len("word__"):
                ],
            )

        if feature_name.startswith(
            "char__"
        ):
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
        self,
        text,
        top_n=8,
    ):

        transformed = (
            self.features
            .transform(
                [
                    str(text)
                ]
            )
        )

        prediction = int(
            self.classifier
            .predict(
                transformed
            )[0]
        )

        decision_score = float(
            self.classifier
            .decision_function(
                transformed
            )[0]
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
            * self.coefficients[
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

            (
                feature_type,
                feature,
            ) = self.clean_feature_name(
                self.feature_names[
                    feature_index
                ]
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
                        float(
                            self.coefficients[
                                feature_index
                            ]
                        ),

                    "contribution":
                        float(
                            contribution
                        ),
                }
            )

        dataframe = pd.DataFrame(
            rows
        )

        if dataframe.empty:

            empty = pd.DataFrame(
                columns=[
                    "feature",
                    "feature_type",
                    "tfidf_value",
                    "weight",
                    "contribution",
                ]
            )

            return {
                "prediction":
                    prediction,

                "decision_score":
                    decision_score,

                "positive":
                    empty.copy(),

                "negative":
                    empty.copy(),
            }

        word_features = dataframe[
            dataframe[
                "feature_type"
            ] == "word"
        ].copy()

        if word_features.empty:
            explainable = dataframe.copy()
        else:
            explainable = word_features

        positive = (
            explainable[
                explainable[
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

        negative = (
            explainable[
                explainable[
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

    def predict(
        self,
        text,
    ):

        text = str(
            text
        ).strip()

        if not text:
            raise ValueError(
                "Input text is empty."
            )

        explanation = (
            self.explain_text(
                text,
                top_n=8,
            )
        )

        prediction = int(
            explanation[
                "prediction"
            ]
        )

        if prediction == 1:
            label = "Prompt Injection"
        else:
            label = "No Prompt Injection"

        return {
            "label":
                label,

            "prediction":
                prediction,

            "decision_score":
                float(
                    explanation[
                        "decision_score"
                    ]
                ),

            "positive_features":
                explanation[
                    "positive"
                ],

            "negative_features":
                explanation[
                    "negative"
                ],

            "model_name":
                self.model_name,
        }