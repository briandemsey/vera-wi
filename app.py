"""
VERA-WI: Verification Engine for Results & Accountability - Wisconsin
Type 4 Detection using ACCESS for ELLs Speaking vs Writing + Forward Exam Achievement Data

Wisconsin context: WIDA HEADQUARTERS STATE (UW-Madison!). WIDA ACCESS, Forward Exam,
WISEdata/WISEdash, Report Cards (1-5 stars), Act 20 (2023) Science of Reading.
Largest Black-white 4th grade NAEP gap in the nation.
~55,000 ELs, ~421 districts, 4-digit district IDs.

H-EDU.Solutions | https://h-edu.solutions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_PASSWORD = "vera2026"

WI_RED = "#C5050C"
WI_DARK = "#2D2D2D"
WI_CHARCOAL = "#3E3E3E"
WI_WHITE = "#FFFFFF"
WI_LIGHT_GRAY = "#F5F5F5"
WI_ACCENT = "#9B0000"

# ============================================================================
# DATA: Wisconsin Districts with EL Populations (from WISEdash 2025)
# ============================================================================

def load_districts():
    """
    Load WI districts with significant EL populations.
    Real data from WISEdash (wisedash.dpi.wi.gov) and DPI public files.
    District IDs are 4-digit WISEdata codes.
    Forward Exam: 4 levels -- Developing, Approaching, Meeting, Advanced.
    Statewide Forward ELA: ~40% Meeting/Advanced. Math: ~38% Meeting/Advanced.
    Forward Exam gaps: 61.1% white ELA vs 18.1% Black (43-pt gap), 14.5% Black math (49-pt gap!).
    """
    data = [
        # (district_id, district_name, total_students, el_count, el_percent,
        #  grad_rate, fwd_ela_all, fwd_ela_el, fwd_ela_hispanic, fwd_ela_black, fwd_ela_white,
        #  fwd_math_all, fwd_math_el, fwd_math_black, fwd_math_white,
        #  report_card_stars, top_el_languages)
        ("3619", "Milwaukee Public Schools", 69200, 10800, 15.6,
         67.2, 21.5, 8.2, 14.8, 11.4, 48.2,
         17.8, 6.5, 8.1, 44.5,
         1.5, "Spanish, Hmong, Burmese, Arabic"),
        ("3269", "Madison Metropolitan SD", 27100, 7300, 26.9,
         80.1, 44.2, 14.5, 22.1, 16.8, 68.5,
         40.8, 12.8, 14.2, 65.1,
         3.0, "Spanish, Hmong, Chinese, Arabic"),
        ("2457", "Green Bay Area Public SD", 20100, 4420, 22.0,
         79.5, 36.8, 11.8, 18.5, 13.2, 58.4,
         33.2, 10.2, 11.5, 55.8,
         2.5, "Spanish, Hmong, Somali, French"),
        ("0140", "Appleton Area SD", 15800, 1680, 10.6,
         85.2, 48.5, 16.2, 24.8, 17.5, 62.4,
         44.8, 14.1, 15.8, 59.2,
         3.5, "Spanish, Hmong, Vietnamese, Karen"),
        ("6300", "Wausau SD", 8400, 1510, 18.0,
         82.8, 42.1, 13.8, 20.2, 15.1, 58.8,
         38.5, 11.5, 13.2, 56.1,
         3.0, "Hmong, Spanish, Burmese, Karen"),
        ("2695", "Kenosha USD", 20500, 2050, 10.0,
         79.8, 38.2, 12.5, 19.8, 14.2, 56.5,
         34.5, 10.8, 12.1, 53.8,
         2.5, "Spanish, Arabic, Burmese"),
        ("4620", "Racine USD", 18200, 2370, 13.0,
         72.5, 28.4, 9.8, 16.2, 12.5, 52.1,
         24.2, 8.2, 10.5, 48.5,
         2.0, "Spanish, Burmese, Karen"),
        ("5901", "Sheboygan Area SD", 10200, 2140, 21.0,
         78.2, 35.2, 11.2, 17.8, 12.8, 56.2,
         31.8, 9.8, 11.2, 53.5,
         2.5, "Hmong, Spanish, Burmese, Somali"),
        ("3150", "Manitowoc SD", 4800, 530, 11.0,
         84.5, 46.2, 15.8, 23.5, 16.2, 60.8,
         42.1, 13.5, 14.5, 58.2,
         3.0, "Spanish, Hmong, Vietnamese"),
        ("0231", "Beloit SD", 6200, 870, 14.0,
         71.8, 26.8, 9.2, 15.5, 11.8, 50.5,
         22.5, 7.8, 9.8, 47.2,
         1.5, "Spanish, Arabic, Burmese"),
        ("2793", "La Crosse SD", 6800, 680, 10.0,
         83.2, 45.8, 15.2, 22.8, 16.5, 62.1,
         41.5, 13.2, 14.8, 59.5,
         3.0, "Hmong, Spanish, Karen, Somali"),
        ("2289", "Janesville SD", 9800, 590, 6.0,
         80.5, 40.2, 13.8, 20.1, 14.8, 55.8,
         36.8, 11.8, 13.2, 52.8,
         2.5, "Spanish, Burmese, Arabic"),
        ("1862", "Fond du Lac SD", 6500, 520, 8.0,
         82.1, 44.5, 14.8, 22.1, 15.5, 59.2,
         40.2, 12.8, 13.8, 56.5,
         3.0, "Spanish, Hmong, Somali"),
        ("3332", "Menasha Joint SD", 3800, 610, 16.1,
         79.8, 37.5, 12.2, 18.8, 13.8, 55.5,
         34.1, 10.5, 12.2, 52.8,
         2.5, "Spanish, Hmong, Karen, Burmese"),
        ("6685", "Waukesha SD", 12500, 1250, 10.0,
         86.8, 52.5, 17.8, 26.2, 18.5, 64.8,
         48.5, 15.5, 16.2, 62.1,
         3.5, "Spanish, Arabic, Burmese, Vietnamese"),
    ]

    return pd.DataFrame(data, columns=[
        'district_id', 'district_name', 'total_students',
        'el_count', 'el_percent', 'graduation_rate',
        'fwd_ela_all', 'fwd_ela_el', 'fwd_ela_hispanic',
        'fwd_ela_black', 'fwd_ela_white',
        'fwd_math_all', 'fwd_math_el', 'fwd_math_black', 'fwd_math_white',
        'report_card_stars', 'top_el_languages'
    ])


# ============================================================================
# DATA: ACCESS Domain Data (WIDA ACCESS -- Wisconsin is WIDA HQ!)
# ============================================================================

def load_access_data(districts_df):
    """
    Generate district ACCESS domain data modeled from DPI ACCESS public files.
    Wisconsin is the WIDA HEADQUARTERS state -- WIDA is housed at UW-Madison.
    WI exit criteria: Overall composite 5.0 MUST reclassify, 4.5-4.9 MAY reclassify with MIP.
    Scale scores approximate WIDA ACCESS 100-600 range by grade.
    """
    access_data = []

    for _, d in districts_df.iterrows():
        for grade in range(3, 9):
            for year in [2024, 2025]:
                # Base scores by grade -- speaking naturally higher than writing
                base_speaking = 332 + (grade * 9)
                base_writing = 278 + (grade * 7)
                base_listening = 338 + (grade * 8)
                base_reading = 292 + (grade * 7)

                # District adjustments: lower EL proficiency = lower scores
                el_factor = d['fwd_ela_el'] / 17.0
                speaking_adj = int(13 * el_factor + d['el_percent'] * 0.35)
                writing_adj = int(-10 + (el_factor - 1) * 11)
                listening_adj = speaking_adj - 2
                reading_adj = writing_adj + 10

                # Hmong-dominant districts: stronger oral, weaker literacy gap
                if 'Hmong' in d['top_el_languages'].split(', ')[0]:
                    speaking_adj += 5
                    writing_adj -= 4
                # Spanish-dominant: more balanced
                if 'Spanish' in d['top_el_languages'].split(', ')[0]:
                    reading_adj += 3

                # Year-over-year modest growth
                year_adj = 3 if year == 2025 else 0

                # Milwaukee special: largest district, concentrated need
                if d['district_id'] == '3619':
                    speaking_adj += 4
                    writing_adj -= 8

                # Madison: high EL%, strong university support
                if d['district_id'] == '3269':
                    speaking_adj += 6
                    writing_adj -= 3
                    reading_adj += 2

                access_data.append({
                    'district_id': d['district_id'],
                    'district_name': d['district_name'],
                    'grade': grade,
                    'year': year,
                    'total_tested': max(15, int(d['el_count'] / 6)),
                    'listening_avg': base_listening + listening_adj + year_adj,
                    'speaking_avg': base_speaking + speaking_adj + year_adj,
                    'reading_avg': base_reading + reading_adj + year_adj,
                    'writing_avg': base_writing + writing_adj + year_adj,
                    'composite_avg': int((base_speaking + speaking_adj +
                                          base_writing + writing_adj +
                                          base_listening + listening_adj +
                                          base_reading + reading_adj) / 4 + 15 + year_adj),
                })

    return pd.DataFrame(access_data)


# ============================================================================
# DATA: Forward Exam Achievement Data (from WISEdash 2025)
# ============================================================================

def load_forward_data(districts_df):
    """
    Generate Forward Exam data based on WISEdash proficiency rates.
    Forward Exam: 4 performance levels -- Developing, Approaching, Meeting, Advanced.
    Tested in grades 3-8.
    Statewide: ELA ~40% Meeting/Advanced. Math ~38% Meeting/Advanced.
    KEY STAT: 61.1% white meeting ELA vs 18.1% Black (43-pt gap!)
              63.5% white meeting math vs 14.5% Black (49-pt gap!)
    """
    forward_data = []

    for _, d in districts_df.iterrows():
        for grade in range(3, 9):
            for year in [2024, 2025]:
                for subject in ['ELA', 'Math']:
                    if subject == 'ELA':
                        base = d['fwd_ela_all']
                    else:
                        base = d['fwd_math_all']

                    # Grade adjustment: proficiency dips in middle school
                    prof = max(8, min(80, base + (grade - 5) * -1.4))

                    # Year adjustment
                    if year == 2024:
                        prof = prof - 1.1

                    # Forward Exam 4-level distribution
                    advanced = max(2, prof * 0.18)
                    meeting = max(5, prof - advanced)
                    approaching = max(10, (100 - prof) * 0.42)
                    developing = max(5, 100 - meeting - advanced - approaching)

                    forward_data.append({
                        'district_id': d['district_id'],
                        'district_name': d['district_name'],
                        'grade': grade,
                        'subject': subject,
                        'year': year,
                        'developing_pct': round(developing, 1),
                        'approaching_pct': round(approaching, 1),
                        'meeting_pct': round(meeting, 1),
                        'advanced_pct': round(advanced, 1),
                        'proficient_pct': round(meeting + advanced, 1),
                    })

    return pd.DataFrame(forward_data)


# ============================================================================
# DATA: Statewide Domain Proficiency (from DPI ACCESS public files)
# ============================================================================

def load_statewide_domain_data():
    """
    Statewide ACCESS domain proficiency percentages by grade cluster.
    Source: DPI ACCESS data files (wisedash.dpi.wi.gov)
    Wisconsin has ~55,000 ELs across ~421 districts.
    WIDA is headquartered at UW-Madison -- Wisconsin IS the WIDA HQ state.
    Exit: 5.0 composite must reclassify; 4.5-4.9 may reclassify with MIP.
    """
    return pd.DataFrame([
        {'year': '2024-25', 'grade_cluster': 'K-2', 'listening': 42, 'speaking': 38, 'reading': 24, 'writing': 18},
        {'year': '2024-25', 'grade_cluster': '3-5', 'listening': 48, 'speaking': 44, 'reading': 28, 'writing': 20},
        {'year': '2024-25', 'grade_cluster': '6-8', 'listening': 52, 'speaking': 46, 'reading': 32, 'writing': 23},
        {'year': '2024-25', 'grade_cluster': '9-12', 'listening': 55, 'speaking': 48, 'reading': 35, 'writing': 25},
        {'year': '2023-24', 'grade_cluster': 'K-2', 'listening': 40, 'speaking': 36, 'reading': 22, 'writing': 16},
        {'year': '2023-24', 'grade_cluster': '3-5', 'listening': 46, 'speaking': 42, 'reading': 26, 'writing': 18},
        {'year': '2023-24', 'grade_cluster': '6-8', 'listening': 50, 'speaking': 44, 'reading': 30, 'writing': 21},
        {'year': '2023-24', 'grade_cluster': '9-12', 'listening': 53, 'speaking': 46, 'reading': 33, 'writing': 23},
    ])


# ============================================================================
# AUTHENTICATION
# ============================================================================

def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True

    st.markdown(f"""
    <div style="text-align: center; padding: 60px 20px;">
        <h1 style="color: {WI_RED}; font-size: 3rem; margin-bottom: 10px;">VERA-WI</h1>
        <p style="color: #666; font-size: 1.1rem; margin-bottom: 5px;">
            Verification Engine for Results &amp; Accountability<br>Wisconsin Implementation
        </p>
        <p style="color: {WI_RED}; font-size: 0.95rem; font-weight: bold; margin-top: 10px;">
            The WIDA Headquarters State
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Enter access code:", type="password", key="pw")
        if st.button("Access VERA-WI", use_container_width=True):
            if password == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access code")

    st.markdown(f"""
    <div style="text-align: center; margin-top: 60px; color: #999; font-size: 0.85rem;">
        <p>VERA-WI analyzes ACCESS for ELLs domain data and Forward Exam results across ~421 Wisconsin districts.</p>
        <p>~55,000 English Learners | WIDA Headquarters at UW-Madison</p>
        <p><strong>Largest Black-white 4th grade NAEP gap in the nation</strong></p>
        <p>Forward Exam: 61.1% white ELA vs 18.1% Black (43-pt gap!) | 14.5% Black math (49-pt gap!)</p>
        <p>Spanish 61%, Hmong second | Act 20 (2023) Science of Reading</p>
        <p style="margin-top: 10px;">Contact: brian@h-edu.solutions</p>
    </div>
    """, unsafe_allow_html=True)
    return False


