import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
import hashlib
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Heart Disease Analysis Dashboard",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Password configuration - Change these values for your security
CORRECT_PASSWORD = "heartdisease2024"  # Change this to your desired password
HASHED_PASSWORD = hashlib.sha256(CORRECT_PASSWORD.encode()).hexdigest()

def check_password():
    """Returns `True` if the user has entered the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == HASHED_PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1 style="color: #e74c3c; font-size: 3rem; margin-bottom: 1rem;">🔒 Secure Access</h1>
        <h2 style="color: #2c3e50; font-size: 1.5rem; margin-bottom: 2rem;">Heart Disease Analysis Dashboard</h2>
        <p style="color: #7f8c8d; font-size: 1.1rem;">Please enter the password to access the medical dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the password input
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password",
            placeholder="Enter dashboard password..."
        )
        
        if "password_correct" in st.session_state:
            if not st.session_state["password_correct"]:
                st.error("❌ Incorrect password. Please try again.")
            
    # Add some styling and information
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;">
        <h3 style="color: #2c3e50; margin-bottom: 1rem;">🏥 About This Dashboard</h3>
        <p style="color: #6c757d; font-size: 1rem; line-height: 1.6;">
            This dashboard provides comprehensive analysis of heart disease data including:
        </p>
        <div style="display: flex; justify-content: space-around; margin-top: 1.5rem; flex-wrap: wrap;">
            <div style="margin: 0.5rem;">
                <span style="font-size: 1.5rem;">👥</span><br>
                <strong>Demographics</strong>
            </div>
            <div style="margin: 0.5rem;">
                <span style="font-size: 1.5rem;">🏥</span><br>
                <strong>Clinical Data</strong>
            </div>
            <div style="margin: 0.5rem;">
                <span style="font-size: 1.5rem;">⚠️</span><br>
                <strong>Risk Factors</strong>
            </div>
            <div style="margin: 0.5rem;">
                <span style="font-size: 1.5rem;">💡</span><br>
                <strong>Insights</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #adb5bd;">
        <small>🔐 Secure Medical Data Analysis • MSBA 382 Project</small>
    </div>
    """, unsafe_allow_html=True)
    
    return False

# Define medical-themed color palettes
MEDICAL_COLORS = {
    'primary': '#e74c3c',      # Red - primary medical color
    'secondary': '#3498db',     # Blue - secondary medical color
    'success': '#27ae60',       # Green - healthy/good
    'warning': '#f39c12',       # Orange - warning/caution
    'info': '#17a2b8',         # Teal - informational
    'purple': '#8e44ad',        # Purple - analysis
    'dark_blue': '#2c3e50',     # Dark blue - professional
    'light_green': '#2ecc71',   # Light green - positive
    'coral': '#ff7675',         # Coral - attention
    'navy': '#34495e'           # Navy - stability
}

# Color schemes for different chart types - FIXED: Using string keys
HEART_DISEASE_COLORS = {'No Heart Disease': MEDICAL_COLORS['success'], 'Heart Disease': MEDICAL_COLORS['primary']}
AGE_GROUP_COLORS = [MEDICAL_COLORS['info'], MEDICAL_COLORS['secondary'], MEDICAL_COLORS['warning'], 
                   MEDICAL_COLORS['coral'], MEDICAL_COLORS['purple']]
GENDER_COLORS = {'Male': MEDICAL_COLORS['secondary'], 'Female': MEDICAL_COLORS['coral']}
CHEST_PAIN_COLORS = [MEDICAL_COLORS['success'], MEDICAL_COLORS['warning'], 
                    MEDICAL_COLORS['coral'], MEDICAL_COLORS['primary']]
