import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from openai import OpenAI
import random


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

st.markdown(
"""
<style>

.metric-card {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    text-align: center;
}

.metric-title {
    font-size: 14px;
    color: #6b7280;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #111827;
}

</style>
""",
unsafe_allow_html=True
)

st.set_page_config(
    page_title="RevenuePilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #F8FAFC;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1300px;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #E5E7EB;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: none;
    background: #4F46E5;
    color: white;
    font-weight: 600;
    padding: 0.7rem;
}

.stButton > button:hover {
    background: #4338CA;
}

</style>
""", unsafe_allow_html=True)


df = pd.read_excel(
    "AI Sales Copilot-SDR Intelligence Platform.xlsx"
)

def generate_ai_analysis(company):

    score = company["Account Score"]

    if score >= 80:
        intent = "High buying intent detected"
        strategy = "Focus on business impact, growth and sales scaling."
        cta = "Book a discovery call with the sales team."

    elif score >= 60:
        intent = "Moderate buying signals detected"
        strategy = "Start with educational content and identify pain points."
        cta = "Open a conversation with a personalized message."

    else:
        intent = "Low urgency account"
        strategy = "Keep monitoring activity and nurture the relationship."
        cta = "Add to long-term prospecting sequence."


    analysis = f"""

## 🤖 AI Account Brief

### Company
{company['Company Name']}

### Account Intelligence

Industry:
{company['Industry']}

Country:
{company['Country']}

Account Score:
{score}/100


### Buying Intent

{intent}


### Recommended Sales Strategy

{strategy}


### Next Best Action

{cta}


### LinkedIn Message

Hi {company['Contact Name']},

I noticed that {company['Company Name']} is growing in the
{company['Industry']} space.

Given your recent activity, I thought it could be interesting
to exchange ideas around scaling sales operations.

Would love to connect.


### Cold Email

Subject:
Scaling sales efficiency at {company['Company Name']}


Hi {company['Contact Name']},

I noticed your team is experiencing growth signals.

Companies at this stage often look for ways to improve
sales efficiency and prioritize the right accounts.

Would you be open to a quick conversation?

Best,
Dayna

