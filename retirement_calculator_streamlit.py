import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="Retirement Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-card {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    .danger-card {
        background-color: #f8d7da;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("💰 Retirement Calculator")
st.markdown("Plan your retirement with confidence")

# Create sidebar for inputs
with st.sidebar:
    st.header("📋 Your Information")
    
    # Personal Information
    st.subheader("Personal Details")
    current_age = st.number_input("Current Age", min_value=18, max_value=100, value=35)
    
    gender = st.radio("Gender", ("Male", "Female"))
    
    # Set inflation based on gender
    if gender == "Male":
        inflation_rate = 2.0
        st.info("✓ Inflation rate set to 2%")
    else:
        inflation_rate = 4.0
        st.info("✓ Inflation rate set to 4%")
    
    retirement_age = st.number_input("Desired Retirement Age", min_value=current_age+1, max_value=100, value=65)
    life_expectancy = st.number_input("Expected Life Expectancy", min_value=retirement_age+1, max_value=120, value=85)
    
    # Financial Information
    st.subheader("Financial Details")
    current_savings = st.number_input("Current Savings ($)", min_value=0, value=100000, step=1000)
    annual_contribution = st.number_input("Annual Contribution ($)", min_value=0, value=10000, step=1000)
    annual_return = st.slider("Expected Annual Return Rate (%)", min_value=0.0, max_value=15.0, value=7.0, step=0.5)
    
    # Retirement Expenses
    st.subheader("Retirement Expenses")
    annual_retirement_expense = st.number_input("Annual Retirement Expenses ($)", min_value=0, value=50000, step=1000)

# Calculate retirement metrics
years_to_retirement = retirement_age - current_age
years_in_retirement = life_expectancy - retirement_age

# Calculate savings at retirement
savings_at_retirement = current_savings
rate = annual_return / 100

for year in range(years_to_retirement):
    savings_at_retirement = savings_at_retirement * (1 + rate) + annual_contribution

# Calculate savings during retirement with inflation
savings_during_retirement = savings_at_retirement
current_expense = annual_retirement_expense
inflation = inflation_rate / 100
retirement_year = 0

for year in range(years_in_retirement):
    savings_during_retirement = savings_during_retirement * (1 + rate) - current_expense
    current_expense = current_expense * (1 + inflation)
    retirement_year += 1
    if savings_during_retirement < 0:
        break

# Determine status
is_sufficient = savings_during_retirement >= 0

# Main content area with columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Age", f"{current_age} years")

with col2:
    st.metric("Retirement Age", f"{retirement_age} years")

with col3:
    st.metric("Years to Retire", f"{years_to_retirement} years")

st.divider()

# Display key results
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Savings Projection")
    
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric("Current Savings", f"${current_savings:,.2f}")
    with metric_col2:
        st.metric("Annual Contribution", f"${annual_contribution:,.2f}")
    
    st.metric("Savings at Retirement (Age {})".format(retirement_age), 
              f"${savings_at_retirement:,.2f}", 
              delta=f"+${savings_at_retirement - current_savings:,.2f}")

with col2:
    st.subheader("💡 Retirement Details")
    
    detail_col1, detail_col2 = st.columns(2)
    with detail_col1:
        st.metric("Annual Return Rate", f"{annual_return}%")
    with detail_col2:
        st.metric("Inflation Rate", f"{inflation_rate}%")
    
    st.metric("Years in Retirement", f"{years_in_retirement} years")
    st.metric("Initial Annual Expenses", f"${annual_retirement_expense:,.2f}")

st.divider()

# Retirement Status
st.subheader("🎯 Retirement Status")

if is_sufficient:
    st.success(f"✓ **Great News!** Your savings will be SUFFICIENT for retirement!")
    st.markdown(f"""
    <div class="success-card">
        <h4>You will have enough savings! 🎉</h4>
        <p><strong>Remaining balance at age {life_expectancy}:</strong> ${savings_during_retirement:,.2f}</p>
        <p>Your retirement is financially secure based on current projections.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Calculate when money runs out
    savings = savings_at_retirement
    age = retirement_age
    expense = annual_retirement_expense
    while savings > 0 and age < life_expectancy:
        savings = savings * (1 + rate) - expense
        expense = expense * (1 + inflation)
        age += 1
    
    st.error(f"⚠️ Your savings will run out around age {age}")
    st.markdown(f"""
    <div class="danger-card">
        <h4>Action Required! ⚠️</h4>
        <p><strong>Projected money depletion age:</strong> {age}</p>
        <p><strong>Shortfall:</strong> ${abs(savings_during_retirement):,.2f}</p>
        <p>Consider increasing savings, delaying retirement, or reducing expenses.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Detailed year-by-year projection
st.subheader("📈 Year-by-Year Projection During Retirement")

# Generate projection data
projection_data = []
savings = savings_at_retirement
expense = annual_retirement_expense
current_age_retirement = retirement_age

for year in range(years_in_retirement):
    age = retirement_age + year
    savings = savings * (1 + rate) - expense
    projection_data.append({
        'Age': age,
        'Year': year + 1,
        'Savings': max(0, savings),
        'Annual Expense': expense,
        'Status': '✓ Solvent' if savings >= 0 else '✗ Depleted'
    })
    expense = expense * (1 + inflation)
    if savings <= 0:
        break

df = pd.DataFrame(projection_data)

# Format the dataframe for display
df['Savings'] = df['Savings'].apply(lambda x: f"${x:,.2f}")
df['Annual Expense'] = df['Annual Expense'].apply(lambda x: f"${x:,.2f}")

st.dataframe(df, use_container_width=True, hide_index=True)

# Create visualization
st.subheader("📉 Savings Over Time During Retirement")

# Regenerate data for chart
chart_data = []
savings = savings_at_retirement
expense = annual_retirement_expense

for year in range(years_in_retirement):
    age = retirement_age + year
    savings = savings * (1 + rate) - expense
    chart_data.append({'Age': age, 'Savings': max(0, savings)})
    expense = expense * (1 + inflation)
    if savings <= 0:
        break

chart_df = pd.DataFrame(chart_data)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(chart_df['Age'], chart_df['Savings'], marker='o', linewidth=2, markersize=6, color='#1f77b4')
ax.fill_between(chart_df['Age'], chart_df['Savings'], alpha=0.3, color='#1f77b4')
ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
ax.set_xlabel('Age', fontsize=12)
ax.set_ylabel('Savings ($)', fontsize=12)
ax.set_title('Projected Savings During Retirement (with Inflation)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))

st.pyplot(fig)

# Footer
st.divider()
st.caption("💡 **Disclaimer:** This calculator is for educational purposes. Consult a financial advisor for personalized advice.")
