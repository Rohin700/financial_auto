import pandas as pd

def transform_sales_data(df):
    """
    Clean and transform raw sales data.
    Returns cleaned data frame
    """
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'], errors = 'coerce')
    
    # Drop rows where date couldn't be parsed
    df = df.dropna(subset = ['date'])
    
    # Remove duplicate
    df = df.drop_duplicates()
    
    # Remove invalid values
    df = df[(df['quantity'] > 0) & (df['price'] > 0)]
    
    # Filling missing Text witht 'Unknown'
    df['product'] = df['product'].fillna("Unknown")
    df['category'] = df['category'].fillna("Unknown")

    # Calculate Revenue and also a new kpi is added
    df['revenue'] = df['quantity'] * df['price']
    
    print("Transformation Complete")
    return df

if __name__ == "__main__":
    from extract import extract_sales_data
    raw_df = extract_sales_data("../data/raw_sales.csv")
    
    cleaned_df = transform_sales_data(raw_df)
    cleaned_df.to_csv("../data/cleaned_sales.csv", index=False)
    
    print(cleaned_df.head())
    
    