import pandas as pd
import dspy
from pathlib import Path

from src.track_one.gepa_config import get_student_lm, get_refiner_lm
from src.track_one.gepa_metric import gepa_kaggle_metric


TRAIN_DATA = Path("data/gepa_splits/gepa_train.csv")
VAL_DATA = Path("data/gepa_splits/gepa_val.csv")
GEPA_LOG_DIR = "src/track_one/metrics/gepa_logs"
OPTIMIZED_STUDENT_PATH = "src/track_one/prompts/optimized_trackA_student.json"


class PredictInteraction(dspy.Signature):
    """You are a biological reasoning assistant. You must predict whether the biological perturbation regulates the target gene. Think step by step about known biological pathways. Your final prediction must be exactly one of: 'up', 'down', or 'none'."""

    pert = dspy.InputField(desc="The CRISPRi knockdown gene.")
    gene = dspy.InputField(desc="The target gene whose expression is predicted.")

    reasoning = dspy.OutputField(desc="Reasoning about the pathway and interaction.")
    prediction = dspy.OutputField(desc="The interaction label. Must be exactly 'up', 'down', or 'none'.")


class TrackAStudent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.ChainOfThought(PredictInteraction)

    def forward(self, pert: str, gene: str):
        return self.predict(pert=pert, gene=gene)


def load_data(filepath: Path):
    df = pd.read_csv(filepath)
    examples = []
    for _, row in df.iterrows():
        ex = dspy.Example(
            pert=str(row['pert']),
            gene=str(row['gene']),
            label=str(row['label'])
        ).with_inputs("pert", "gene")
        examples.append(ex)
    return examples


def main():
    print("Setting up models...")
    student_lm = get_student_lm()
    refiner_lm = get_refiner_lm()

    dspy.settings.configure(lm=student_lm)

    print("Loading datasets...")
    trainset = load_data(TRAIN_DATA)
    valset = load_data(VAL_DATA)

    print(f"Loaded {len(trainset)} training examples and {len(valset)} validation examples.")

    print("Initializing GEPA Optimizer...")
    gepa = dspy.GEPA(
        metric=gepa_kaggle_metric,
        reflection_lm=refiner_lm,
        max_full_evals=3,
        track_stats=True,
        log_dir=GEPA_LOG_DIR,
    )

    student_module = TrackAStudent()

    print("Starting optimization... (This will take a while, making calls to NVIDIA API)")
    optimized_student = gepa.compile(
        student_module,
        trainset=trainset,
        valset=valset
    )

    print("\nOptimization Complete!")
    Path(OPTIMIZED_STUDENT_PATH).parent.mkdir(parents=True, exist_ok=True)
    optimized_student.save(OPTIMIZED_STUDENT_PATH)
    print(f"Saved optimized module to {OPTIMIZED_STUDENT_PATH}")

if __name__ == "__main__":
    main()
