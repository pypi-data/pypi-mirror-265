import os
import sys
import pickle
import warnings
import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import shap
import numpy as np
import pandas as pd
from loguru import logger
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from mordred import Calculator, descriptors
from molvs import standardize_smiles

from dilipred.constants import (
    ASSAY_TYPE,
    DESCS,
    LIV_DATA,
    SOURCE,
    BANNER,
    ABSTRACT,
    CITE,
)


now = datetime.now()
formatted_date = now.strftime("%d-%m-%Y")
formatted_time = now.strftime("%H-%M-%S")

INFO = pd.DataFrame({"name": LIV_DATA, "source": SOURCE, "assaytype": ASSAY_TYPE})


def standardized_smiles(value):
    try:
        return standardize_smiles(value)
    except:
        return "Cannot_do"


def MorganFingerprint(s):
    x = Chem.MolFromSmiles(s)
    return AllChem.GetMorganFingerprintAsBitVect(x, 2, 2048)


def MACCSKeysFingerprint(s):
    x = Chem.MolFromSmiles(s)
    return AllChem.GetMACCSKeysFingerprint(x)


def get_num_charged_atoms_neg(mol):
    mol_h = Chem.AddHs(mol)
    Chem.rdPartialCharges.ComputeGasteigerCharges(mol_h)

    positive = 0
    negative = 0

    for atom in mol_h.GetAtoms():
        if float(atom.GetProp("_GasteigerCharge")) <= 0:
            negative += 1

    return negative


def get_num_charged_atoms_pos(mol):
    mol_h = Chem.AddHs(mol)
    Chem.rdPartialCharges.ComputeGasteigerCharges(mol_h)

    positive = 0
    negative = 0

    for atom in mol_h.GetAtoms():
        if float(atom.GetProp("_GasteigerCharge")) >= 0:
            positive += 1
    return positive


def get_assembled_ring(mol):
    ring_info = mol.GetRingInfo()
    num_ring = ring_info.NumRings()
    ring_atoms = ring_info.AtomRings()
    num_assembled = 0

    for i in range(num_ring):
        for j in range(i + 1, num_ring):
            x = set(ring_atoms[i])
            y = set(ring_atoms[j])
            if not x.intersection(y):  # 2つの環が縮環でない場合に
                for x_id in x:
                    x_atom = mol.GetAtomWithIdx(x_id)
                    neighbors = [k.GetIdx() for k in x_atom.GetNeighbors()]
                    for x_n in neighbors:
                        if x_n in y:  # 環同士を繋ぐ結合があるか否か
                            num_assembled += 1

    return num_assembled


def get_num_stereocenters(mol):
    return AllChem.CalcNumAtomStereoCenters(
        mol
    ) + AllChem.CalcNumUnspecifiedAtomStereoCenters(mol)


def calc_descriptors(dataframe):
    mols = dataframe.smiles_r.apply(Chem.MolFromSmiles)
    descr = []
    for m in mols:
        descr.append(
            [
                Descriptors.TPSA(m),
                Descriptors.NumRotatableBonds(m),
                AllChem.CalcNumRings(m),
                Descriptors.NumAromaticRings(m),
                Descriptors.NumHAcceptors(m),
                Descriptors.NumHDonors(m),
                Descriptors.FractionCSP3(m),
                Descriptors.MolLogP(m),
                Descriptors.NHOHCount(m),
                Descriptors.NOCount(m),
                Descriptors.NumHeteroatoms(m),
                get_num_charged_atoms_pos(m),
                get_num_charged_atoms_neg(m),
                get_assembled_ring(m),
                get_num_stereocenters(m),
            ]
        )
    descr = np.asarray(descr)
    return descr


