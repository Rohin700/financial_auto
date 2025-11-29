import pandas as pd # Provides powerful data structures (DataFrame & Series) for data analysis, manipulation, and processing.
import os # provide tools to interact with your operating system

def extract_sales_data(file_path):
    """
    Extract raw sales data from CSV.
    Validates file presence & expected columns.
    Returns DataFrame.
    """
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at: {file_path}")
    
    try : 
        df = pd.read_csv(file_path)
        print("Raw data loaded successfully")
    
    except Exception as e:
        raise Exception(f"Error reading CSV: {str(e)}")
    
    required_cols = ["date", "product", "category", "quantity", "price"]
    
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise Exception(f"Missing columns: {missing}")
    
    print("Columns validated")
    return df

if __name__ == "__main__":
    file_path = "../data/raw_sales.csv"
    df = extract_sales_data(file_path)

    print(df.head())
