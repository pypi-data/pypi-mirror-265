from dilipred import DILIPRedictor

if __name__ == '__main__':
    dp = DILIPRedictor()
    smiles = "CCCCCCCO"
    result = dp.predict(smiles)
    assert result is not None