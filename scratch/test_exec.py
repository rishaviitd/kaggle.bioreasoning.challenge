code = '''import dspy
class SimpleClassificationSignature(dspy.Signature):
    pert = dspy.InputField(desc="The knocked-out perturbation gene")
    gene = dspy.InputField(desc="The target gene to predict")
    
    reasoning = dspy.OutputField(desc="Step-by-step biological reasoning")
    label = dspy.OutputField(desc="Final label: exactly 'up', 'down', or 'none'")
    
SimpleClassificationSignature.__doc__ = """hello"""
program = dspy.ChainOfThought(SimpleClassificationSignature)
'''
d = {}
exec(code, d)
print(d['SimpleClassificationSignature'].__doc__)
