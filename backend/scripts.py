import numpy as np
import pandas as pd
import warnings
from pydantic import BaseModel, Field
import logging
import joblib
from typing import Type


logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore', category=FutureWarning)


def parse_feature(estimator):
    selected_features = estimator.feature_names_in_
    features = dict()
    for feature in selected_features:
        if feature.startswith('class_') or feature.startswith('ln_') or feature.startswith('log_'):
            details = feature.split("_")
            trans = details[0]
            name = details[1]
        else:
            name = feature
            trans = ""
        
        if name not in features.keys():
            features[name] = [trans]
        else:
            features[name].append(trans)

    return features


def get_derived_features(df, feature_details, cutpoints):
    feature_df = pd.DataFrame()
    for name, transes in feature_details.items():
        for trans in transes:
            if trans == "":
                if name == "ALBIscore":
                    feature_df[name] = (np.log10(df['BILI'] * 17.1) * 0.66) - ((df['ALB'] * 10) * 0.085)
                elif name == "APRI":
                    feature_df[name] = (df['AST'] / 45) / (df['PLAT'] / 100000)
                elif name == "BMI":
                    feature_df[name] = df['Weight'] / ((df['Height'] / 100)**2)
                else:
                    feature_df[name] = df[name]
            elif trans == "class":
                if name == "Size":
                    feature_df[f"{trans}_{name}"] = pd.cut(df['Tumor size'], bins=cutpoints['Tumor size'], labels=list(range( len(cutpoints['Tumor size'])-1 )))
                elif name == "INR":
                    feature_df[f"{trans}_{name}"] = pd.cut(df['PTINR'], bins=cutpoints['PTINR'], labels=list(range( len(cutpoints['PTINR'])-1 )))
                elif name == "TB":
                    feature_df[f"{trans}_{name}"] = pd.cut(df['BILI'], bins=cutpoints['BILI'], labels=list(range( len(cutpoints['BILI'])-1 )))
                elif name == "NLR":
                    df[name] = df['Neutrophil'] / df['Lymphocyte']
                    feature_df[f"{trans}_{name}"] = pd.cut(df[name], bins=cutpoints[name], labels=list(range( len(cutpoints[name])-1 )))
                else:
                    feature_df[f"{trans}_{name}"] = pd.cut(df[name], bins=cutpoints[name], labels=list(range( len(cutpoints[name])-1 )))
            elif trans == "ln":
                if name == "BMI":
                    df[name] = df['Weight'] / ((df['Height'] / 100)**2)
                elif name == "FIB4":
                    df[name] = (df['Age'] * df['AST']) / ((df['ALT']**0.5) * (df['PLAT'] / 1000))
                feature_df[f"{trans}_{name}"] = df[name].apply(np.log)
            elif trans == "log":
                feature_df[f"{trans}_{name}"] = df[name].apply(np.log10)

    return feature_df


def standardize_df(df, scaler_pth):
    col_names = df.columns
    scaler = joblib.load(scaler_pth)
    std_data = scaler.transform(df)
    std_feature_df = pd.DataFrame(std_data, columns=col_names)
    
    return std_feature_df


def predict_ER(estimator, feature_df, RISK_THRESHOLD, mode="case"):
    preds = pd.Series(estimator.predict(feature_df), name='risk_score').round(2)
    risk_groups = preds.apply(lambda risk_score: "High" if risk_score >= RISK_THRESHOLD else "Low" )
    risk_groups.name = 'risk_group'

    survf = estimator.predict_survival_function(feature_df)
    month6_probs = pd.Series(np.asarray([ fn(6) for fn in survf])).round(2)
    month12_probs = pd.Series(np.asarray([ fn(12) for fn in survf])).round(2)
    month18_probs = pd.Series(np.asarray([ fn(18) for fn in survf])).round(2)
    month24_probs = pd.Series(np.asarray([ fn(24) for fn in survf])).round(2)

    results = pd.concat([preds, risk_groups], axis=1).to_dict(orient='records')

    survival_result = pd.concat([month6_probs, month12_probs, month18_probs, month24_probs], axis=1).to_dict(orient='split')['data']

    if mode == "case":
        for idx, result in enumerate(results):
            result['non_recurrence_rates'] = survival_result[idx]  # array
            results[idx] = result
    elif mode == "batch":
        for idx, result in enumerate(results):
            result['6 month recurrence-free survival rate'] = survival_result[idx][0]
            result['12 month recurrence-free survival rate'] = survival_result[idx][1]
            result['18 month recurrence-free survival rate'] = survival_result[idx][2]
            result['24 month recurrence-free survival rate'] = survival_result[idx][3]
            results[idx] = result

    return results


def predict_surv(estimator, feature_df, RISK_THRESHOLD, mode="case"):
    preds = pd.Series(estimator.predict(feature_df), name='risk_score').round(2)
    risk_groups = preds.apply(lambda risk_score: "High" if risk_score >= RISK_THRESHOLD else "Low" )
    risk_groups.name = 'risk_group'

    survf = estimator.predict_survival_function(feature_df)
    year1_probs = pd.Series(np.asarray([ fn(12) for fn in survf])).round(2)
    year2_probs = pd.Series(np.asarray([ fn(24) for fn in survf])).round(2)
    year3_probs = pd.Series(np.asarray([ fn(36) for fn in survf])).round(2)
    year4_probs = pd.Series(np.asarray([ fn(48) for fn in survf])).round(2)
    year5_probs = pd.Series(np.asarray([ fn(60) for fn in survf])).round(2)

    results = pd.concat([preds, risk_groups], axis=1).to_dict(orient='records')

    survival_result = pd.concat([year1_probs, year2_probs, year3_probs, year4_probs, year5_probs], axis=1).to_dict(orient='split')['data']

    if mode == "case":
        for idx, result in enumerate(results):
            result['survival_rates'] = survival_result[idx]  # array
            results[idx] = result
    elif mode == "batch":
        for idx, result in enumerate(results):
            result['1 year survival rate'] = survival_result[idx][0]
            result['2 year survival rate'] = survival_result[idx][1]
            result['3 year survival rate'] = survival_result[idx][2]
            result['4 year survival rate'] = survival_result[idx][3]
            result['5 year survival rate'] = survival_result[idx][4]
            results[idx] = result

    return results



if __name__ == "__main__":
    print("test")