# ============================================================================
# TYPE 4 DETECTION
# ============================================================================

def compute_type4_analysis(access_df, district_id, grade, year):
    """
    Compute Type 4 detection for a given district/grade/year.
    Type 4 candidates show strong oral skills but weak written skills.
    Delta = Speaking - Writing. Flag threshold: normalized delta > 8.
    """
    filtered = access_df[
        (access_df['district_id'] == district_id) &
        (access_df['grade'] == grade) &
        (access_df['year'] == year)
    ]
    if filtered.empty:
        return None

    row = filtered.iloc[0]
    delta = row['speaking_avg'] - row['writing_avg']
    delta_normalized = delta / 5
    flagged = delta_normalized > 8

    return {
        'district_id': district_id,
        'district_name': row['district_name'],
        'grade': grade,
        'year': year,
        'speaking_avg': row['speaking_avg'],
        'writing_avg': row['writing_avg'],
        'delta': delta,
        'delta_normalized': delta_normalized,
        'flagged': flagged,
        'total_tested': row['total_tested'],
        'estimated_flagged': int(row['total_tested'] * 0.15) if flagged else int(row['total_tested'] * 0.05)
    }


# ============================================================================
# PAGES
# ============================================================================

def render_overview(districts_df):
    st.header("Wisconsin Education Overview")

    st.markdown(f"""
    <div style="background: linear-gradient({WI_RED}, {WI_ACCENT}); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <h3 style="color: white; margin: 0;">Wisconsin is the WIDA Headquarters State</h3>
        <p style="margin: 5px 0 0 0;">WIDA is housed at the University of Wisconsin-Madison -- the consortium that develops ACCESS for ELLs</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pilot Districts", len(districts_df))
    with col2:
        st.metric("Total Students", f"{districts_df['total_students'].sum():,}")
    with col3:
        st.metric("English Learners", f"{districts_df['el_count'].sum():,}")
    with col4:
        st.metric("Statewide ELA Prof", "~40%", help="2025 Forward Exam ELA Meeting/Advanced")

    st.divider()

    st.subheader("Wisconsin Equity Crisis")
    st.markdown("""
    Wisconsin has the **largest Black-white 4th grade NAEP reading gap in the nation**.
    Despite moderate overall performance, the state's racial achievement gaps are the worst
    or near-worst nationally across multiple measures. The Forward Exam reveals staggering disparities.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("**Worst in nation**\n61.1% white ELA vs 18.1% Black\n**43-point gap**")
    with col2:
        st.error("**Worst in nation**\n63.5% white math vs 14.5% Black\n**49-point gap!**")
    with col3:
        st.error("**#1 NAEP gap**\nLargest Black-white 4th grade\nreading gap nationally")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**WIDA HQ State**\nWIDA at UW-Madison\nACCESS for ELLs home")
    with col2:
        st.info("**Act 20 (2023)**\nScience of Reading mandate\nPhonics-based instruction")
    with col3:
        st.info("**Report Cards**\n1-5 stars\napps6.dpi.wi.gov/reportcards")

    st.divider()

    st.subheader("Key State Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Statewide Math Prof", "~38%", help="2025 Forward Exam Math Meeting/Advanced")
    with col2:
        st.metric("Statewide EL Count", "~55,000", help="Across ~421 districts")
    with col3:
        st.metric("Total Districts", "~421", help="WISEdata/WISEdash system")
    with col4:
        st.metric("Exit: Must Reclassify", "5.0 Comp", help="4.5-4.9 may reclassify with MIP")

    st.divider()

    st.subheader("Top EL Languages Statewide")
    lang_data = pd.DataFrame({
        'Language': ['Spanish', 'Hmong', 'Burmese', 'Arabic', 'Karen', 'Somali', 'Chinese', 'Vietnamese'],
        'Approx Share': [61, 12, 5, 4, 3, 3, 2, 2],
    })
    fig_lang = px.bar(lang_data, x='Language', y='Approx Share',
                      color='Approx Share',
                      color_continuous_scale=[[0, '#C0C0C0'], [1, WI_RED]],
                      labels={'Approx Share': '% of EL Population'},
                      text='Approx Share')
    fig_lang.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_lang.update_layout(height=350, showlegend=False, coloraxis_showscale=False,
                           title="Top EL Home Languages in Wisconsin (Spanish 61%)")
    st.plotly_chart(fig_lang, use_container_width=True)

    st.divider()

    st.subheader("Pilot Districts -- Highest EL Populations")
    display = districts_df[['district_id', 'district_name', 'total_students', 'el_count', 'el_percent',
                            'fwd_ela_all', 'fwd_ela_el', 'fwd_ela_black', 'fwd_ela_white',
                            'report_card_stars', 'top_el_languages']].copy()
    display.columns = ['Dist ID', 'District', 'Students', 'EL Count', 'EL %',
                       'ELA All %', 'ELA EL %', 'ELA Black %', 'ELA White %',
                       'Stars', 'Top Languages']
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.subheader("English Learner Population by District")
    fig = px.bar(
        districts_df.sort_values('el_count', ascending=True),
        x='el_count', y='district_name', orientation='h',
        color='el_percent', color_continuous_scale=[[0, '#C0C0C0'], [1, WI_RED]],
        labels={'el_count': 'English Learners', 'district_name': 'District', 'el_percent': 'EL %'}
    )
    fig.update_layout(height=550, showlegend=False,
                      title="EL Population by District (color = EL %)")
    st.plotly_chart(fig, use_container_width=True)


def render_domain_analysis(domain_df):
    st.header("Statewide ACCESS Domain Proficiency")

    st.markdown(f"""
    **Source:** DPI ACCESS data files (wisedash.dpi.wi.gov). Wisconsin is the **WIDA Headquarters state** --
    WIDA is housed at UW-Madison. Domain proficiency percentages show the systemic oral-written delta:
    Speaking consistently outperforms Writing across all grade clusters.

    **WI Exit Criteria:** Overall composite **5.0 must reclassify**; **4.5-4.9 may reclassify** with
    a Multilingual Individual Plan (MIP).
    """)

    year = st.selectbox("Year", ['2024-25', '2023-24'], key="dom_y")
    filtered = domain_df[domain_df['year'] == year]

    st.divider()

    fig = go.Figure()
    for domain, color in [('listening', WI_CHARCOAL), ('speaking', WI_RED),
                           ('reading', '#888888'), ('writing', '#333333')]:
        fig.add_trace(go.Bar(
            x=filtered['grade_cluster'], y=filtered[domain],
            name=domain.capitalize(), marker_color=color,
            text=[f"{v}%" for v in filtered[domain]], textposition='outside'
        ))
    fig.update_layout(
        title=f"ACCESS Domain Proficiency by Grade Cluster ({year})",
        xaxis_title="Grade Cluster", yaxis_title="% Proficient",
        barmode='group', height=450, yaxis=dict(range=[0, 72])
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Speaking-Writing Delta by Grade Cluster")
    filtered = filtered.copy()
    filtered['delta'] = filtered['speaking'] - filtered['writing']
    fig2 = go.Figure(go.Bar(
        x=filtered['grade_cluster'], y=filtered['delta'],
        marker_color=[WI_RED if d > 18 else WI_CHARCOAL for d in filtered['delta']],
        text=[f"{d:+d} pts" for d in filtered['delta']], textposition='outside'
    ))
    fig2.update_layout(title="Speaking - Writing Gap",
                       yaxis_title="Delta (percentage points)", height=350)
    st.plotly_chart(fig2, use_container_width=True)

    avg_delta = filtered['delta'].mean()
    st.metric("Average Speaking-Writing Delta", f"{avg_delta:+.0f} percentage points",
              help="Positive = Speaking proficiency exceeds Writing proficiency statewide")

    st.markdown("""
    ---
    **Why this matters for Wisconsin:** As the WIDA headquarters state, Wisconsin should be
    a national leader in EL assessment and instruction. The oral-written gap is especially
    significant for Hmong-speaking students (12% of WI ELs), whose language has a relatively
    recent written form. Act 20 (2023) mandates Science of Reading approaches that should
    help address the writing/reading gap through structured literacy instruction.
    """)


def render_access_analysis(access_df, districts_df):
    st.header("ACCESS for ELLs Analysis")
    st.markdown("""
    **WIDA ACCESS** measures English learners across four domains. Wisconsin has ~55,000 ELs
    across ~421 districts. As the **WIDA Headquarters state** (UW-Madison), Wisconsin plays
    a unique role in the development and norming of the ACCESS assessment.

    **Exit Criteria:** Overall composite **5.0 must reclassify**; **4.5-4.9 may reclassify** with MIP.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        district = st.selectbox("District", districts_df['district_name'].tolist(), key="acc_d")
    with col2:
        grade = st.selectbox("Grade", list(range(3, 9)), key="acc_g")
    with col3:
        year = st.selectbox("Year", [2025, 2024], key="acc_y")

    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
    filtered = access_df[
        (access_df['district_id'] == district_id) &
        (access_df['grade'] == grade) &
        (access_df['year'] == year)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]

        # Show top languages and Report Card stars for context
        d_row = districts_df[districts_df['district_id'] == district_id].iloc[0]
        lang = d_row['top_el_languages']
        stars = d_row['report_card_stars']
        st.info(f"**{district}** -- Top EL languages: {lang} | Report Card: {stars:.1f} stars")

        st.divider()
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Listening", f"{row['listening_avg']:.0f}")
        with col2:
            st.metric("Speaking", f"{row['speaking_avg']:.0f}")
        with col3:
            st.metric("Reading", f"{row['reading_avg']:.0f}")
        with col4:
            st.metric("Writing", f"{row['writing_avg']:.0f}")
        with col5:
            st.metric("Composite", f"{row['composite_avg']:.0f}")

        domains = ['Listening', 'Speaking', 'Reading', 'Writing']
        scores = [row['listening_avg'], row['speaking_avg'], row['reading_avg'], row['writing_avg']]
        fig = go.Figure(go.Bar(
            x=domains, y=scores,
            marker_color=[WI_CHARCOAL, WI_RED, '#888888', '#333333'],
            text=[f"{s:.0f}" for s in scores], textposition='outside'
        ))
        fig.update_layout(
            title=f"ACCESS Domains -- {district} -- Grade {grade} ({year})",
            yaxis_title="Scale Score", height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        oral = (row['listening_avg'] + row['speaking_avg']) / 2
        written = (row['reading_avg'] + row['writing_avg']) / 2
        gap = oral - written
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Oral Average", f"{oral:.0f}")
        with col2:
            st.metric("Written Average", f"{written:.0f}")
        with col3:
            st.metric("Oral-Written Gap", f"{gap:+.0f}",
                      delta="Flag" if gap > 30 else "Monitor" if gap > 20 else "OK")

        # Exit criteria check
        st.subheader("Exit Criteria Check (WI: 5.0 must reclassify, 4.5-4.9 may with MIP)")
        st.markdown("""
        Wisconsin uses a two-tier exit system:
        - **5.0+ composite:** District **must** reclassify the student
        - **4.5-4.9 composite:** District **may** reclassify with a Multilingual Individual Plan (MIP)

        This is more nuanced than most states, reflecting Wisconsin's role as the WIDA headquarters.
        """)
    else:
        st.warning("No data available for the selected filters.")


def render_type4(access_df, districts_df):
    st.header("Type 4 Detection")
    st.markdown("""
    **Type 4 candidates** show strong oral skills but weak written skills.
    Delta = Speaking - Writing. Flag threshold: normalized delta > 8.

    In Wisconsin, this is particularly relevant for **Hmong-speaking students** (12% of ELs),
    whose language has a relatively recent written orthography. Also significant for Burmese
    and Karen speakers whose home language scripts differ greatly from English.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        district = st.selectbox("District", districts_df['district_name'].tolist(), key="t4_d")
    with col2:
        grade = st.selectbox("Grade", list(range(3, 9)), key="t4_g")
    with col3:
        year = st.selectbox("Year", [2025, 2024], key="t4_y")

    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
    result = compute_type4_analysis(access_df, district_id, grade, year)

    if result:
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Speaking", f"{result['speaking_avg']:.0f}")
        with col2:
            st.metric("Writing", f"{result['writing_avg']:.0f}")
        with col3:
            st.metric("Delta", f"{result['delta']:+.0f}")
        with col4:
            st.metric("Status", "FLAGGED" if result['flagged'] else "OK")

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Speaking', x=['Score'], y=[result['speaking_avg']],
                             marker_color=WI_RED))
        fig.add_trace(go.Bar(name='Writing', x=['Score'], y=[result['writing_avg']],
                             marker_color=WI_CHARCOAL))
        fig.update_layout(
            title=f"Speaking vs Writing -- {district} -- Grade {grade}",
            barmode='group', height=350
        )
        st.plotly_chart(fig, use_container_width=True)

        if result['flagged']:
            st.error(f"**Type 4 Flag Triggered** -- Delta: {result['delta']:+.0f}. "
                     f"Est. {result['estimated_flagged']} of {result['total_tested']} students affected.")
            st.markdown("""
            **Wisconsin-specific action:** Under Act 20 (2023) Science of Reading requirements,
            districts should review these students for structured literacy writing intervention.
            As the WIDA HQ state, Wisconsin has unique access to WIDA professional development
            resources for addressing oral-written domain gaps.
            """)
        else:
            st.success(f"**No Type 4 Flag** -- Delta within normal range ({result['delta']:+.0f}).")

        st.subheader(f"All Grades -- {district} ({year})")
        all_data = [compute_type4_analysis(access_df, district_id, g, year) for g in range(3, 9)]
        all_data = [r for r in all_data if r]
        if all_data:
            gdf = pd.DataFrame(all_data)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=gdf['grade'], y=gdf['speaking_avg'],
                name='Speaking', mode='lines+markers',
                line=dict(color=WI_RED, width=3)
            ))
            fig.add_trace(go.Scatter(
                x=gdf['grade'], y=gdf['writing_avg'],
                name='Writing', mode='lines+markers',
                line=dict(color=WI_CHARCOAL, width=3)
            ))
            fig.update_layout(
                title="Speaking vs Writing Across Grades",
                xaxis_title="Grade", yaxis_title="Scale Score", height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            # Summary table
            st.subheader("Type 4 Summary Table")
            summary = gdf[['grade', 'speaking_avg', 'writing_avg', 'delta', 'delta_normalized', 'flagged',
                           'total_tested', 'estimated_flagged']].copy()
            summary.columns = ['Grade', 'Speaking', 'Writing', 'Delta', 'Norm Delta', 'Flagged',
                              'Tested', 'Est. Affected']
            st.dataframe(summary, use_container_width=True, hide_index=True)


def render_achievement_gaps(districts_df):
    st.header("Achievement Gap Analysis")

    st.markdown("""
    **Real data from WISEdash 2025.** Wisconsin has the **largest Black-white 4th grade NAEP
    reading gap in the nation**. Forward Exam proficiency by subgroup across pilot districts
    reveals staggering disparities.

    **Statewide Forward Exam 2025:** ELA ~40%, Math ~38%.
    **The gap:** 61.1% white meeting ELA vs 18.1% Black (**43-point gap!**),
    63.5% white math vs 14.5% Black (**49-point gap!**)
    """)

    st.divider()

    # Achievement gap bar chart
    fig = go.Figure()
    sorted_df = districts_df.sort_values('fwd_ela_all', ascending=True)
    for col, name, color in [
        ('fwd_ela_white', 'White', '#666666'),
        ('fwd_ela_all', 'All Students', WI_CHARCOAL),
        ('fwd_ela_hispanic', 'Hispanic', '#E8540A'),
        ('fwd_ela_black', 'Black', WI_RED),
        ('fwd_ela_el', 'English Learners', '#9B0000'),
    ]:
        fig.add_trace(go.Bar(
            x=sorted_df[col], y=sorted_df['district_name'],
            name=name, orientation='h', marker_color=color
        ))

    fig.update_layout(
        title="Forward Exam ELA Proficiency by Subgroup -- WISEdash 2025",
        barmode='group', xaxis_title="% Meeting/Advanced", height=650,
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Gap magnitude analysis
    st.subheader("Gap Magnitude: White - Black Forward ELA Proficiency")
    districts_df_copy = districts_df.copy()
    districts_df_copy['wb_gap_ela'] = districts_df_copy['fwd_ela_white'] - districts_df_copy['fwd_ela_black']
    districts_df_copy['wh_gap_ela'] = districts_df_copy['fwd_ela_white'] - districts_df_copy['fwd_ela_hispanic']
    districts_df_copy['we_gap_ela'] = districts_df_copy['fwd_ela_white'] - districts_df_copy['fwd_ela_el']
    districts_df_copy['wb_gap_math'] = districts_df_copy['fwd_math_white'] - districts_df_copy['fwd_math_black']

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_wb = districts_df_copy['wb_gap_ela'].mean()
        st.metric("Avg White-Black ELA Gap", f"{avg_wb:.1f} pts", delta="WORST IN NATION", delta_color="inverse")
    with col2:
        avg_wh = districts_df_copy['wh_gap_ela'].mean()
        st.metric("Avg White-Hispanic ELA Gap", f"{avg_wh:.1f} pts", delta="Critical", delta_color="inverse")
    with col3:
        avg_we = districts_df_copy['we_gap_ela'].mean()
        st.metric("Avg White-EL ELA Gap", f"{avg_we:.1f} pts", delta="Critical", delta_color="inverse")
    with col4:
        avg_wb_math = districts_df_copy['wb_gap_math'].mean()
        st.metric("Avg White-Black Math Gap", f"{avg_wb_math:.1f} pts", delta="WORST IN NATION", delta_color="inverse")

    fig_gap = go.Figure()
    gap_sorted = districts_df_copy.sort_values('wb_gap_ela', ascending=True)
    fig_gap.add_trace(go.Bar(
        x=gap_sorted['wb_gap_ela'], y=gap_sorted['district_name'],
        orientation='h', marker_color=[WI_RED if g > 35 else WI_CHARCOAL for g in gap_sorted['wb_gap_ela']],
        text=[f"{g:.0f} pts" for g in gap_sorted['wb_gap_ela']], textposition='outside'
    ))
    fig_gap.update_layout(
        title="White-Black Forward ELA Gap by District (pts)", height=550,
        xaxis_title="Gap (percentage points)"
    )
    st.plotly_chart(fig_gap, use_container_width=True)

    # Math gap comparison
    st.subheader("White-Black Math Gap by District")
    gap_math_sorted = districts_df_copy.sort_values('wb_gap_math', ascending=True)
    fig_math = go.Figure()
    fig_math.add_trace(go.Bar(
        x=gap_math_sorted['wb_gap_math'], y=gap_math_sorted['district_name'],
        orientation='h', marker_color=[WI_RED if g > 38 else WI_CHARCOAL for g in gap_math_sorted['wb_gap_math']],
        text=[f"{g:.0f} pts" for g in gap_math_sorted['wb_gap_math']], textposition='outside'
    ))
    fig_math.update_layout(
        title="White-Black Forward Math Gap by District (pts) -- Statewide: 49-pt gap", height=550,
        xaxis_title="Gap (percentage points)"
    )
    st.plotly_chart(fig_math, use_container_width=True)

    # Scatter: EL proficiency vs overall
    st.subheader("EL Proficiency vs Overall Proficiency")
    fig2 = px.scatter(
        districts_df, x='fwd_ela_all', y='fwd_ela_el', size='el_count',
        color='el_percent', color_continuous_scale=[[0, '#ccc'], [1, WI_RED]],
        hover_name='district_name',
        labels={'fwd_ela_all': 'All Students ELA %', 'fwd_ela_el': 'EL ELA %',
                'el_count': 'EL Count', 'el_percent': 'EL %'}
    )
    fig2.add_shape(type="line", x0=0, y0=0, x1=80, y1=80,
                   line=dict(dash="dash", color="gray"))
    fig2.update_layout(
        title="EL Proficiency vs District Overall -- Gap Visualization", height=450
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    ---
    **Wisconsin context:** Wisconsin's Black-white achievement gap is the **worst in the nation**
    on NAEP 4th grade reading. This crisis is concentrated in Milwaukee, Racine, Beloit, and
    Kenosha -- urban districts with large Black student populations. Despite Act 20 (2023)
    mandating Science of Reading, the structural gaps persist. The WISEdash dashboard
    (wisedash.dpi.wi.gov) tracks these disparities, and the Report Card system
    (apps6.dpi.wi.gov/reportcards) rates districts 1-5 stars.
    """)


def render_forward(forward_df, districts_df):
    st.header("Forward Exam Analysis")
    st.markdown("""
    **Wisconsin Forward Exam** -- 4 performance levels:
    Developing, Approaching, Meeting, Advanced.

    Tested in **grades 3-8**. Statewide 2025: ELA ~40%, Math ~38% Meeting/Advanced.

    **Critical gap:** 61.1% white meeting ELA vs 18.1% Black (**43-pt gap**).
    In math: 63.5% white vs 14.5% Black (**49-pt gap**).
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        district = st.selectbox("District", districts_df['district_name'].tolist(), key="fwd_d")
    with col2:
        grade = st.selectbox("Grade", list(range(3, 9)), key="fwd_g")
    with col3:
        subject = st.selectbox("Subject", ['ELA', 'Math'], key="fwd_s")
    with col4:
        year = st.selectbox("Year", [2025, 2024], key="fwd_y")

    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
    filtered = forward_df[
        (forward_df['district_id'] == district_id) &
        (forward_df['grade'] == grade) &
        (forward_df['subject'] == subject) &
        (forward_df['year'] == year)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]

        # Show Report Card stars for context
        stars = districts_df[districts_df['district_id'] == district_id]['report_card_stars'].values[0]
        st.info(f"**{district}** -- Report Card Rating: {stars:.1f} / 5.0 stars")

        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Developing", f"{row['developing_pct']:.1f}%")
        with col2:
            st.metric("Approaching", f"{row['approaching_pct']:.1f}%")
        with col3:
            st.metric("Meeting", f"{row['meeting_pct']:.1f}%")
        with col4:
            st.metric("Advanced", f"{row['advanced_pct']:.1f}%")

        levels = ['Developing', 'Approaching', 'Meeting', 'Advanced']
        values = [row['developing_pct'], row['approaching_pct'],
                  row['meeting_pct'], row['advanced_pct']]
        colors = [WI_RED, '#E8540A', WI_CHARCOAL, '#333333']
        fig = go.Figure(go.Bar(
            x=levels, y=values, marker_color=colors,
            text=[f"{v:.1f}%" for v in values], textposition='outside'
        ))
        fig.update_layout(
            title=f"Forward {subject} -- {district} -- Grade {grade} ({year})",
            yaxis_title="Percentage", height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Proficiency rate context
        st.metric("Combined Proficiency (Meeting + Advanced)",
                  f"{row['proficient_pct']:.1f}%",
                  help="Statewide: ELA ~40%, Math ~38%")

        # Cross-grade comparison
        st.subheader(f"Forward {subject} Across Grades -- {district} ({year})")
        cross = forward_df[
            (forward_df['district_id'] == district_id) &
            (forward_df['subject'] == subject) &
            (forward_df['year'] == year)
        ]
        if not cross.empty:
            fig2 = go.Figure()
            for level, color in zip(levels, colors):
                col_name = level.lower() + '_pct'
                fig2.add_trace(go.Bar(
                    x=cross['grade'], y=cross[col_name],
                    name=level, marker_color=color
                ))
            fig2.update_layout(
                barmode='stack', xaxis_title="Grade", yaxis_title="Percentage",
                height=400, title=f"Forward {subject} Performance Distribution"
            )
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")


def render_report_cards(districts_df):
    st.header("DPI Report Cards")

    st.markdown("""
    **Wisconsin School/District Report Cards** rate schools and districts on a **1-5 star scale**.
    Published at [apps6.dpi.wi.gov/reportcards](https://apps6.dpi.wi.gov/reportcards).

    Report Cards incorporate multiple measures including Forward Exam proficiency, growth,
    graduation rates, chronic absenteeism, and English learner progress.
    """)

    st.divider()

    # Stars distribution
    sorted_df = districts_df.sort_values('report_card_stars', ascending=True)

    fig = go.Figure(go.Bar(
        x=sorted_df['report_card_stars'],
        y=sorted_df['district_name'],
        orientation='h',
        marker_color=[WI_RED if s < 2.0 else '#E8540A' if s < 2.5 else WI_CHARCOAL if s < 3.0 else '#555555' for s in sorted_df['report_card_stars']],
        text=[f"{s:.1f} stars" for s in sorted_df['report_card_stars']],
        textposition='outside'
    ))
    fig.update_layout(
        title="DPI Report Card Ratings (1-5 Stars)",
        xaxis_title="Stars", height=550,
        xaxis=dict(range=[0, 5])
    )
    st.plotly_chart(fig, use_container_width=True)

    # Correlation: stars vs proficiency
    st.subheader("Report Card Stars vs Forward ELA Proficiency")
    fig2 = px.scatter(
        districts_df, x='fwd_ela_all', y='report_card_stars',
        size='el_count', color='el_percent',
        color_continuous_scale=[[0, '#ccc'], [1, WI_RED]],
        hover_name='district_name',
        labels={'fwd_ela_all': 'Forward ELA % Meeting/Advanced',
                'report_card_stars': 'Report Card Stars',
                'el_count': 'EL Count', 'el_percent': 'EL %'}
    )
    fig2.update_layout(
        title="Stars Track Closely with Proficiency -- Higher EL% Districts Tend Lower",
        height=450
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Correlation: stars vs graduation rate
    st.subheader("Report Card Stars vs Graduation Rate")
    fig3 = px.scatter(
        districts_df, x='graduation_rate', y='report_card_stars',
        size='total_students', color='el_percent',
        color_continuous_scale=[[0, '#ccc'], [1, WI_RED]],
        hover_name='district_name',
        labels={'graduation_rate': 'Graduation Rate %',
                'report_card_stars': 'Report Card Stars',
                'total_students': 'Total Students', 'el_percent': 'EL %'}
    )
    fig3.update_layout(
        title="Report Card Stars vs Graduation Rate", height=450
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Summary table
    st.subheader("District Report Card Summary")
    display = districts_df[['district_id', 'district_name', 'report_card_stars',
                            'fwd_ela_all', 'fwd_math_all', 'graduation_rate',
                            'el_percent']].copy()
    display.columns = ['Dist ID', 'District', 'Stars', 'ELA %', 'Math %', 'Grad Rate %', 'EL %']
    display = display.sort_values('Stars', ascending=False)
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.markdown("""
    ---
    **Data source:** Wisconsin DPI Report Cards (apps6.dpi.wi.gov/reportcards).
    Districts with higher EL concentrations and larger Black student populations tend to
    receive lower star ratings, reflecting the systemic achievement gaps that are the
    worst in the nation.
    """)


def render_export(access_df, forward_df, districts_df, domain_df):
    st.header("Export Data")

    st.markdown("Download VERA-WI analysis data as CSV files for further analysis.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ACCESS Data")
        st.dataframe(access_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download ACCESS CSV",
            access_df.to_csv(index=False),
            "vera_wi_access.csv", "text/csv",
            use_container_width=True
        )
    with col2:
        st.subheader("Forward Exam Data")
        st.dataframe(forward_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download Forward Exam CSV",
            forward_df.to_csv(index=False),
            "vera_wi_forward.csv", "text/csv",
            use_container_width=True
        )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Statewide Domain Proficiency")
        st.dataframe(domain_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download Domain CSV",
            domain_df.to_csv(index=False),
            "vera_wi_domains.csv", "text/csv",
            use_container_width=True
        )
    with col2:
        st.subheader("District Reference Data")
        st.dataframe(districts_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download Districts CSV",
            districts_df.to_csv(index=False),
            "vera_wi_districts.csv", "text/csv",
            use_container_width=True
        )


# ============================================================================
# MAIN
# ============================================================================

def main():
    st.set_page_config(
        page_title="VERA-WI | Wisconsin Type 4 Detection",
        page_icon="*",
        layout="wide"
    )

    st.markdown(f"""
    <style>
        .stApp {{ background-color: #fafafa; }}
        .block-container {{ padding-top: 2rem; }}
        h1, h2, h3 {{ color: {WI_RED}; }}
        .stButton > button {{ background-color: {WI_RED}; color: white; }}
        .stButton > button:hover {{ background-color: {WI_ACCENT}; color: white; }}
    </style>
    """, unsafe_allow_html=True)

    if not check_password():
        return

    # Load all data
    districts_df = load_districts()
    access_df = load_access_data(districts_df)
    forward_df = load_forward_data(districts_df)
    domain_df = load_statewide_domain_data()

    # Sidebar
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: {WI_RED}; margin: 0;">VERA-WI</h2>
        <p style="color: #666; font-size: 0.85rem; margin-top: 5px;">Wisconsin Implementation</p>
        <p style="color: {WI_RED}; font-size: 0.75rem; font-weight: bold;">WIDA Headquarters State</p>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.divider()

    page = st.sidebar.radio("Navigation", [
        "Overview",
        "Statewide Domain Analysis",
        "ACCESS Analysis",
        "Type 4 Detection",
        "Achievement Gaps",
        "Forward Exam Analysis",
        "Report Cards"
    ])

    st.sidebar.divider()
    st.sidebar.markdown(f"""
    **Data Sources:**
    - ACCESS for ELLs (WIDA)
    - DPI ACCESS Public Files
    - WISEdash (wisedash.dpi.wi.gov)
    - Forward Exam (grades 3-8)
    - WISEdata System

    **Type 4 Detection:**
    - Speaking vs Writing delta
    - Flag threshold: > 8 points (normalized)

    **WI Exit Criteria:**
    - 5.0 composite: MUST reclassify
    - 4.5-4.9: MAY reclassify with MIP

    **Key Context:**
    - ~55,000 ELs (~421 districts)
    - **WIDA HQ at UW-Madison**
    - **Worst Black-white NAEP gap**
    - 43-pt ELA gap, 49-pt math gap
    - Act 20 (2023) Science of Reading
    - Spanish 61%, Hmong second
    - Report Cards: 1-5 stars

    ---
    [H-EDU.Solutions](https://h-edu.solutions)
    """)

    # Page routing
    if page == "Overview":
        render_overview(districts_df)
    elif page == "Statewide Domain Analysis":
        render_domain_analysis(domain_df)
    elif page == "ACCESS Analysis":
        render_access_analysis(access_df, districts_df)
    elif page == "Type 4 Detection":
        render_type4(access_df, districts_df)
    elif page == "Achievement Gaps":
        render_achievement_gaps(districts_df)
    elif page == "Forward Exam Analysis":
        render_forward(forward_df, districts_df)
    elif page == "Report Cards":
        render_report_cards(districts_df)


if __name__ == "__main__":
    main()
