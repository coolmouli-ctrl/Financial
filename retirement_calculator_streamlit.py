import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def get_default_openai_key() -> str:
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    return os.getenv("OPENAI_API_KEY", "")


def clean_json_response(raw_text: str) -> str:
    text = raw_text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        for part in parts:
            candidate = part.strip()
            if candidate.startswith("json"):
                candidate = candidate[4:].strip()
            if candidate.startswith("{") and candidate.endswith("}"):
                return candidate
    return text


def simulate_retirement(profile: dict, return_rate_pct: float, inflation_pct: float, expense_multiplier: float = 1.0) -> dict:
    years_to_retirement = profile["retirement_age"] - profile["current_age"]
    years_in_retirement = profile["life_expectancy"] - profile["retirement_age"]

    savings_at_retirement = profile["current_savings"]
    rate = return_rate_pct / 100

    for _ in range(years_to_retirement):
        savings_at_retirement = savings_at_retirement * (1 + rate) + profile["annual_contribution"]

    savings_during_retirement = savings_at_retirement
    current_expense = profile["annual_retirement_expense"] * expense_multiplier
    inflation = inflation_pct / 100
    depletion_age = None

    for year in range(years_in_retirement):
        savings_during_retirement = savings_during_retirement * (1 + rate) - current_expense
        current_expense = current_expense * (1 + inflation)
        if savings_during_retirement < 0:
            depletion_age = profile["retirement_age"] + year + 1
            break

    return {
        "savings_at_retirement": savings_at_retirement,
        "ending_balance": savings_during_retirement,
        "is_sufficient": savings_during_retirement >= 0,
        "depletion_age": depletion_age,
    }


def get_chatbot_reply(user_question: str, profile: dict, model_name: str, api_key: str) -> str:
    if OpenAI is None:
        return "The OpenAI package is not installed. Run `pip install openai` and restart the app."
    if not api_key:
        return "Add your OpenAI API key in sidebar AI settings (or set OPENAI_API_KEY) to use the chatbot."

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are a retirement planning assistant in a Streamlit app. "
        "Give clear, practical, and concise explanations for non-experts. "
        "Do not claim certainty. Mention trade-offs and suggest next actions. "
        "This is educational content, not financial advice."
    )

    context = (
        "User profile and projection context:\n"
        f"- Current age: {profile['current_age']}\n"
        f"- Retirement age: {profile['retirement_age']}\n"
        f"- Life expectancy: {profile['life_expectancy']}\n"
        f"- Current savings: ${profile['current_savings']:,.2f}\n"
        f"- Annual contribution: ${profile['annual_contribution']:,.2f}\n"
        f"- Expected annual return: {profile['annual_return']}%\n"
        f"- Annual retirement expense: ${profile['annual_retirement_expense']:,.2f}\n"
        f"- Inflation: {profile['inflation_rate']}%\n"
        f"- Savings at retirement: ${profile['savings_at_retirement']:,.2f}\n"
        f"- Ending balance by life expectancy: ${profile['ending_balance']:,.2f}"
    )

    completion = client.chat.completions.create(
        model=model_name,
        temperature=0.4,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": context},
            {"role": "user", "content": user_question},
        ],
    )
    return completion.choices[0].message.content


def generate_ai_scenarios(profile: dict, model_name: str, api_key: str) -> dict:
    if OpenAI is None:
        return {"error": "The OpenAI package is not installed. Run `pip install openai` and restart the app."}
    if not api_key:
        return {"error": "Add your OpenAI API key in sidebar AI settings (or set OPENAI_API_KEY)."}

    client = OpenAI(api_key=api_key)

    prompt = f"""
Create exactly three retirement planning scenarios for this user:
- current_age: {profile['current_age']}
- retirement_age: {profile['retirement_age']}
- life_expectancy: {profile['life_expectancy']}
- current_savings: {profile['current_savings']}
- annual_contribution: {profile['annual_contribution']}
- annual_return: {profile['annual_return']}
- annual_retirement_expense: {profile['annual_retirement_expense']}
- inflation_rate: {profile['inflation_rate']}

Return valid JSON only with this exact schema:
{{
  "scenarios": [
    {{
      "name": "Optimistic",
      "annual_return_pct": number,
      "inflation_pct": number,
      "annual_expense_change_pct": number,
      "analysis": "short explanation"
    }},
    {{
      "name": "Realistic",
      "annual_return_pct": number,
      "inflation_pct": number,
      "annual_expense_change_pct": number,
      "analysis": "short explanation"
    }},
    {{
      "name": "Conservative",
      "annual_return_pct": number,
      "inflation_pct": number,
      "annual_expense_change_pct": number,
      "analysis": "short explanation"
    }}
  ]
}}

Rules:
- Keep values realistic and diverse.
- annual_expense_change_pct means % change to the base annual retirement expense.
- Keep analysis under 35 words per scenario.
"""

    completion = client.chat.completions.create(
        model=model_name,
        temperature=0.5,
        messages=[
            {
                "role": "system",
                "content": "You generate structured retirement scenarios. Return strict JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    raw = completion.choices[0].message.content
    cleaned = clean_json_response(raw)
    parsed = json.loads(cleaned)
    return parsed

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
    current_age = st.number_input("Current Age", min_value=18, max_value=100, value=46)
    
    retirement_age = st.number_input("Desired Retirement Age", min_value=current_age+1, max_value=100, value=65)
    life_expectancy = st.number_input("Expected Life Expectancy", min_value=retirement_age+1, max_value=120, value=85)
    
    # Financial Information
    st.subheader("Financial Details")
    current_savings = st.number_input("Current Savings ($)", min_value=0, value=100000, step=1000)
    annual_contribution = st.number_input("Annual Contribution ($)", min_value=0, value=0, step=1000)
    annual_return = st.slider("Expected Annual Return Rate (%)", min_value=0.0, max_value=15.0, value=1.5, step=0.5)
    
    # Retirement Expenses
    st.subheader("Retirement Expenses")
    annual_retirement_expense = st.number_input("Annual Retirement Expenses ($)", min_value=0, value=50000, step=1000)
    
    # Inflation Rate
    st.subheader("Inflation")
    inflation_rate = st.slider("Expected Inflation Rate (%)", min_value=0.0, max_value=10.0, value=2.5, step=0.1)

    st.subheader("🤖 AI Settings")
    model_name = st.text_input("OpenAI Model", value="gpt-4o-mini")
    api_key_input = st.text_input(
        "OpenAI API Key",
        value=st.session_state.get("openai_api_key", get_default_openai_key()),
        type="password",
        help="Stored only for this app session.",
    )
    st.session_state["openai_api_key"] = api_key_input.strip()

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

profile = {
    "current_age": current_age,
    "retirement_age": retirement_age,
    "life_expectancy": life_expectancy,
    "current_savings": float(current_savings),
    "annual_contribution": float(annual_contribution),
    "annual_return": float(annual_return),
    "annual_retirement_expense": float(annual_retirement_expense),
    "inflation_rate": float(inflation_rate),
    "savings_at_retirement": float(savings_at_retirement),
    "ending_balance": float(savings_during_retirement),
}

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

st.divider()
st.subheader("🤖 AI Assistant")

if "scenario_df" not in st.session_state:
    st.session_state["scenario_df"] = None

ai_tab1, ai_tab2 = st.tabs(["Retirement Chatbot", "Scenario Generator"])

with ai_tab1:
    st.caption("Ask questions about your plan, trade-offs, and practical next steps.")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Ask me anything about your retirement plan. I can explain gaps and suggest adjustments.",
            }
        ]

    if st.button("Clear Chat", key="clear_chat_btn"):
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Ask me anything about your retirement plan. I can explain gaps and suggest adjustments.",
            }
        ]
        st.rerun()

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_prompt = st.chat_input("Example: How can I retire 3 years earlier?")
    if user_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    reply = get_chatbot_reply(
                        user_question=user_prompt,
                        profile=profile,
                        model_name=model_name,
                        api_key=st.session_state.get("openai_api_key", ""),
                    )
                except Exception as ex:
                    reply = f"I hit an error while generating the response: {ex}"
                st.write(reply)

        st.session_state.chat_messages.append({"role": "assistant", "content": reply})