"""

    return analysis

def metric_card(title, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                {title}
            </div>
            <div class="metric-value">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def score_gauge(score):

    fig = px.pie(
        values=[score,100-score],
        names=["Score","Remaining"],
        hole=0.7,
        title="Account Score"
    )

    fig.update_traces(
        textinfo="none"
    )

    fig.update_layout(
        showlegend=False,
        height=250
    )

    return fig

st.markdown("""
<div style="
padding:30px;
border-radius:18px;
background:linear-gradient(135deg,#4F46E5,#7C3AED);
color:white;
margin-bottom:25px;
">

<h1 style="margin-bottom:5px;">
RevenuePilot AI
</h1>

<p style="font-size:18px;margin-top:0;">
AI-powered Sales Intelligence Platform for Modern SDR Teams
</p>

<p style="opacity:0.85;">
Prioritize accounts • Detect buying signals • Generate personalized outreach
</p>

</div>
""", unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    metric_card(
        " Total Accounts",
        len(df)
    )

with kpi2:
    metric_card(
        " Average Score",
        round(df["Account Score"].mean(),1)
    )

with kpi3:
    high_accounts = len(
        df[
            df["Priority Level"]
            .fillna("")
            .str.contains("HIGH", case=False)
        ]
    )

    metric_card(
        " High Priority",
        high_accounts
    )

with kpi4:
    metric_card(
        " Countries",
        df["Country"].nunique()
    )

st.divider()
st.subheader("📊 Sales Pipeline Overview")

fig = px.histogram(
    df,
    x="Account Score",
    nbins=10,
    title="Account Score Distribution"
)

st.plotly_chart(fig, use_container_width=True)

industry_counts = (
    df["Industry"]
    .value_counts()
    .reset_index()
)

industry_counts.columns = ["Industry", "Count"]

fig2 = px.bar(
    industry_counts,
    x="Industry",
    y="Count",
    title="Accounts by Industry"
)

st.plotly_chart(fig2, use_container_width=True)

st.sidebar.markdown(
"""
Select an account to generate an AI-powered sales analysis.
"""
)

st.sidebar.divider()

st.sidebar.subheader("🏢 Account Selection")

# Load data


# Dropdown list of companies
company = st.sidebar.selectbox(
    "Choose a company",
    df["Company Name"]
)

# Show selected company data
selected_data = df[df["Company Name"] == company]

st.subheader("Company Details")
st.dataframe(selected_data)
company = selected_data.iloc[0]

st.divider()
tab1, tab2, tab3, tab4 = st.tabs([
    "Company",
    "Signals",
    "AI Insights",
    "💬 Outreach"
])
with tab1:
    st.markdown("## 🏢 Company Overview")
    col1, col2 = st.columns(2)

with col1:
    st.write(f"**Company:** {company['Company Name']}")
    st.write(f"**Industry:** {company['Industry']}")
    st.write(f"**Country:** {company['Country']}")
    st.write(f"**Employees:** {company['Employees']}")
    st.write(f"**Website:** {company['Website']}")

with col2:

    st.plotly_chart(
        score_gauge(
            company["Account Score"]
        ),
        use_container_width=True
    )

    st.metric(
        "Priority Level",
        company["Priority Level"]
    )
    st.metric(
        "Priority Level",
        company['Priority Level']
    )

    st.write(f"Reason:{company['Scoring Reason']}")

st.divider()
with tab2:
    st.markdown("## 📈 Buying Signals")


    signal1, signal2, signal3 = st.columns(3)


with signal1:
    st.info(
        f"""
        FUNDING :

        {company['Recent Funding']}

        Potential budget  ↑ 
        """
    )


with signal2:
    st.info(
        f"""
        HIRING :

        {company['Hiring Sales Team']}

        Sales organization  ↑ 
        """
    )


with signal3:
    st.info(
        f"""
        EXPANSION :

        {company['International Expansion']}

        New market opportunity
        """
    )


signal4, signal5 = st.columns(2)


with signal4:
    st.success(
        f"""
        TRAFFIC GROWTH :

        {company['Website Traffic Growth']}

        Market interest  ↑ 
        """
    )


with signal5:
    st.warning(
        f"""
        TECHNOLOGY GROWTH :

        {company['Tech Growth']}

        Digital transformation signal
        """
    )

st.divider()

with tab3:
    st.markdown(
    "## 🎯 Recommended Sales Strategy"
)


strategy_col1, strategy_col2 = st.columns(2)


with strategy_col1:

    st.info(
        f"""
        **Target Persona**

        👤 {company['Contact Name']}

        Role:
        {company['Job Title'] if 'Job Title' in company else 'Decision Maker'}

        Recommended channel:

        LinkedIn + Email
        """
    )


with strategy_col2:

    if company["Account Score"] >= 80:

        st.success(
            """
            **Recommended Approach**

            🔥 High-value account

            Focus on:
            - Business impact
            - Growth challenges
            - Scaling sales operations

            CTA:
            Book a discovery call
            """
        )

    else:

        st.warning(
            """
            **Recommended Approach**

            Nurture account.

            Focus on:
            - Education
            - Industry insights
            - Future opportunities
            """
        )

st.divider()
with tab4:
    st.markdown("## 🎯 Account Prioritization")

    st.write(f"**Account Score:** {company['Account Score']}/100")
    st.write(f"**Priority Level:** {company['Priority Level']}")
    st.write(f"**Scoring Reason:** {company['Scoring Reason']}")

    st.divider()
    st.markdown("## 🤖 SDR Recommendation")

    priority = company["Priority Level"]

if "🔥 HIGH" in str(priority):
    st.success("Contact this account immediately. Strong buying signals detected.")

elif "MEDIUM" in str(priority):
    st.warning("Good opportunity. Consider a personalized outreach.")

else:
    st.info("Low priority account. Keep under observation.")


ai_result = generate_ai_analysis(company)


st.markdown("## 🤖 AI Account Intelligence")


col1, col2 = st.columns(2)


with col1:
    st.metric(
        "Account Score",
        f"{company['Account Score']}/100"
    )


with col2:

    if company["Account Score"] >= 80:
        st.metric(
            "Buying Intent",
            "🔥 HIGH"
        )
    else:
        st.metric(
            "Buying Intent",
            "MEDIUM"
        )


st.divider()


st.markdown("### 🎯 Recommended Sales Strategy")

st.info(
    """
    Focus on business impact, growth challenges
    and sales scaling opportunities.
    """
)


st.markdown("### ⚡ Next Best Action")

st.success(
    """
    Book a discovery call with the sales team.
    """
)


st.markdown("### 💬 Outreach Generated")


tab1, tab2 = st.tabs(
    [
        "LinkedIn Message",
        "Cold Email"
    ]
)


with tab1:
    st.write(
        f"""
Hi {company['Contact Name']},

I noticed {company['Company Name']}
is growing in the {company['Industry']} space.

Would love to exchange ideas about
scaling sales operations.

Best, 

Dayna
        """
    )


with tab2:
    st.write(
        f"""
Subject:
Scaling sales efficiency at {company['Company Name']}


Hi {company['Contact Name']},

I noticed your company is experiencing
growth signals.

Would you be open to a quick conversation?

Best, 

Dayna
        """
    )