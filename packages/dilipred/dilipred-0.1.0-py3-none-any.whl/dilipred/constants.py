BANNER = """ 
██████████   █████ █████       █████ ███████████                         █████
░░███░░░░███ ░░███ ░░███       ░░███ ░░███░░░░░███                       ░░███ 
 ░███   ░░███ ░███  ░███        ░███  ░███    ░███ ████████   ██████   ███████ 
 ░███    ░███ ░███  ░███        ░███  ░██████████ ░░███░░███ ███░░███ ███░░███ 
 ░███    ░███ ░███  ░███        ░███  ░███░░░░░░   ░███ ░░░ ░███████ ░███ ░███ 
 ░███    ███  ░███  ░███      █ ░███  ░███         ░███     ░███░░░  ░███ ░███ 
 ██████████   █████ ███████████ █████ █████        █████    ░░██████ ░░████████
░░░░░░░░░░   ░░░░░ ░░░░░░░░░░░ ░░░░░ ░░░░░        ░░░░░      ░░░░░░   ░░░░░░░░ 
                                                                                                                                                
                                                                               """

ABSTRACT = """Drug-induced liver injury (DILI) presents a significant challenge in drug discovery, often leading to clinical trial failures and necessitating drug withdrawals. In this study, we introduce a novel method for DILI prediction that first predicts eleven proxy-DILI labels and then uses them as features in addition to chemical structural features to predict DILI. The features include in vitro (e.g., mitochondrial toxicity, bile salt export pump inhibition) data, in vivo (e.g., preclinical rat hepatotoxicity studies) data, pharmacokinetic parameters of maximum concentration, structural fingerprints, and physicochemical parameters. We trained DILI-prediction models on 1020 compounds from the DILIst dataset and tested on a held-out external test set of 255 compounds from DILIst dataset. The best model, DILIPredictor, attained a balanced accuracy of 70% and an LR+ score of 7.21. This model enabled the early detection of 26 toxic compounds compared to models using only structural features (4.62 LR+ score). Using feature interpretation from DILIPredictor, we were able to identify the chemical substructures causing DILI as well as differentiate cases DILI is caused by compounds in animals but not in humans. For example, DILIPredictor correctly recognized 2-butoxyethanol as non-toxic in humans despite its hepatotoxicity in mice models. Overall, the DILIPredictor model improves the detection of compounds causing DILI with an improved differentiation between animal and human sensitivity as well as the potential for mechanism evaluation. DILIPredictor is publicly available at https://broad.io/DILIPredictor for use via web interface and with all code available for download."""

CITE = """If you use DILIPred in your work, please cite:
Improved Early Detection of Drug-Induced Liver Injury by Integrating Predicted in vivo and in vitro Data
Srijit Seal, Dominic P. Williams, Layla Hosseini-Gerami, Ola Spjuth, Andreas Bender
bioRxiv 2024.01.10.575128; doi: https://doi.org/10.1101/2024.01.10.575128\n"""

DESCS = [
    "PSA",
    "n_rot_bonds",
    "n_rings",
    "n_ar_rings",
    "n_HBA",
    "n_HBD",
    "Fsp3",
    "logP",
    "NHOHCount",
    "NOCount",
    "NumHeteroatoms",
    "n_positive",
    "_n_negative",
    "n_ring_asmbl",
    "n_stereo",
]


LIV_DATA = ["2", "3", "5", "6", "7", "8", "10", "11", "14", "15", "16"]

SOURCE = [
    "Liver Toxicity Knowledge Base",
    "Human hepatotoxicity",
    "Animal hepatotoxicity A",
    "Animal hepatotoxicity B",
    "Preclinical hepatotoxicity",
    "Diverse DILI A",
    "Diverse DILI B",
    "Diverse DILI C",
    "BESP",
    "Mitotox",
    "Reactive Metabolite",
]


ASSAY_TYPE = [
    "DILI",
    "Human hepatotoxicity",
    "Animal hepatotoxicity",
    "Animal hepatotoxicity",
    "Animal hepatotoxicity",
    "Heterogenous Data ",
    "Heterogenous Data ",
    "Heterogenous Data ",
    "Mechanisms of Liver Toxicity",
    "Mechanisms of Liver Toxicity",
    "Mechanisms of Liver Toxicity",
]
