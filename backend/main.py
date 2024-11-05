import pandas as pd
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import ValidationError
from io import BytesIO
import joblib
import logging
import json
from setting import *
from scripts import parse_feature, get_derived_features, standardize_df, predict_ER, predict_surv
from models import PatientData_ER, PatientData_Surv

# Initial
## setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
# get root logger
logger = logging.getLogger(__name__)
logger.info("Logging...")

logger.info("Import EL-RFA models...")
EL_CERAL_S_model = joblib.load(EL_CERAL_S)
EL_CERAL_L_model = joblib.load(EL_CERAL_L)
EL_MERAL_S_model = joblib.load(EL_MERAL_S)
EL_MERAL_L_model = joblib.load(EL_MERAL_L)
EL_COSAL_model = joblib.load(EL_COSAL)
EL_MOSAL_model = joblib.load(EL_MOSAL)

logger.info("Get EL-RFA features...")
EL_CERAL_S_features = parse_feature(EL_CERAL_S_model)
EL_CERAL_L_features = parse_feature(EL_CERAL_L_model)
EL_MERAL_S_features = parse_feature(EL_MERAL_S_model)
EL_MERAL_L_features = parse_feature(EL_MERAL_L_model)
EL_COSAL_features = parse_feature(EL_COSAL_model)
EL_MOSAL_features = parse_feature(EL_MOSAL_model)

logger.info("Initialize API...")
app = FastAPI()

# CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Initialization complete.")


# Views
@app.get("/api/test")
def test():
    return EL_CERAL_L_features

