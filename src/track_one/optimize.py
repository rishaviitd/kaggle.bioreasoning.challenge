import pandas as pd
import dspy
from pathlib import Path

from src.track_one.evaluate.gepa_config import get_student_lm, get_refiner_lm
from src.track_one.evaluate.gepa_metric import gepa_kaggle_metric

# 1. Define the DSPy Signature and Module
class PredictInteraction(dspy.Signature):
    """You are a biological reasoning assistant. You must predict whether the biological perturbation regulates the target gene. Think step by step about known biological pathways. Your final prediction must be exactly one of: 'up', 'down', or 'none'."""
    
    pert = dspy.InputField(desc="The biological perturbation (e.g., a drug or compound).")
    gene = dspy.InputField(desc="The target gene.")
    
    reasoning = dspy.OutputField(desc="Reasoning about the pathway and interaction.")
    prediction = dspy.OutputField(desc="The interaction label. Must be exactly 'up', 'down', or 'none'.")

class TrackAStudent(dspy.Module):
    def __init__(self):
        super().__init__()
        # Using ChainOfThought to allow the model to output 'reasoning' before 'prediction'
        self.predict = dspy.ChainOfThought(PredictInteraction)
        
    def forward(self, pert: str, gene: str):
        return self.predict(pert=pert, gene=gene)

def load_data(filepath: Path):
    df = pd.read_csv(filepath)
    examples = []
    for _, row in df.iterrows():
        # Input fields must not be included in with_inputs unless we do it correctly. 
        # dspy.Example automatically treats kwargs as fields.
        ex = dspy.Example(
            pert=str(row['pert']),
            gene=str(row['gene']),
            label=str(row['label'])
        ).with_inputs("pert", "gene")
        examples.append(ex)
    return examples

def main():
    # 2. Configure DSPy Models via NVIDIA endpoints
    print("Setting up models...")
    student_lm = get_student_lm()
    refiner_lm = get_refiner_lm()
    
    dspy.settings.configure(lm=student_lm)
    
    # 3. Load Datasets
    print("Loading datasets...")
    trainset = load_data(Path("data/splits/gepa_train.csv"))
    valset = load_data(Path("data/splits/gepa_val.csv"))
    
    print(f"Loaded {len(trainset)} training examples and {len(valset)} validation examples.")
    
    # 4. Initialize GEPA
    # We use a relatively small number of full evals for testing purposes, but you can increase it.
    print("Initializing GEPA Optimizer...")
    gepa = dspy.GEPA(
        metric=gepa_kaggle_metric,
        reflection_lm=refiner_lm,
        auto="medium",          # Optimization budget
        max_full_evals=3,       # How many full candidate evaluations to perform. Set higher for full runs.
        track_stats=True,
        log_dir="data/splits/gepa_logs" # Save checkpoints here
    )
    
    student_module = TrackAStudent()
    
    # 5. Compile!
    print("Starting optimization... (This will take a while, making calls to NVIDIA API)")
    optimized_student = gepa.compile(
        student_module,
        trainset=trainset,
        valset=valset
    )
    
    # 6. Save the optimized prompt
    print("\nOptimization Complete!")
    optimized_student.save("data/splits/optimized_trackA_student.json")
    print("Saved optimized module to data/splits/optimized_trackA_student.json")

if __name__ == "__main__":
    main()
