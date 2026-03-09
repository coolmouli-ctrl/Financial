import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Interest Rate Calculator", page_icon="📊", layout="wide")

st.title("📊 Average Interest Rate Calculator")
st.markdown("Upload an Excel file with Principal and Interest data to calculate the average interest rate.")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)
        
        st.subheader("📋 Data Preview")
        st.dataframe(df, use_container_width=True)
        
        # Display basic info
        st.info(f"Total rows: {len(df)}")
        
        # Let user select columns
        col1, col2 = st.columns(2)
        
        with col1:
            principal_col = st.selectbox(
                "Select Principal Column",
                options=df.columns.tolist(),
                index=0 if len(df.columns) > 0 else None
            )
        
        with col2:
            interest_col = st.selectbox(
                "Select Interest Column",
                options=df.columns.tolist(),
                index=1 if len(df.columns) > 1 else None
            )
        
        # Option to specify if interest is already a rate or an amount
        interest_type = st.radio(
            "What does the Interest column represent?",
            options=["Interest Amount (needs calculation)", "Interest Rate (%)"],
            index=0
        )
        
        if st.button("Calculate Average Interest Rate", type="primary"):
            try:
                # Extract the selected columns
                principal = pd.to_numeric(df[principal_col], errors='coerce')
                interest = pd.to_numeric(df[interest_col], errors='coerce')
                
                # Remove rows with NaN or zero principal
                valid_mask = (~principal.isna()) & (~interest.isna()) & (principal != 0)
                principal_clean = principal[valid_mask]
                interest_clean = interest[valid_mask]
                
                if len(principal_clean) == 0:
                    st.error("No valid data found. Please check your Principal and Interest columns.")
                else:
                    # Calculate interest rates
                    if interest_type == "Interest Amount (needs calculation)":
                        interest_rates = (interest_clean / principal_clean) * 100
                        calculation_note = "Interest rates calculated as (Interest / Principal) × 100"
                    else:
                        interest_rates = interest_clean
                        calculation_note = "Interest rates taken directly from the data"
                    
                    # Calculate average
                    avg_interest_rate = interest_rates.mean()
                    
                    # Display results
                    st.success("✅ Calculation Complete!")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Average Interest Rate", f"{avg_interest_rate:.2f}%")
                    
                    with col_b:
                        st.metric("Minimum Rate", f"{interest_rates.min():.2f}%")
                    
                    with col_c:
                        st.metric("Maximum Rate", f"{interest_rates.max():.2f}%")
                    
                    st.info(calculation_note)
                    
                    # Show detailed breakdown
                    with st.expander("📊 View Detailed Breakdown"):
                        result_df = pd.DataFrame({
                            principal_col: principal_clean.values,
                            interest_col: interest_clean.values,
                            'Calculated Rate (%)': interest_rates.values
                        })
                        result_df.index = np.arange(1, len(result_df) + 1)
                        result_df.index.name = 'Row'
                        st.dataframe(result_df, use_container_width=True)
                        
                        # Summary statistics
                        st.subheader("Summary Statistics")
                        summary_data = {
                            'Metric': ['Count', 'Mean', 'Median', 'Std Dev', 'Min', 'Max'],
                            'Value': [
                                f"{len(interest_rates)}",
                                f"{interest_rates.mean():.2f}%",
                                f"{interest_rates.median():.2f}%",
                                f"{interest_rates.std():.2f}%",
                                f"{interest_rates.min():.2f}%",
                                f"{interest_rates.max():.2f}%"
                            ]
                        }
                        st.table(pd.DataFrame(summary_data))
                
            except Exception as e:
                st.error(f"Error during calculation: {str(e)}")
                st.info("Please ensure the selected columns contain numeric values.")
        
    except Exception as e:
        st.error(f"Error reading Excel file: {str(e)}")
        st.info("Please ensure you've uploaded a valid Excel file (.xlsx or .xls)")

else:
    st.info("👆 Please upload an Excel file to get started")
    
    # Show example format
    with st.expander("📝 Expected Excel Format"):
        st.markdown("""
        Your Excel file should have at least two columns:
        
        | Principal | Interest |
        |-----------|----------|
        | 10000     | 500      |
        | 20000     | 1200     |
        | 15000     | 900      |
        
        **Note:** 
        - Column names can be different (you'll select them in the app)
        - Interest can be either the amount or the rate percentage
        - The app will calculate the average interest rate from all rows
        """)
