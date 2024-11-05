from pydantic import BaseModel


ER_cli_features = {
    'age': 'Age',
    'height': 'Height',
    'weight': 'Weight',
    'tumor_number': 'Tumor number',
    'tumor_size': 'Tumor size',
    'afp': 'AFP',
    'ast': 'AST',
    'alt': 'ALT',
    'alb': 'ALB',
    'alk_p': 'ALK-P',
    'bili': 'BILI',
    'cr': 'CR',
    'wbc': 'WBC',
    'plat': 'PLAT',
    'ptinr': 'PTINR',
    'na': 'Na',
    'close_to_4_score': 'close_to_4_score',
    'bclc': 'BCLC',
    'close_to_1': 'close_to_1',
    'close_to_2378': 'close_to_2378',
}

class PatientData_ER(BaseModel):
    age: float | None = None
    height: float | None = None
    weight: float | None = None
    tumor_number: float | None = None
    tumor_size: float | None = None
    afp: float | None = None
    ast: float | None = None
    alt: float | None = None
    alb: float | None = None
    alk_p: float | None = None
    bili: float | None = None
    cr: float | None = None
    wbc: float | None = None
    plat: float | None = None
    ptinr: float | None = None
    na: float | None = None
    close_to_4_score: float | None = None
    bclc: float | None = None
    close_to_1: float | None = None
    close_to_2378: float | None = None

    def dict(self, *args, **kwargs):
        original_dict = super().dict(*args, **kwargs)
        return {ER_cli_features[key]: original_dict[key] for key in original_dict if key in ER_cli_features.keys()}


Surv_cli_features = {
    'sex': 'Sex',
    'age': 'Age',
    'height': 'Height',
    'weight': 'Weight',
    'afp': 'AFP',
    'ast': 'AST',
    'alt': 'ALT',
    'alb': 'ALB',
    'alk_p': 'ALK-P',
    'bili': 'BILI',
    'child_class': 'Child_Class',
    'plat': 'PLAT',
    'hb': 'HB',
    'neutrophil': 'Neutrophil',
    'lymphocyte': 'Lymphocyte',
    'bun': 'BUN',
    'cr': 'CR',
    'bclc': 'BCLC',
    'close_to_4': 'close_to_4',
}

class PatientData_Surv(BaseModel):
    sex: float | None = None
    age: float | None = None
    height: float | None = None
    weight: float | None = None
    afp: float | None = None
    ast: float | None = None
    alt: float | None = None
    alb: float | None = None
    alk_p: float | None = None
    bili: float | None = None
    child_class: float | None = None
    plat: float | None = None
    hb: float | None = None
    neutrophil: float | None = None
    lymphocyte: float | None = None
    bun: float | None = None
    cr: float | None = None
    bclc: float | None = None
    close_to_4: float | None = None

    def dict(self, *args, **kwargs):
        original_dict = super().dict(*args, **kwargs)
        return {Surv_cli_features[key]: original_dict[key] for key in original_dict if key in Surv_cli_features.keys()}