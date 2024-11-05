from joblib import load



with open("./data/EL-CERAL/CERAL-L-v241103.joblib", "rb") as f:
    scaler = load(f)

print(scaler)