RISK_GRADIENT = ['#27ae60', '#f39c12', '#e74c3c']  # Green to Orange to Red

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #e74c3c;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #c0c0c0;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e74c3c;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        width: 200px; /* Optional: Fix width for uniformity */
        height: 100px; /* Adjust height based on content */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        margin: 0.5rem;
        white-space: nowrap; /* Prevent line breaks */
        overflow: hidden;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.3rem;
    }

    .metric-label {
        font-size: 1rem;
        color: #7f8c8d;
        font-weight: 500;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }

    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    
    /* Logout button styling */
    .logout-button {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
        background-color: #e74c3c;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.9rem;
    }
    
    .logout-button:hover {
        background-color: #c0392b;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and comprehensively clean the heart disease dataset"""
    # Load the dataset
    df = pd.read_csv('heart_disease_uci.csv')

    # Clean column names
    df.columns = df.columns.str.strip()
    
    # STEP 1: Handle Impossible Medical Values
    # Replace impossible cholesterol values (0) with NaN
    df.loc[df['chol'] == 0, 'chol'] = np.nan
    
    
    # Drop variables with >40% missing data (ca, thal, slope)
    high_missing_vars = ['ca', 'thal', 'slope']
    vars_to_drop = [var for var in high_missing_vars if var in df.columns]
    df_cleaned = df.drop(columns=vars_to_drop)
    
    # STEP 4: Handle Moderate Missing Values with Imputation
    # Numerical variables - use median imputation
    numerical_cols = ['chol', 'trestbps', 'thalch', 'oldpeak']
    for col in numerical_cols:
        if col in df_cleaned.columns and df_cleaned[col].isnull().any():
            median_val = df_cleaned[col].median()
            df_cleaned[col].fillna(median_val, inplace=True)
    
    # Categorical variables - use mode imputation
    categorical_cols = ['cp', 'fbs', 'restecg', 'exang']
    for col in categorical_cols:
        if col in df_cleaned.columns and df_cleaned[col].isnull().any():
            mode_val = df_cleaned[col].mode()[0] if not df_cleaned[col].mode().empty else 0
            df_cleaned[col].fillna(mode_val, inplace=True)
    
    # STEP 5: Create Binary Target Variable (keep as int for computations)
    df_cleaned['has_heart_disease'] = (df_cleaned['num'] > 0).astype(int)

    # Map fasting blood sugar
    if 'fbs' in df_cleaned.columns:
        df_cleaned['fbs'] = df_cleaned['fbs'].map({1: '>120 mg/dl', 0: '≤120 mg/dl'})
    
    # Map resting ECG results
    if 'restecg' in df_cleaned.columns:
        restecg_mapping = {
            0: 'Normal',
            1: 'ST-T Abnormality',
            2: 'LV Hypertrophy'
        }
        df_cleaned['restecg'] = df_cleaned['restecg'].map(restecg_mapping)
    
    
    # STEP 8: Create Derived Variables for Analysis
    # Create age groups
    df_cleaned['age_group'] = pd.cut(df_cleaned['age'], 
                                   bins=[0, 40, 50, 60, 70, 100], 
                                   labels=['<40', '40-49', '50-59', '60-69', '70+'])
    
    # Create cholesterol categories
    df_cleaned['chol_category'] = pd.cut(df_cleaned['chol'], 
                                       bins=[0, 200, 240, 1000], 
                                       labels=['Normal (<200)', 'Borderline (200-239)', 'High (≥240)'])
    
    # Create blood pressure categories
    df_cleaned['bp_category'] = pd.cut(df_cleaned['trestbps'], 
                                     bins=[0, 120, 140, 1000], 
                                     labels=['Normal (<120)', 'Elevated (120-139)', 'High (≥140)'])
    
    # Create max heart rate categories
    df_cleaned['hr_category'] = pd.cut(df_cleaned['thalch'], 
                                     bins=[0, 120, 150, 220], 
                                     labels=['Low (<120)', 'Normal (120-149)', 'High (≥150)'])
    
    # STEP 9: Data Quality Flags
    # Flag records with potential data quality issues
    df_cleaned['low_hr_flag'] = (df_cleaned['thalch'] < 80).astype(int)
    df_cleaned['high_chol_flag'] = (df_cleaned['chol'] > 400).astype(int)
    df_cleaned['high_bp_flag'] = (df_cleaned['trestbps'] > 180).astype(int)
    
    return df_cleaned

def add_display_columns(df):
    """Add string versions of categorical columns for proper color mapping"""
    df_display = df.copy()
    
    # Create string version of heart disease for color mapping
    df_display['heart_disease_label'] = df_display['has_heart_disease'].map({
        0: 'No Heart Disease', 
        1: 'Heart Disease'
    })
    
    # Create string version of exang for color mapping
    df_display['exang_label'] = df_display['exang'].map({
        False: 'No', 
        True: 'Yes'
    })
    
    # Create string version of fbs for color mapping (if it's still numeric)
    if df_display['fbs'].dtype in ['int64', 'float64']:
        df_display['fbs_label'] = df_display['fbs'].map({
            0: '≤120 mg/dl', 
            1: '>120 mg/dl'
        })
    else:
        df_display['fbs_label'] = df_display['fbs']
    
    return df_display

def create_overview_metrics(df):
    """Create overview metrics cards with icons"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-label">👥 Total Patients</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        heart_disease_count = df['has_heart_disease'].sum()
        heart_disease_rate = (heart_disease_count / len(df)) * 100
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{heart_disease_count:,}</div>
            <div class="metric-label">🫀 Heart Cases ({heart_disease_rate:.1f}%)</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        avg_age = df['age'].mean()
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{avg_age:.1f}</div>
            <div class="metric-label">📅 Avg Age (years)</div>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        male_count = (df['sex'] == 'Male').sum()
        male_percentage = (male_count / len(df)) * 100
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{male_count:,}</div>
            <div class="metric-label">👨 Male Patients ({male_percentage:.1f}%)</div>
        </div>
        ''', unsafe_allow_html=True)

def create_demographic_analysis(df):
    """Create demographic analysis visualizations"""
    st.markdown('<div class="section-header">👥 Demographic Analysis</div>', unsafe_allow_html=True)
    
    # Add display columns for proper color mapping
    df_display = add_display_columns(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Heart disease distribution by age group with themed colors
        age_disease = df_display.groupby(['age_group', 'heart_disease_label']).size().reset_index(name='count')
        
        # Calculate percentages for each age group
        age_totals = df_display.groupby('age_group').size().reset_index(name='total')
        age_disease = age_disease.merge(age_totals, on='age_group')
        age_disease['percentage'] = (age_disease['count'] / age_disease['total'] * 100).round(1)
        
        fig = px.bar(age_disease, x='age_group', y='count', color='heart_disease_label',
                    title='Heart Disease Distribution by Age Group',
                    labels={'age_group': 'Age Group', 'count': 'Number of Patients', 'heart_disease_label': 'Heart Disease'},
                    color_discrete_map=HEART_DISEASE_COLORS,
                    text='percentage')
        
        # Add percentage labels inside bars
        fig.update_traces(texttemplate='%{text}%', textposition='inside')
        fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gender distribution by heart disease with custom colors
        gender_disease = df_display.groupby(['sex', 'heart_disease_label']).size().reset_index(name='count')
        
        # Calculate percentages for each gender
        gender_totals = df_display.groupby('sex').size().reset_index(name='total')
        gender_disease = gender_disease.merge(gender_totals, on='sex')
        gender_disease['percentage'] = (gender_disease['count'] / gender_disease['total'] * 100).round(1)
        
        # Create bar chart with themed colors
        fig = px.bar(gender_disease, x='sex', y='count', color='heart_disease_label',
                    title='Heart Disease Distribution by Gender',
                    labels={'heart_disease_label': 'Heart Disease', 'count': 'Number of Patients'},
                    color_discrete_map=HEART_DISEASE_COLORS,
                    text='percentage')
        
        # Add percentage labels inside bars
        fig.update_traces(texttemplate='%{text}%', textposition='inside')
        fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def create_clinical_analysis(df):
    """Create clinical parameters analysis"""
    st.markdown('<div class="section-header">🏥 Clinical Parameters Analysis</div>', unsafe_allow_html=True)

    # Add display columns for proper color mapping
    df_display = add_display_columns(df)
    
    # First row - Chest Pain and Cholesterol Box Plot
    col1, col2 = st.columns(2)
    
    with col1:
        # Chest pain analysis with varied colors
        cp_disease = df_display.groupby(['cp', 'heart_disease_label']).size().reset_index(name='count')
        
        # Calculate percentages for each chest pain type
        cp_totals = df_display.groupby('cp').size().reset_index(name='total')
        cp_disease = cp_disease.merge(cp_totals, on='cp')
        cp_disease['percentage'] = (cp_disease['count'] / cp_disease['total'] * 100).round(1)
        
        fig = px.bar(cp_disease, x='cp', y='count', color='heart_disease_label',
                    title='Heart Disease Distribution by Chest Pain Type',
                    labels={'cp': 'Chest Pain Type', 'count': 'Number of Patients', 'heart_disease_label': 'Heart Disease'},
                    color_discrete_map=HEART_DISEASE_COLORS,
                    text='percentage')
        
        # Add percentage labels inside bars
        fig.update_traces(texttemplate='%{text}%', textposition='inside')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cholesterol categories by heart disease with purple theme
        chol_disease = df_display.groupby(['chol_category', 'heart_disease_label']).size().reset_index(name='count')
        
        # Calculate percentages for each cholesterol category
        chol_totals = df_display.groupby('chol_category').size().reset_index(name='total')
        chol_disease = chol_disease.merge(chol_totals, on='chol_category')
        chol_disease['percentage'] = (chol_disease['count'] / chol_disease['total'] * 100).round(1)
        
        fig = px.bar(chol_disease, x='chol_category', y='count', color='heart_disease_label',
                    title='Heart Disease Distribution by Cholesterol Category',
                    labels={'chol_category': 'Cholesterol Category', 'count': 'Number of Patients', 'heart_disease_label': 'Heart Disease'},
                    color_discrete_map=HEART_DISEASE_COLORS,
                    text='percentage')
        
        # Add percentage labels inside bars
        fig.update_traces(texttemplate='%{text}%', textposition='inside')
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def create_risk_factors_analysis(df):
    """Analyze risk factors correlation"""
    st.markdown('<div class="section-header">⚠️ Risk Factors Analysis</div>', unsafe_allow_html=True)
    
    # Add display columns for proper color mapping
    df_display = add_display_columns(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk factors by categories with gradient colors
        risk_data = []
        
        # Calculate risk by cholesterol category
        if 'chol_category' in df.columns:
            chol_risk = df.groupby('chol_category')['has_heart_disease'].mean() * 100
            for cat, risk in chol_risk.items():
                risk_data.append({'Category': f'Cholesterol: {cat}', 'Risk': risk})
        
        # Calculate risk by BP category
        if 'bp_category' in df.columns:
            bp_risk = df.groupby('bp_category')['has_heart_disease'].mean() * 100
            for cat, risk in bp_risk.items():
                risk_data.append({'Category': f'BP: {cat}', 'Risk': risk})
        
        # Calculate risk by other factors (using original column for computation)
        fbs_risk = df.groupby('fbs')['has_heart_disease'].mean() * 100
        for fbs_val, risk in fbs_risk.items():
            risk_data.append({'Category': f'Fasting Blood Sugar: {fbs_val}', 'Risk': risk})
        
        risk_df = pd.DataFrame(risk_data)
        risk_df['Risk_Text'] = risk_df['Risk'].round(1)
        
        # Use a medical-themed color scale
        fig = px.bar(risk_df, x='Risk', y='Category', orientation='h',
                    title='Heart Disease Risk by Categories (%)',
                    color='Risk', 
                    color_continuous_scale=[[0, MEDICAL_COLORS['success']], 
                                          [0.5, MEDICAL_COLORS['warning']], 
                                          [1, MEDICAL_COLORS['primary']]],
                    text='Risk_Text')
        
        # Add percentage labels inside bars
        fig.update_traces(texttemplate='%{text}%', textposition='inside')
        fig.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Exercise-induced angina with teal colors
        exang_disease = df_display.groupby(['exang_label', 'heart_disease_label']).size().reset_index(name='count')
        
        # Calculate percentages for exercise-induced angina
        exang_totals = df_display.groupby('exang_label').size().reset_index(name='total')
        exang_disease = exang_disease.merge(exang_totals, on='exang_label')
        exang_disease['percentage'] = (exang_disease['count'] / exang_disease['total'] * 100).round(1)
        
        # Define colors for exercise-induced angina
        exang_colors = {'No': MEDICAL_COLORS['light_green'], 'Yes': MEDICAL_COLORS['navy']}
        
        fig = px.bar(exang_disease, x='exang_label', y='count', color='heart_disease_label',
                    title='Heart Disease Distribution by Exercise-Induced Angina',
                    labels={'exang_label': 'Exercise-Induced Angina', 'count': 'Number of Patients', 'heart_disease_label': 'Heart Disease'},
                    color_discrete_map=HEART_DISEASE_COLORS,
                    text='percentage')
        
        # Add percentage labels inside bars
        fig.update_traces(texttemplate='%{text}%', textposition='inside')
        fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def create_insights_and_recommendations(df):
    """Generate insights and recommendations"""
    st.markdown('<div class="section-header">💡 Key Insights & Recommendations</div>', unsafe_allow_html=True)
    
    # Calculate key statistics
    heart_disease_rate = (df['has_heart_disease'].sum() / len(df)) * 100
    
    # Calculate gender-specific rates
    male_df = df[df['sex'] == 'Male']
    female_df = df[df['sex'] == 'Female']
    
    male_disease_rate = (male_df['has_heart_disease'].sum() / len(male_df)) * 100 if len(male_df) > 0 else 0
    female_disease_rate = (female_df['has_heart_disease'].sum() / len(female_df)) * 100 if len(female_df) > 0 else 0
    
    # Age analysis
    avg_age_disease = df[df['has_heart_disease'] == 1]['age'].mean()
    avg_age_no_disease = df[df['has_heart_disease'] == 0]['age'].mean()
    
    # Chest pain analysis
    cp_risk = df.groupby('cp')['has_heart_disease'].mean() * 100
    highest_risk_cp = cp_risk.idxmax()
    highest_risk_cp_rate = cp_risk.max()
    

    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("**🔍 Key Findings:**")
    st.markdown(f"""
    - **Overall Risk**: {heart_disease_rate:.1f}% of patients have heart disease
    - **Gender Disparity**: Males have {male_disease_rate:.1f}% risk vs females {female_disease_rate:.1f}%
    - **Age Factor**: Patients with heart disease are on average {avg_age_disease - avg_age_no_disease:.1f} years older
    - **Highest Risk**: {highest_risk_cp} chest pain type has {highest_risk_cp_rate:.1f}% risk
    - **Exercise Response**: Exercise-induced angina is a significant risk factor
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Clear session state to logout"""
    st.session_state["password_correct"] = False
    st.rerun()

def main():
    # Check if user is authenticated
    if not check_password():
        return
    
    # Add logout button in sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("🔐 Logout", key="logout_btn"):
            logout()
    
    st.markdown('''
        <div class="main-header">
            <span style="color:white;">MSBA 382 Project</span><br>🫀 Heart Disease Analysis Dashboard
        </div>
    ''', unsafe_allow_html=True)

    
    # Load data
    try:
        df = load_data()
        
        # Sidebar with filters
        st.sidebar.title("🔧 Filters")
        # Filters
        age_range = st.sidebar.slider("Age Range", int(df['age'].min()), int(df['age'].max()), 
                                     (int(df['age'].min()), int(df['age'].max())))
        selected_gender = st.sidebar.selectbox("Gender", ['All'] + list(df['sex'].unique()))
        selected_dataset = st.sidebar.selectbox("Dataset", ['All'] + list(df['dataset'].unique()))
        
        # Apply filters
        filtered_df = df[(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])]
        if selected_gender != 'All':
            filtered_df = filtered_df[filtered_df['sex'] == selected_gender]
        if selected_dataset != 'All':
            filtered_df = filtered_df[filtered_df['dataset'] == selected_dataset]
        
        if len(filtered_df) != len(df):
            st.sidebar.info(f"Showing {len(filtered_df)} records")
        
        # Main dashboard sections
        create_overview_metrics(filtered_df)
        create_demographic_analysis(filtered_df)
        create_clinical_analysis(filtered_df)
        create_risk_factors_analysis(filtered_df)
        create_insights_and_recommendations(filtered_df)
        
    except FileNotFoundError:
        st.error("❌ Error: Could not find 'heart_disease_uci.csv' file. Please ensure the file is in the correct location.")
        st.info("💡 To use this dashboard:")
        st.markdown("""
        1. Download the Heart Disease UCI dataset
        2. Save it as 'heart_disease_uci.csv' in the same directory as this script
        3. Restart the Streamlit application
        """)
    
    except Exception as e:
        st.error(f"❌ An error occurred while loading the data: {str(e)}")
        st.info("Please check your data file format and try again.")

if __name__ == "__main__":
    main()