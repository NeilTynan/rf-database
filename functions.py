def clean_currency(series):
    return (series
            .str.replace('€', '', regex=False)
            .str.replace('£', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.replace('- ', '-', regex=False)  # fix spaced negative sign
            .str.strip()
            .astype(float)
            .astype(int))