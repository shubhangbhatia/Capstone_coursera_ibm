"""Analyze the supplied launch dataset and train a baseline reuse classifier."""
import argparse, json
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/spacex_launches_demo.csv")
    ap.add_argument("--output-dir", default="outputs")
    args = ap.parse_args()
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input)
    required = {"first_stage_reused","orbit","payload_type","launch_site","payload_mass_kg","landing_attempt","booster_reuse_count"}
    missing = required - set(df.columns)
    if missing: raise ValueError(f"Dataset missing required columns: {sorted(missing)}")
    df = df.dropna(subset=["first_stage_reused"])
    features = ["orbit","payload_type","launch_site","payload_mass_kg","landing_attempt","booster_reuse_count"]
    X, y = df[features], df["first_stage_reused"].astype(int)
    cat = ["orbit","payload_type","launch_site","landing_attempt"]
    num = ["payload_mass_kg","booster_reuse_count"]
    pre = ColumnTransformer([
        ("cat", Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore"))]), cat),
        ("num", Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler())]), num)
    ])
    pipe = Pipeline([("preprocess",pre),("classifier",RandomForestClassifier(n_estimators=250,max_depth=8,class_weight="balanced",random_state=42))])
    Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    pipe.fit(Xtr,ytr); pred = pipe.predict(Xte)
    result = {"rows":len(df),"test_rows":len(yte),"accuracy":accuracy_score(yte,pred),
              "precision":precision_score(yte,pred,zero_division=0),
              "recall":recall_score(yte,pred,zero_division=0),"f1":f1_score(yte,pred,zero_division=0),
              "confusion_matrix":confusion_matrix(yte,pred).tolist()}
    (out/"metrics.json").write_text(json.dumps(result,indent=2))
    joblib.dump(pipe,out/"reuse_classifier.joblib")
    df.describe(include="all").transpose().to_csv(out/"data_profile.csv")
    print(json.dumps(result,indent=2))
if __name__ == "__main__": main()