with ai_tab2:
    st.caption("Generate AI-based optimistic, realistic, and conservative scenarios from your inputs.")

    scenario_btn_col1, scenario_btn_col2 = st.columns(2)
    with scenario_btn_col1:
        generate_clicked = st.button("Generate AI Scenarios", use_container_width=True)
    with scenario_btn_col2:
        clear_clicked = st.button("Clear Scenarios", use_container_width=True, key="clear_scenarios_btn")

    if clear_clicked:
        st.session_state["scenario_df"] = None
        st.rerun()

    if generate_clicked:
        with st.spinner("Generating scenarios..."):
            try:
                scenario_payload = generate_ai_scenarios(
                    profile=profile,
                    model_name=model_name,
                    api_key=st.session_state.get("openai_api_key", ""),
                )

                if "error" in scenario_payload:
                    st.error(scenario_payload["error"])
                else:
                    scenario_rows = []
                    for scenario in scenario_payload.get("scenarios", []):
                        expense_multiplier = 1 + (float(scenario["annual_expense_change_pct"]) / 100)
                        result = simulate_retirement(
                            profile,
                            return_rate_pct=float(scenario["annual_return_pct"]),
                            inflation_pct=float(scenario["inflation_pct"]),
                            expense_multiplier=expense_multiplier,
                        )

                        scenario_rows.append(
                            {
                                "Scenario": scenario["name"],
                                "Return %": float(scenario["annual_return_pct"]),
                                "Inflation %": float(scenario["inflation_pct"]),
                                "Expense Change %": float(scenario["annual_expense_change_pct"]),
                                "Savings at Retirement": result["savings_at_retirement"],
                                "End Balance": result["ending_balance"],
                                "Status": "✓ Sufficient" if result["is_sufficient"] else "⚠️ Shortfall",
                                "Depletion Age": result["depletion_age"] if result["depletion_age"] else "N/A",
                                "AI Analysis": scenario["analysis"],
                            }
                        )

                    scenario_df = pd.DataFrame(scenario_rows)
                    st.session_state["scenario_df"] = scenario_df

                    display_df = scenario_df.copy()
                    display_df["Savings at Retirement"] = display_df["Savings at Retirement"].map(lambda x: f"${x:,.2f}")
                    display_df["End Balance"] = display_df["End Balance"].map(lambda x: f"${x:,.2f}")

                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                    st.info("Use these scenarios to stress-test your plan and compare what changes are most impactful.")
            except Exception as ex:
                st.error(f"Unable to generate scenarios: {ex}")

    if st.session_state.get("scenario_df") is not None and not st.session_state["scenario_df"].empty:
        existing_df = st.session_state["scenario_df"]
        display_df = existing_df.copy()
        display_df["Savings at Retirement"] = display_df["Savings at Retirement"].map(lambda x: f"${x:,.2f}")
        display_df["End Balance"] = display_df["End Balance"].map(lambda x: f"${x:,.2f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        csv_bytes = existing_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Export Scenarios to CSV",
            data=csv_bytes,
            file_name="retirement_ai_scenarios.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_scenarios_csv",
        )

# Footer
st.divider()
st.caption("💡 **Disclaimer:** This calculator is for educational purposes. Consult a financial advisor for personalized advice.")
