import unittest
from pathlib import Path
import pandas as pd
from data.data_processor import process_data, base_data_dir
from config.settings import DATA_DIR, INDEX_PROXY_TICKER

class TestDataProcessor(unittest.TestCase):
    def test_process_data(self):
        # Define output path for processed data
        processed_data_path = Path(DATA_DIR) / "test_processed_data.feather"

        # Run the data processing function
        processed_data = process_data(base_data_dir, output_path=processed_data_path)

        # Assert the result is not None and not empty
        self.assertIsNotNone(processed_data, "Processed data should not be None.")
        self.assertFalse(processed_data.empty, "Processed data should not be empty.")

        # Assert the file was saved
        self.assertTrue(processed_data_path.exists(), "Processed data file was not saved.")

        # Validate the reading of the saved file and assert expected columns
        df = pd.read_feather(processed_data_path)

        # Assert the DataFrame is not empty
        self.assertFalse(df.empty, "Loaded DataFrame should not be empty.")

        # Assert critical columns exist in the processed data
        expected_columns = [
            "50_MA", 
            "200_MA", 
            "50_Vol_Avg",
            "Price_Change", 
            "52_Week_High",
            "Is_New_High",
            "Volume_Spike",
            "Stock_Returns",
            "Cumulative_Stock_Returns",
            "Relative_Strength",
            "INDEX_Close",  
            "Cumulative_INDEX_Returns",  
            "INDEX_50_MA",  
            "INDEX_200_MA"  
        ]
        for col in expected_columns:
            self.assertIn(col, df.columns, f"'{col}' column is missing in the processed data.")

        # Check if the index proxy data is included
        self.assertTrue((df['ticker'] == INDEX_PROXY_TICKER).any(), f"'{INDEX_PROXY_TICKER}' data is missing in the processed dataset.")

        # Additional suggestion: Verify no NaN values in critical columns (if that's expected behavior)
        #for col in expected_columns:
        #    self.assertFalse(df[col].isna().any(), f"'{col}' column contains NaN values.")

        # Cleanup
        processed_data_path.unlink()  # Delete the test file after running

if __name__ == "__main__":
    unittest.main()