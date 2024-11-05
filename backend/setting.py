import sys, os
from dotenv import load_dotenv
load_dotenv()

# 讀取模型儲存路徑
EL_CERAL_S = os.getenv("EL_CERAL_S")
EL_CERAL_L = os.getenv("EL_CERAL_L")
EL_MERAL_S = os.getenv("EL_MERAL_S")
EL_MERAL_L = os.getenv("EL_MERAL_L")

EL_COSAL = os.getenv("EL_COSAL")
EL_MOSAL = os.getenv("EL_MOSAL")

if not EL_CERAL_S: raise ValueError("Cannot find the path of EL_CERAL_S model.")
elif not EL_CERAL_L: raise ValueError("Cannot find the path of EL_CERAL_L model.")
elif not EL_MERAL_S: raise ValueError("Cannot find the path of EL_MERAL_S model.")
elif not EL_MERAL_L: raise ValueError("Cannot find the path of EL_MERAL_L model.")
elif not EL_COSAL: raise ValueError("Cannot find the path of EL_COSAL model.")
elif not EL_MOSAL: raise ValueError("Cannot find the path of EL_MOSAL model.")

# 讀取正規化檔儲存路徑
EL_CERAL_S_SCALER = os.getenv("EL_CERAL_S_SCALER")
EL_CERAL_L_SCALER = os.getenv("EL_CERAL_L_SCALER")
EL_MERAL_S_SCALER = os.getenv("EL_MERAL_S_SCALER")
EL_MERAL_L_SCALER = os.getenv("EL_MERAL_L_SCALER")

EL_COSAL_SCALER = os.getenv("EL_COSAL_SCALER")
EL_MOSAL_SCALER = os.getenv("EL_MOSAL_SCALER")

if not EL_CERAL_S_SCALER: raise ValueError("Cannot find the path of EL_CERAL_S scaler.")
elif not EL_CERAL_L_SCALER: raise ValueError("Cannot find the path of EL_CERAL_L scaler.")
elif not EL_MERAL_S_SCALER: raise ValueError("Cannot find the path of EL_MERAL_S scaler.")
elif not EL_MERAL_L_SCALER: raise ValueError("Cannot find the path of EL_MERAL_L scaler.")
elif not EL_COSAL_SCALER: raise ValueError("Cannot find the path of EL_COSAL scaler.")
elif not EL_MOSAL_SCALER: raise ValueError("Cannot find the path of EL_MOSAL scaler.")


CUTPOINTS = {
    'PTINR': [0, 1.1, float('inf')],  # class_INR
    'BILI': [0, 1.2, 2, float('inf')],  # class_TB
    'Tumor size': [0, 2, 3, 4, 5, 10, float('inf')],
    'CR': [0, 1.2, float('inf')],
    'AST': [0, 40, 80, float('inf')],
    'NLR': [0, 2.5, 3, 4, 5, float('inf')]
}


RISK_THRESHOLD_CERAL_S = 0.13982914572864316
RISK_THRESHOLD_CERAL_L = -0.2264321608040201
RISK_THRESHOLD_MERAL_S = 0.36842105263157876
RISK_THRESHOLD_MERAL_L = -0.216026711185309

RISK_THRESHOLD_COSAL = 0.4415160260606086
RISK_THRESHOLD_MOSAL = 0.26638203215999434


if __name__ == "__main__":
    print("EL-RFA-MODELs")