def calc_all_fp_desc(data):
    calc = Calculator(descriptors, ignore_3D=True)
    Ser_Mol = data["smiles_r"].apply(Chem.MolFromSmiles)
    Mordred_table = calc.pandas(Ser_Mol)
    Mordred_table = Mordred_table.astype("float")

    MACCSfingerprint_array = np.stack(data["smiles_r"].apply(MACCSKeysFingerprint))
    MACCS_collection = []
    for x in np.arange(MACCSfingerprint_array.shape[1]):
        x = "MACCS" + str(x)
        MACCS_collection.append(x)
    MACCSfingerprint_table = pd.DataFrame(
        MACCSfingerprint_array, columns=MACCS_collection
    )

    MorganFingerprint_array = np.stack(data["smiles_r"].apply(MorganFingerprint))
    Morgan_fingerprint_collection = []
    for x in np.arange(MorganFingerprint_array.shape[1]):
        x = "Mfp" + str(x)
        Morgan_fingerprint_collection.append(x)
    Morgan_fingerprint_table = pd.DataFrame(
        MorganFingerprint_array, columns=Morgan_fingerprint_collection
    )

    a = calc_descriptors(data)
    descdf = pd.DataFrame(a, columns=DESCS)
    descdf_approved = descdf.reset_index(drop=True)
    descdf_approved

    tox_model_data = pd.concat(
        [
            data,
            Morgan_fingerprint_table,
            MACCSfingerprint_table,
            descdf_approved,
            Mordred_table,
        ],
        axis=1,
    )
    tox_model_data

    return tox_model_data


def predict_individual_liv_data(data_dummy, features, endpoint):  # predict animal data
    with open(
        os.path.dirname(os.path.abspath(__file__))
        + f"/models/bestlivmodel_{endpoint}_model.sav",
        "rb",
    ) as f:
        loaded_rf = pickle.load(f)

    X = data_dummy[features]
    X = X.values
    y_proba = loaded_rf.predict_proba(X)[:, 1]

    return y_proba


def predict_individual_cmax_data(data_dummy, features, endpoint):  # predict animal data
    with open(
        os.path.dirname(os.path.abspath(__file__))
        + f"/models/bestlivmodel_{endpoint}_model.sav",
        "rb",
    ) as f:
        regressor = pickle.load(f)

    X = data_dummy[features]
    X = X.values
    # Add predictions to held out test set dili
    y_pred = regressor.predict(X)

    return y_pred


def predict_liv_all(data):
    # Read columns needed for rat data
    file = open(
        os.path.dirname(os.path.abspath(__file__))
        + "/models/features_morgan_mordred_maccs_physc.txt",
        "r",
    )
    file_lines = file.read()
    features = file_lines.split("\n")
    features = features[:-1]

    data_dummy = data

    for endpoint in LIV_DATA:
        y_proba = predict_individual_liv_data(data_dummy, features, endpoint)
        data[endpoint] = y_proba

    for endpoint in [
        "median pMolar unbound plasma concentration",
        "median pMolar total plasma concentration",
    ]:
        y_proba = predict_individual_cmax_data(data_dummy, features, endpoint)
        data[endpoint] = y_proba

    return data


def predict_DILI(data):

    # Read columns needed for rat data
    file = open(
        os.path.dirname(os.path.abspath(__file__))
        + f"/models/features_morgan_mordred_maccs_physc.txt",
        "r",
    )
    file_lines = file.read()
    features = file_lines.split("\n")
    features = features[:-1]

    features = (
        list(features)
        + [
            "median pMolar unbound plasma concentration",
            "median pMolar total plasma concentration",
        ]
        + list(LIV_DATA)
    )
    with open(
        os.path.dirname(os.path.abspath(__file__)) + "/models/final_dili_model.sav",
        "rb",
    ) as f:
        loaded_rf = pickle.load(f)

    X = data[features]
    y_proba = loaded_rf.predict_proba(X)[:, 1]
    best_thresh = 0.612911
    y_pred = [1 if y_proba > best_thresh else 0]

    explainer = shap.TreeExplainer(loaded_rf)
    shap_values = explainer.shap_values(X)

    flat_shaplist = [item for sublist in shap_values[1] for item in sublist]

    interpret = pd.DataFrame()
    interpret["name"] = features
    interpret["SHAP"] = flat_shaplist
    return (interpret, y_proba, y_pred)


