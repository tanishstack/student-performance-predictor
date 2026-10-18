"""Student performance simulation using an exponential gap model."""

import html

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def calculate_scores(
    initial_score: float,
    target_score: float,
    improvement_constant: float,
    days: np.ndarray,
) -> np.ndarray:
    """Return modelled scores for each day using the exponential gap model."""
    if not 0 <= initial_score <= 100:
        raise ValueError("The initial score must be between 0 and 100.")
    if not initial_score <= target_score <= 100:
        raise ValueError("The target score must be at least the initial score and at most 100.")
    if improvement_constant <= 0:
        raise ValueError("The improvement constant k must be positive.")

    study_days = np.asarray(days, dtype=float)
    if np.any(study_days < 0):
        raise ValueError("Study days cannot be negative.")

    remaining_gap = target_score - initial_score
    return target_score - remaining_gap * np.exp(-improvement_constant * study_days)


st.set_page_config(
    page_title="Student Performance Predictor",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #29233f;
        --muted: #726d83;
        --line: #e8e4f1;
        --panel-shadow: 0 12px 30px rgba(41, 28, 77, 0.07);
    }
    .stApp { background: #f6f4fb; color: var(--ink); }
    header[data-testid="stHeader"] { background: rgba(246, 244, 251, 0.92); }
    .main .block-container { max-width: 1280px; padding: 2.2rem 2rem 3rem; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(165deg, #171238 0%, #28205d 54%, #48206f 100%);
    }
    section[data-testid="stSidebar"] > div { background: transparent; }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    section[data-testid="stSidebar"] h2 { color: #f5f2ff; }
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { font-weight: 600; }
    section[data-testid="stSidebar"] [data-baseweb="input"] > div {
        background: #fff;
        border-color: #d9d1ef;
        border-radius: 10px;
    }
    section[data-testid="stSidebar"] [data-baseweb="input"] input {
        color: #29233f !important;
        -webkit-text-fill-color: #29233f;
    }
    section[data-testid="stSidebar"] [data-baseweb="input"] button { color: #514274; }
    .hero-kicker {
        color: #7557c8;
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        margin: 0 0 0.45rem;
    }
    .hero-title {
        color: #21183f;
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.12;
        margin: 0;
    }
    .hero-subtitle { color: var(--muted); font-size: 1.04rem; margin: 0.55rem 0 1.3rem; }
    .quote-banner {
        background: linear-gradient(105deg, #ffffff 0%, #f0eaff 100%);
        border: 1px solid #e6ddfa;
        border-left: 5px solid #7650d8;
        border-radius: 14px;
        box-shadow: 0 8px 22px rgba(54, 35, 103, 0.06);
        margin: 0.7rem 0 1.65rem;
        padding: 1rem 1.25rem;
    }
    .quote-text { color: #392b5e; font-size: 1.02rem; font-style: italic; margin: 0; }
    .quote-credit { color: #776694; font-size: 0.84rem; font-weight: 700; margin: 0.4rem 0 0; }
    .student-summary {
        align-items: center;
        background: #fff;
        border: 1px solid var(--line);
        border-radius: 12px;
        box-shadow: 0 5px 16px rgba(41, 28, 77, 0.04);
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem 1rem;
        margin: 0.55rem 0 1.2rem;
        padding: 0.85rem 1rem;
    }
    .student-label { color: #7a718d; font-size: 0.76rem; font-weight: 800; text-transform: uppercase; }
    .student-name { color: #2d2250; font-size: 1rem; font-weight: 800; }
    .student-plan { color: #716b80; font-size: 0.9rem; }
    .metric-grid {
        display: grid;
        gap: 16px;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        margin: 0.8rem 0 1.55rem;
    }
    .metric-card {
        border-radius: 17px;
        box-shadow: 0 12px 24px rgba(49, 34, 84, 0.16);
        color: #fff;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 144px;
        min-width: 0;
        padding: 1.1rem 1.25rem;
    }
    .metric-purple { background: linear-gradient(135deg, #7955e8 0%, #4435b5 100%); }
    .metric-pink { background: linear-gradient(135deg, #ec62ad 0%, #bd397d 100%); }
    .metric-cyan { background: linear-gradient(135deg, #28c4d5 0%, #356bdd 100%); }
    .metric-emerald { background: linear-gradient(135deg, #24c997 0%, #087b75 100%); }
    .metric-amber { background: linear-gradient(135deg, #ffc45c 0%, #e66d3d 100%); }
    .metric-label { color: rgba(255, 255, 255, 0.88); font-size: 0.88rem; font-weight: 700; }
    .metric-value {
        color: #fff;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.15;
        overflow-wrap: anywhere;
        padding: 0.35rem 0;
    }
    .metric-detail { color: rgba(255, 255, 255, 0.84); font-size: 0.82rem; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #7955e8, #4435b5);
        border-radius: 16px;
        color: #fff;
        padding: 1rem;
    }
    [class*="st-key-model-panel"],
    [class*="st-key-table-panel"],
    [class*="st-key-chart-panel"] {
        background: #fff;
        border: 1px solid var(--line);
        border-radius: 16px;
        box-shadow: var(--panel-shadow);
        padding: 1rem 1.15rem;
    }
    [class*="st-key-model-panel"] { background: #fbfaff; margin-bottom: 1.5rem; }
    [class*="st-key-table-panel"] h3,
    [class*="st-key-chart-panel"] h3 { color: #30254f; font-size: 1.08rem; }
    [data-testid="stDataFrame"] { border: 1px solid #eeeaf5; border-radius: 10px; }
    @media (max-width: 620px) {
        .main .block-container { padding: 1.5rem 1rem 2rem; }
        .hero-title { font-size: 2rem; }
        .metric-grid { grid-template-columns: 1fr; }
        .student-summary { align-items: flex-start; flex-direction: column; }
        [class*="st-key-model-panel"],
        [class*="st-key-table-panel"],
        [class*="st-key-chart-panel"] { padding: 0.8rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p class="hero-kicker">Computational Mathematics Laboratory</p>
    <h1 class="hero-title">Student Performance<br>and Study-Time Predictor</h1>
    <p class="hero-subtitle">Explore how an exponential model closes the gap toward a study goal.</p>
    <div class="quote-banner">
        <p class="quote-text">“Learning never exhausts the mind.”</p>
        <p class="quote-credit">Leonardo da Vinci</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Student and study plan")
    student_name = st.text_input("Student name", value="Alex Morgan", max_chars=80)
    initial_score = st.number_input(
        "Current score (%)", min_value=0.0, max_value=100.0, value=58.0, step=1.0
    )
    target_score = st.number_input(
        "Target score (%)", min_value=0.0, max_value=100.0, value=90.0, step=1.0
    )
    daily_study_hours = st.number_input(
        "Daily study hours", min_value=0.0, max_value=24.0, value=2.5, step=0.5
    )
    study_period_days = st.number_input(
        "Study period (days)", min_value=1, max_value=365, value=30, step=1
    )
    improvement_constant = st.number_input(
        "Improvement constant k", min_value=0.001, value=0.08, step=0.01, format="%.3f"
    )

with st.container(key="model-panel"):
    st.subheader("The exponential gap model")
    st.latex(r"\mathrm{Score}(t) = S_{\max} - (S_{\max} - S_0)e^{-kt}")
    st.write(
        "The remaining gap between the current score and the chosen target decays exponentially, "
        "so the modelled score approaches the target over time."
    )
    st.caption(
        "This is a simplified mathematical simulation, not a scientifically validated predictor "
        "of actual exam results. Daily study hours are used to calculate planned study time; the "
        "specified score formula uses elapsed days and k."
    )

if not student_name.strip():
    st.error("Enter a student name to view the results.")
elif target_score < initial_score:
    st.error("The target score cannot be below the current score.")
else:
    days = np.arange(int(study_period_days) + 1)
    try:
        scores = calculate_scores(
            float(initial_score),
            float(target_score),
            float(improvement_constant),
            days,
        )
    except ValueError as error:
        st.error(str(error))
    else:
        final_score = float(scores[-1])
        score_change = final_score - float(initial_score)
        total_study_hours = float(daily_study_hours) * int(study_period_days)

        st.subheader("Your study snapshot")
        safe_student_name = html.escape(student_name.strip())
        st.markdown(
            f"""
            <div class="student-summary">
                <span class="student-label">Student</span>
                <span class="student-name">{safe_student_name}</span>
                <span class="student-plan">{daily_study_hours:.1f} hours/day</span>
                <span class="student-plan">{int(study_period_days)} study days</span>
                <span class="student-plan">Target {target_score:.1f}%</span>
            </div>
            <div class="metric-grid">
                <div class="metric-card metric-purple">
                    <span class="metric-label">Planned study time</span>
                    <span class="metric-value">{total_study_hours:.1f} hours</span>
                    <span class="metric-detail">Across {int(study_period_days)} planned days</span>
                </div>
                <div class="metric-card metric-pink">
                    <span class="metric-label">Initial score</span>
                    <span class="metric-value">{initial_score:.2f}%</span>
                    <span class="metric-detail">Starting point</span>
                </div>
                <div class="metric-card metric-cyan">
                    <span class="metric-label">Modelled final score</span>
                    <span class="metric-value">{final_score:.2f}%</span>
                    <span class="metric-detail">At the end of the study period</span>
                </div>
                <div class="metric-card metric-emerald">
                    <span class="metric-label">Modelled change</span>
                    <span class="metric-value">{score_change:+.2f}</span>
                    <span class="metric-detail">Percentage points</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        result_table = pd.DataFrame(
            {
                "Study day": days,
                "Modelled score (%)": np.round(scores, 2),
            }
        )

        left_column, right_column = st.columns([1, 1.45], gap="large")
        with left_column:
            with st.container(key="table-panel"):
                st.subheader("Daily score table")
                st.dataframe(result_table, hide_index=True, width="stretch", height=440)

        with right_column:
            with st.container(key="chart-panel"):
                st.subheader("Score over the study period")
                figure, axis = plt.subplots(figsize=(8, 4.8), facecolor="#ffffff")
                axis.set_facecolor("#ffffff")
                axis.plot(days, scores, color="#6848c7", linewidth=2.7, label="Modelled score")
                axis.axhline(
                    float(target_score),
                    color="#e99a43",
                    linestyle="--",
                    linewidth=1.7,
                    label=f"Target ({target_score:.1f}%)",
                )
                axis.set_xlabel("Study time (days)")
                axis.set_ylabel("Score (%)")
                axis.set_ylim(0, 105)
                axis.set_xlim(0, int(study_period_days))
                axis.grid(True, color="#e9e5f1", alpha=0.9)
                axis.spines[["top", "right"]].set_visible(False)
                axis.spines[["left", "bottom"]].set_color("#d8d2e4")
                axis.tick_params(colors="#625b72")
                axis.legend(frameon=False)
                figure.tight_layout()
                st.pyplot(figure, width="stretch")
                plt.close(figure)