@app.post("/api/early_recurrence/submit/case")
async def submit(request: Request):
    form_data = await request.form()
    data_dict = {key: value for key, value in form_data.items() if not isinstance(value, UploadFile)}
    file: UploadFile = form_data.get("file")

    try:
        patient_data = PatientData_ER(**data_dict)
    except ValidationError as e:
        return HTTPException(status_code=400, detail=f"Validation error: {e.errors()}")
    clinical_data_df = pd.DataFrame([patient_data.dict()])
    
    if file:
        file_contents = await file.read()
        try:
            if file.filename.endswith('.csv'):
                image_features_df = pd.read_csv( BytesIO( file_contents ) ).astype('float')
            elif file.filename.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
                image_features_df = pd.read_excel( BytesIO( file_contents ) ).astype('float')
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format")
            
            complete_data_df = pd.concat([clinical_data_df, image_features_df], axis=1)
            
            if complete_data_df.loc[0, 'Tumor size'] > 2.0:
                try:
                    feature_df = get_derived_features(complete_data_df, EL_MERAL_L_features, CUTPOINTS)
                    std_feature_df = standardize_df(feature_df[EL_MERAL_L_model.feature_names_in_], EL_MERAL_L_SCALER)
                    results = predict_ER(EL_MERAL_L_model, std_feature_df, RISK_THRESHOLD_MERAL_L)
                except:
                    raise HTTPException(status_code=400, detail="Failed to use your image features.")
            else:
                try:
                    feature_df = get_derived_features(complete_data_df, EL_MERAL_S_features, CUTPOINTS)
                    std_feature_df = standardize_df(feature_df[EL_MERAL_S_model.feature_names_in_], EL_MERAL_S_SCALER)
                    results = predict_ER(EL_MERAL_S_model, std_feature_df, RISK_THRESHOLD_MERAL_S)
                except:
                    raise HTTPException(status_code=400, detail="Failed to use your image features.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
    else:
        if clinical_data_df.loc[0, 'Tumor size'] > 2.0:
            feature_df = get_derived_features(clinical_data_df, EL_CERAL_L_features, CUTPOINTS)
            std_feature_df = standardize_df(feature_df[EL_CERAL_L_model.feature_names_in_], EL_CERAL_L_SCALER)
            results = predict_ER(EL_CERAL_L_model, std_feature_df, RISK_THRESHOLD_CERAL_L)
        else:
            feature_df = get_derived_features(clinical_data_df, EL_CERAL_S_features, CUTPOINTS)
            std_feature_df = standardize_df(feature_df[EL_CERAL_S_model.feature_names_in_], EL_CERAL_S_SCALER)
            results = predict_ER(EL_CERAL_S_model, std_feature_df, RISK_THRESHOLD_CERAL_S)
    
    return results

@app.post("/api/overall_survival/submit/case")
async def submit(request: Request):
    form_data = await request.form()
    data_dict = {key: value for key, value in form_data.items() if not isinstance(value, UploadFile)}
    file: UploadFile = form_data.get("file")

    try:
        patient_data = PatientData_Surv(**data_dict)
    except ValidationError as e:
        return HTTPException(status_code=400, detail=f"Validation error: {e.errors()}")
    clinical_data_df = pd.DataFrame([patient_data.dict()])
    
    if file:
        file_contents = await file.read()
        try:
            if file.filename.endswith('.csv'):
                image_features_df = pd.read_csv( BytesIO( file_contents ) ).astype('float')
            elif file.filename.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
                image_features_df = pd.read_excel( BytesIO( file_contents ) ).astype('float')
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format")
            
            complete_data_df = pd.concat([clinical_data_df, image_features_df], axis=1)
            
            try:
                feature_df = get_derived_features(complete_data_df, EL_MOSAL_features, CUTPOINTS)
                std_feature_df = standardize_df(feature_df[EL_MOSAL_model.feature_names_in_], EL_MOSAL_SCALER)
                results = predict_surv(EL_MOSAL_model, std_feature_df, RISK_THRESHOLD_MOSAL)
            except:
                raise HTTPException(status_code=400, detail="Failed to use your image features.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
    else:
        feature_df = get_derived_features(clinical_data_df, EL_COSAL_features, CUTPOINTS)
        std_feature_df = standardize_df(feature_df[EL_COSAL_model.feature_names_in_], EL_COSAL_SCALER)
        results = predict_surv(EL_COSAL_model, std_feature_df, RISK_THRESHOLD_COSAL)
    
    return results

@app.post("/api/early_recurrence/submit/batch")
async def submit_batch(file: UploadFile):
    file_contents = await file.read()
    try:
        if file.filename.endswith('.csv'):
            data_df = pd.read_csv( BytesIO( file_contents ) ).astype('float')
        elif file.filename.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
            data_df = pd.read_excel( BytesIO( file_contents ) ).astype('float')
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        if 'Tumor size' not in data_df.columns or data_df['Tumor size'].isnull().all():
            raise HTTPException(status_code=400, detail="Failed to use your features.")
        
        data_df_L = data_df[data_df['Tumor size'] > 2.0]
        data_df_S = data_df[data_df['Tumor size'] <= 2.0]
        
        if sum(data_df['Tumor size'] > 2.0) > 0:
            try:
                feature_df_L = get_derived_features(data_df_L, EL_MERAL_L_features, CUTPOINTS)
                std_feature_df_L = standardize_df(feature_df_L[EL_MERAL_L_model.feature_names_in_], EL_MERAL_L_SCALER)
                results_L = predict_ER(EL_MERAL_L_model, std_feature_df_L, RISK_THRESHOLD_MERAL_L, mode="batch")
                results_L_df = pd.DataFrame(results_L, index=data_df_L.index)
            except:
                try:
                    feature_df_L = get_derived_features(data_df_L, EL_CERAL_L_features, CUTPOINTS)
                    std_feature_df_L = standardize_df(feature_df_L[EL_CERAL_L_model.feature_names_in_], EL_CERAL_L_SCALER)
                    results_L = predict_ER(EL_CERAL_L_model, std_feature_df_L, RISK_THRESHOLD_CERAL_L, mode="batch")
                    results_L_df = pd.DataFrame(results_L, index=data_df_L.index)
                except:
                    raise HTTPException(status_code=400, detail="Failed to use your features.")

        if sum(data_df['Tumor size'] <= 2.0) > 0:
            try:
                feature_df_S = get_derived_features(data_df_S, EL_MERAL_S_features, CUTPOINTS)
                std_feature_df_S = standardize_df(feature_df_S[EL_MERAL_S_model.feature_names_in_], EL_MERAL_S_SCALER)
                results_S = predict_ER(EL_MERAL_S_model, std_feature_df_S, RISK_THRESHOLD_MERAL_S, mode="batch")
                results_S_df = pd.DataFrame(results_S, index=data_df_S.index)
            except:
                try:
                    feature_df_S = get_derived_features(data_df_S, EL_CERAL_S_features, CUTPOINTS)
                    std_feature_df_S = standardize_df(feature_df_S[EL_CERAL_S_model.feature_names_in_], EL_CERAL_S_SCALER)
                    results_S = predict_ER(EL_CERAL_S_model, std_feature_df_S, RISK_THRESHOLD_CERAL_S, mode="batch")
                    results_S_df = pd.DataFrame(results_S, index=data_df_S.index)
                except:
                    raise HTTPException(status_code=400, detail="Failed to use your features.")
        
        results_df = pd.concat([results_L_df, results_S_df]).sort_index()
        excel_file = BytesIO()
        results_df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        response = StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response.headers["Content-Disposition"] = "attachment; filename=results.xlsx"

        return response
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/api/overall_survival/submit/batch")
async def submit_batch(file: UploadFile):
    file_contents = await file.read()
    try:
        if file.filename.endswith('.csv'):
            data_df = pd.read_csv( BytesIO( file_contents ) ).astype('float')
        elif file.filename.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
            data_df = pd.read_excel( BytesIO( file_contents ) ).astype('float')
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        try:
            feature_df = get_derived_features(data_df, EL_MOSAL_features, CUTPOINTS)
            std_feature_df = standardize_df(feature_df[EL_MOSAL_model.feature_names_in_], EL_MOSAL_SCALER)
            results = predict_surv(EL_MOSAL_model, std_feature_df, RISK_THRESHOLD_MOSAL, mode="batch")
        except:
            try:
                feature_df = get_derived_features(data_df, EL_COSAL_features, CUTPOINTS)
                std_feature_df = standardize_df(feature_df[EL_COSAL_model.feature_names_in_], EL_COSAL_SCALER)
                results = predict_surv(EL_COSAL_model, std_feature_df, RISK_THRESHOLD_COSAL, mode="batch")
            except:
                raise HTTPException(status_code=400, detail="Failed to use your features.")
        
        results_df = pd.DataFrame(results)
        excel_file = BytesIO()
        results_df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        response = StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response.headers["Content-Disposition"] = "attachment; filename=results.xlsx"

        return response
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))