class DILIPRedictor:
    def predict(self, smiles):
        logger.debug("Standardizing SMILES")
        smiles_r = standardized_smiles(smiles)
        if smiles_r == "Cannot_do":
            raise Exception("InvalidSMILESError")
        test = {"smiles_r": [smiles_r]}
        test = pd.DataFrame(test)

        desc = pd.read_csv(
            os.path.dirname(os.path.abspath(__file__))
            + "/models/all_features_desc.csv",
            encoding="windows-1252",
        )

        logger.debug("Calculating Descriptors")
        test_mfp_Mordred = calc_all_fp_desc(test)

        logger.debug("Loading Models")
        test_mfp_Mordred_liv = predict_liv_all(test_mfp_Mordred)
        test_mfp_Mordred_liv_values = test_mfp_Mordred_liv.T.reset_index().rename(
            columns={"index": "name", 0: "value"}
        )

        logger.debug("Models Predicting")
        interpret, y_proba, y_pred = predict_DILI(test_mfp_Mordred_liv)
        interpret = pd.merge(
            interpret, desc, right_on="name", left_on="name", how="outer"
        )
        interpret = pd.merge(
            interpret,
            test_mfp_Mordred_liv_values,
            right_on="name",
            left_on="name",
            how="inner",
        )

        if y_pred[0] == 1:
            logger.critical("The compound is predicted DILI-Positive")
        if y_pred[0] == 0:
            logger.critical("The compound is predicted DILI-Negative")

        logger.info(
            f"Unbound Cmax: {np.round(10**-test_mfp_Mordred_liv['median pMolar unbound plasma concentration'][0] *10**6, 2)} uM"
        )
        logger.info(
            f"Total Cmax: {np.round(10**-test_mfp_Mordred_liv['median pMolar total plasma concentration'][0] *10**6, 2)} uM"
        )

        top = interpret[interpret["SHAP"] > 0].sort_values(by=["SHAP"], ascending=False)
        proxy_DILI_SHAP_top = pd.merge(INFO, top[top["name"].isin(LIV_DATA)])
        proxy_DILI_SHAP_top["pred"] = proxy_DILI_SHAP_top["value"] > 0.50
        proxy_DILI_SHAP_top["SHAP contribution to Toxicity"] = "Positive"
        proxy_DILI_SHAP_top["smiles"] = smiles_r

        bottom = interpret[interpret["SHAP"] < 0].sort_values(
            by=["SHAP"], ascending=True
        )
        proxy_DILI_SHAP_bottom = pd.merge(INFO, bottom[bottom["name"].isin(LIV_DATA)])
        proxy_DILI_SHAP_bottom["pred"] = proxy_DILI_SHAP_bottom["value"] > 0.50
        proxy_DILI_SHAP_bottom["SHAP contribution to Toxicity"] = "Negative"
        proxy_DILI_SHAP_bottom["smiles"] = smiles_r

        SHAP = pd.DataFrame(
            columns=[
                "name",
                "source",
                "assaytype",
                "SHAP",
                "description",
                "value",
                "pred",
                "smiles",
            ]
        )
        SHAP = pd.concat([SHAP, proxy_DILI_SHAP_top])
        SHAP = pd.concat([SHAP, proxy_DILI_SHAP_bottom])
        SHAP["name"] = SHAP["name"].astype(str)
        SHAP = SHAP.sort_values(by=["name"], ascending=True)

        preds_DILI = pd.DataFrame(
            {
                "source": ["DILI"],
                "assaytype": ["DILIst_FDA"],
                "description": ["This is the predicted FDA DILIst label"],
                "value": [y_proba[0]],
                "pred": [y_pred[0]],
                "SHAP contribution to Toxicity": ["N/A"],
                "SHAP": ["N/A"],
            }
        )

        SHAP = SHAP[
            [
                "source",
                "assaytype",
                "description",
                "value",
                "pred",
                "SHAP contribution to Toxicity",
                "SHAP",
            ]
        ]
        SHAP = pd.concat([preds_DILI, SHAP]).reset_index(drop=True)
        SHAP["smiles"] = smiles
        SHAP["smiles_r"] = smiles_r

        return SHAP


def main():
    parser = argparse.ArgumentParser(
        description=BANNER + "\n\n" + ABSTRACT + "\n\n" + CITE,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "--smiles",
        "-s",
        "-smi",
        "--smi",
        "-smiles",
        help="Input SMILES string to predict properties",
    )
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    dili_predictor = DILIPRedictor()
    print(BANNER)
    print(CITE)

    result = dili_predictor.predict(args.smiles)
    filename = f"DILIPRedictor_{formatted_time}_{formatted_date}.csv"
    logger.info(f"Saving Results in {filename}")
    result.to_csv(filename, index=False)
    

if __name__ == "__main__":
    main()
