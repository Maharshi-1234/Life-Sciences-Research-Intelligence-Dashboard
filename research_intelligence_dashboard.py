# =============================================================================
# Title     : Life Sciences Research Intelligence Dashboard
# Author    : Ramana Maharshi Mellacheruvu
# Date      : 09-06-2026
# Objective : Build an interactive Drug Discovery dashboard that supports data
#             viewing, searching, filtering, metrics, insights, alerts,
#             recommendations, charts, and report export.
# =============================================================================

"""
Pseudocode:
1. Define dataset paths, required fields, and analytical thresholds.
2. Load and validate the Drug Discovery CSV dataset.
3. Configure a Streamlit dashboard with multiple navigation sections.
4. Allow users to view the complete dataset.
5. Allow users to search using compound ID, compound name, target, or researcher.
6. Allow users to filter using stage, status, priority, country, target, and year.
7. Calculate and display business metrics.
8. Generate management-oriented insights.
9. Create charts for status, stage, target, priority, and yearly trends.
10. Implement an alert and recommendation engine.
11. Allow users to export filtered data and a dashboard summary report.
12. Handle and display relevant errors.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIRECTORY = Path(__file__).resolve().parent

DATA_FILE = (
    BASE_DIRECTORY
    / "Dataset"
    / "research_dashboard_data.csv"
)

REQUIRED_COLUMNS = {
    "compound_id",
    "compound_name",
    "target_protein",
    "research_stage",
    "assigned_researcher",
    "toxicity_score",
    "efficacy_score",
    "processing_days",
    "development_status",
    "priority",
    "country",
    "study_year",
}

NUMERIC_COLUMNS = [
    "toxicity_score",
    "efficacy_score",
    "processing_days",
    "study_year",
]

HIGH_TOXICITY_THRESHOLD = 70
LOW_EFFICACY_THRESHOLD = 60
HIGH_EFFICACY_THRESHOLD = 85
DELAY_THRESHOLD_DAYS = 45
ACCEPTABLE_TOXICITY_THRESHOLD = 50


# ---------------------------------------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Research Intelligence Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Task 2 - CSV Data Storage Layer
# ---------------------------------------------------------------------------

@st.cache_data
def load_dataset(file_path: Path) -> pd.DataFrame:
    """
    Load and validate the Drug Discovery dashboard dataset.

    Args:
        file_path: Path of the source CSV file.

    Returns:
        Validated Drug Discovery DataFrame.

    Raises:
        FileNotFoundError: If the dataset is unavailable.
        ValueError: If required columns or numeric values are invalid.
    """
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    dataset = pd.read_csv(file_path)

    missing_columns = REQUIRED_COLUMNS - set(
        dataset.columns
    )

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            f"{', '.join(sorted(missing_columns))}"
        )

    for column_name in NUMERIC_COLUMNS:
        converted_values = pd.to_numeric(
            dataset[column_name],
            errors="coerce",
        )

        if converted_values.isna().any():
            raise ValueError(
                f"Column '{column_name}' contains "
                "invalid numeric values."
            )

        dataset[column_name] = converted_values

    return dataset


# ---------------------------------------------------------------------------
# Task 5 - Business Metrics
# ---------------------------------------------------------------------------

def calculate_business_metrics(
    dataset: pd.DataFrame,
) -> dict:
    """
    Calculate Drug Discovery business metrics.

    Args:
        dataset: DataFrame to analyse.

    Returns:
        Dictionary containing dashboard metrics.
    """
    high_potential_mask = (
        dataset["efficacy_score"]
        >= HIGH_EFFICACY_THRESHOLD
    ) & (
        dataset["toxicity_score"]
        <= ACCEPTABLE_TOXICITY_THRESHOLD
    )

    delayed_mask = (
        dataset["processing_days"]
        >= DELAY_THRESHOLD_DAYS
    )

    return {
        "total_compounds": int(
            dataset["compound_id"].nunique()
        ),
        "active_compounds": int(
            (
                dataset["development_status"]
                == "Active"
            ).sum()
        ),
        "promising_compounds": int(
            (
                dataset["development_status"]
                == "Promising"
            ).sum()
        ),
        "delayed_compounds": int(
            delayed_mask.sum()
        ),
        "high_priority_compounds": int(
            (
                dataset["priority"] == "High"
            ).sum()
        ),
        "high_potential_compounds": int(
            high_potential_mask.sum()
        ),
        "average_efficacy": round(
            float(
                dataset["efficacy_score"].mean()
            ),
            2,
        ),
        "average_toxicity": round(
            float(
                dataset["toxicity_score"].mean()
            ),
            2,
        ),
        "average_processing_days": round(
            float(
                dataset["processing_days"].mean()
            ),
            2,
        ),
        "distinct_targets": int(
            dataset["target_protein"].nunique()
        ),
        "distinct_researchers": int(
            dataset["assigned_researcher"].nunique()
        ),
        "distinct_countries": int(
            dataset["country"].nunique()
        ),
    }


# ---------------------------------------------------------------------------
# Task 6 - Insights Section
# ---------------------------------------------------------------------------

def generate_business_insights(
    dataset: pd.DataFrame,
) -> list[str]:
    """
    Generate management-oriented Drug Discovery insights.

    Args:
        dataset: DataFrame to analyse.

    Returns:
        List containing generated insights.
    """
    if dataset.empty:
        return [
            "No records are available for insight generation."
        ]

    highest_efficacy_record = dataset.loc[
        dataset["efficacy_score"].idxmax()
    ]

    highest_toxicity_record = dataset.loc[
        dataset["toxicity_score"].idxmax()
    ]

    most_delayed_record = dataset.loc[
        dataset["processing_days"].idxmax()
    ]

    most_active_researcher = (
        dataset["assigned_researcher"]
        .value_counts()
        .idxmax()
    )

    researcher_count = int(
        dataset["assigned_researcher"]
        .value_counts()
        .max()
    )

    most_studied_target = (
        dataset["target_protein"]
        .value_counts()
        .idxmax()
    )

    target_count = int(
        dataset["target_protein"]
        .value_counts()
        .max()
    )

    most_common_stage = (
        dataset["research_stage"]
        .value_counts()
        .idxmax()
    )

    stage_count = int(
        dataset["research_stage"]
        .value_counts()
        .max()
    )

    leading_country = (
        dataset["country"]
        .value_counts()
        .idxmax()
    )

    country_count = int(
        dataset["country"]
        .value_counts()
        .max()
    )

    high_potential_count = int(
        (
            (
                dataset["efficacy_score"]
                >= HIGH_EFFICACY_THRESHOLD
            )
            & (
                dataset["toxicity_score"]
                <= ACCEPTABLE_TOXICITY_THRESHOLD
            )
        ).sum()
    )

    return [
        (
            f"{highest_efficacy_record['compound_name']} has the "
            f"highest efficacy score of "
            f"{highest_efficacy_record['efficacy_score']}."
        ),
        (
            f"{highest_toxicity_record['compound_name']} has the "
            f"highest toxicity score of "
            f"{highest_toxicity_record['toxicity_score']}."
        ),
        (
            f"{most_delayed_record['compound_name']} has the "
            f"longest processing time at "
            f"{most_delayed_record['processing_days']} days."
        ),
        (
            f"{most_active_researcher} manages the largest portfolio "
            f"with {researcher_count} compounds."
        ),
        (
            f"{most_studied_target} is the most frequently studied "
            f"target protein, with {target_count} compounds."
        ),
        (
            f"{most_common_stage} is the most common research stage, "
            f"covering {stage_count} compounds."
        ),
        (
            f"{leading_country} contains the largest compound portfolio "
            f"with {country_count} records."
        ),
        (
            f"{high_potential_count} compounds combine high efficacy "
            "with acceptable toxicity."
        ),
    ]


# ---------------------------------------------------------------------------
# Task 7 - Custom Feature: Alert and Recommendation Engine
# ---------------------------------------------------------------------------

def identify_alerts(
    dataset: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """
    Identify scientific and operational alerts.

    Args:
        dataset: DataFrame to analyse.

    Returns:
        Dictionary containing alert records.
    """
    high_toxicity = dataset.loc[
        dataset["toxicity_score"]
        >= HIGH_TOXICITY_THRESHOLD
    ].copy()

    low_efficacy = dataset.loc[
        dataset["efficacy_score"]
        < LOW_EFFICACY_THRESHOLD
    ].copy()

    delayed = dataset.loc[
        dataset["processing_days"]
        >= DELAY_THRESHOLD_DAYS
    ].copy()

    high_priority_risk = dataset.loc[
        (
            dataset["priority"] == "High"
        )
        & (
            (
                dataset["toxicity_score"]
                >= HIGH_TOXICITY_THRESHOLD
            )
            | (
                dataset["efficacy_score"]
                < LOW_EFFICACY_THRESHOLD
            )
            | (
                dataset["processing_days"]
                >= DELAY_THRESHOLD_DAYS
            )
        )
    ].copy()

    stalled = dataset.loc[
        dataset["development_status"].isin(
            [
                "On Hold",
                "Discontinued",
            ]
        )
    ].copy()

    return {
        "high_toxicity": high_toxicity,
        "low_efficacy": low_efficacy,
        "delayed": delayed,
        "high_priority_risk": high_priority_risk,
        "stalled": stalled,
    }


def generate_recommendations(
    alerts: dict[str, pd.DataFrame],
) -> list[str]:
    """
    Generate recommendations from identified alerts.

    Args:
        alerts: Alert records grouped by category.

    Returns:
        List containing management recommendations.
    """
    recommendations = []

    high_toxicity_count = len(
        alerts["high_toxicity"]
    )

    low_efficacy_count = len(
        alerts["low_efficacy"]
    )

    delayed_count = len(
        alerts["delayed"]
    )

    high_priority_count = len(
        alerts["high_priority_risk"]
    )

    stalled_count = len(
        alerts["stalled"]
    )

    if high_toxicity_count:
        recommendations.append(
            f"Review {high_toxicity_count} compounds with toxicity "
            f"scores of {HIGH_TOXICITY_THRESHOLD} or above."
        )

    if low_efficacy_count:
        recommendations.append(
            f"Reassess {low_efficacy_count} compounds with efficacy "
            f"scores below {LOW_EFFICACY_THRESHOLD}."
        )

    if delayed_count:
        recommendations.append(
            f"Investigate processing bottlenecks affecting "
            f"{delayed_count} delayed compounds."
        )

    if high_priority_count:
        recommendations.append(
            f"Escalate {high_priority_count} high-priority compounds "
            "showing poor scientific or operational performance."
        )

    if stalled_count:
        recommendations.append(
            f"Conduct portfolio review for {stalled_count} compounds "
            "that are On Hold or Discontinued."
        )

    recommendations.append(
        "Prioritize high-efficacy, low-toxicity compounds for "
        "further development."
    )

    return recommendations


# ---------------------------------------------------------------------------
# Task 3 - Search Functionality
# ---------------------------------------------------------------------------

def search_dataset(
    dataset: pd.DataFrame,
    search_field: str,
    search_term: str,
) -> pd.DataFrame:
    """
    Search the dataset using one selected field.

    Args:
        dataset: Source DataFrame.
        search_field: Field selected for search.
        search_term: User-entered search value.

    Returns:
        DataFrame containing matching records.
    """
    if not search_term.strip():
        return dataset.copy()

    return dataset.loc[
        dataset[search_field]
        .astype(str)
        .str.contains(
            search_term.strip(),
            case=False,
            na=False,
        )
    ].copy()


# ---------------------------------------------------------------------------
# Task 4 - Filtering Functionality
# ---------------------------------------------------------------------------

def apply_filters(
    dataset: pd.DataFrame,
    selected_stages: list[str],
    selected_statuses: list[str],
    selected_priorities: list[str],
    selected_countries: list[str],
    selected_targets: list[str],
    selected_researchers: list[str],
    selected_years: list[int],
) -> pd.DataFrame:
    """
    Apply interactive dashboard filters.

    Args:
        dataset: Source DataFrame.
        selected_stages: Selected research stages.
        selected_statuses: Selected development statuses.
        selected_priorities: Selected priorities.
        selected_countries: Selected countries.
        selected_targets: Selected target proteins.
        selected_researchers: Selected researchers.
        selected_years: Selected study years.

    Returns:
        Filtered DataFrame.
    """
    filtered_dataset = dataset.copy()

    if selected_stages:
        filtered_dataset = filtered_dataset.loc[
            filtered_dataset["research_stage"]
            .isin(selected_stages)
        ]

    if selected_statuses:
        filtered_dataset = filtered_dataset.loc[
            filtered_dataset["development_status"]
            .isin(selected_statuses)
        ]

    if selected_priorities:
        filtered_dataset = filtered_dataset.loc[
            filtered_dataset["priority"]
            .isin(selected_priorities)
        ]

    if selected_countries:
        filtered_dataset = filtered_dataset.loc[
            filtered_dataset["country"]
            .isin(selected_countries)
        ]

    if selected_targets:
        filtered_dataset = filtered_dataset.loc[
            filtered_dataset["target_protein"]
            .isin(selected_targets)
        ]

    if selected_researchers:
        filtered_dataset = filtered_dataset.loc[
            filtered_dataset["assigned_researcher"]
            .isin(selected_researchers)
        ]

    if selected_years:
        filtered_dataset = filtered_dataset.loc[
            filtered_dataset["study_year"]
            .isin(selected_years)
        ]

    return filtered_dataset


# ---------------------------------------------------------------------------
# Stretch Goal - Export Report Feature
# ---------------------------------------------------------------------------

def create_dashboard_report(
    dataset: pd.DataFrame,
    metrics: dict,
    insights: list[str],
    alerts: dict[str, pd.DataFrame],
    recommendations: list[str],
) -> str:
    """
    Create a downloadable dashboard summary report.

    Args:
        dataset: Analysed DataFrame.
        metrics: Dashboard metrics.
        insights: Generated insights.
        alerts: Identified alerts.
        recommendations: Generated recommendations.

    Returns:
        Formatted text report.
    """
    report_lines = [
        "=" * 79,
        "DRUG DISCOVERY RESEARCH INTELLIGENCE DASHBOARD REPORT",
        "=" * 79,
        "",
        "DATASET SUMMARY",
        "-" * 79,
        f"Records Analysed           : {len(dataset)}",
        f"Total Compounds            : {metrics['total_compounds']}",
        f"Active Compounds           : {metrics['active_compounds']}",
        f"Promising Compounds        : {metrics['promising_compounds']}",
        f"Delayed Compounds          : {metrics['delayed_compounds']}",
        f"High-Priority Compounds    : {metrics['high_priority_compounds']}",
        f"High-Potential Compounds   : {metrics['high_potential_compounds']}",
        f"Average Efficacy           : {metrics['average_efficacy']}",
        f"Average Toxicity           : {metrics['average_toxicity']}",
        f"Average Processing Days    : {metrics['average_processing_days']}",
        "",
        "KEY INSIGHTS",
        "-" * 79,
    ]

    for number, insight in enumerate(
        insights,
        start=1,
    ):
        report_lines.append(
            f"{number}. {insight}"
        )

    report_lines.extend([
        "",
        "ALERT SUMMARY",
        "-" * 79,
        f"High-Toxicity Alerts       : {len(alerts['high_toxicity'])}",
        f"Low-Efficacy Alerts        : {len(alerts['low_efficacy'])}",
        f"Delayed Alerts             : {len(alerts['delayed'])}",
        f"High-Priority Risk Alerts  : {len(alerts['high_priority_risk'])}",
        f"Stalled Compounds          : {len(alerts['stalled'])}",
        "",
        "RECOMMENDATIONS",
        "-" * 79,
    ])

    for number, recommendation in enumerate(
        recommendations,
        start=1,
    ):
        report_lines.append(
            f"{number}. {recommendation}"
        )

    report_lines.extend([
        "",
        "=" * 79,
    ])

    return "\n".join(report_lines)


# ---------------------------------------------------------------------------
# Dashboard Utility Functions
# ---------------------------------------------------------------------------

def display_metric_cards(metrics: dict) -> None:
    """
    Display dashboard metric cards.

    Args:
        metrics: Calculated business metrics.
    """
    row_one = st.columns(5)

    row_one[0].metric(
        "Total Compounds",
        metrics["total_compounds"],
    )
    row_one[1].metric(
        "Active",
        metrics["active_compounds"],
    )
    row_one[2].metric(
        "Promising",
        metrics["promising_compounds"],
    )
    row_one[3].metric(
        "Delayed",
        metrics["delayed_compounds"],
    )
    row_one[4].metric(
        "High Priority",
        metrics["high_priority_compounds"],
    )

    row_two = st.columns(5)

    row_two[0].metric(
        "High Potential",
        metrics["high_potential_compounds"],
    )
    row_two[1].metric(
        "Average Efficacy",
        metrics["average_efficacy"],
    )
    row_two[2].metric(
        "Average Toxicity",
        metrics["average_toxicity"],
    )
    row_two[3].metric(
        "Average Processing",
        f"{metrics['average_processing_days']} days",
    )
    row_two[4].metric(
        "Target Proteins",
        metrics["distinct_targets"],
    )


def display_empty_result_message() -> None:
    """Display a standard no-results message."""
    st.warning(
        "No records match the selected search or filter criteria."
    )


# ---------------------------------------------------------------------------
# Task 1 - Application Design
# ---------------------------------------------------------------------------

def run_dashboard(dataset: pd.DataFrame) -> None:
    """
    Run the interactive Streamlit dashboard.

    Args:
        dataset: Validated Drug Discovery DataFrame.
    """
    st.sidebar.title("Navigation")

    selected_page = st.sidebar.radio(
        "Go to",
        [
            "Home",
            "View Data",
            "Search",
            "Filters",
            "Metrics",
            "Insights",
            "Alerts & Recommendations",
            "Export Report",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Drug Discovery Research Intelligence Dashboard"
    )

    if selected_page == "Home":
        st.title(
            "🧬 Life Sciences Research Intelligence Dashboard"
        )

        st.subheader("Drug Discovery Intelligence")

        st.write(
            "This dashboard helps business and scientific users "
            "search, filter, analyse, and interpret Drug Discovery "
            "research data."
        )

        metrics = calculate_business_metrics(
            dataset
        )

        display_metric_cards(
            metrics
        )

        st.markdown("### Application Capabilities")

        st.markdown(
            """
            - View all compound records
            - Search by multiple fields
            - Apply interactive filters
            - View business metrics
            - Generate scientific insights
            - Identify operational alerts
            - Generate management recommendations
            - Export filtered data and a summary report
            """
        )

        st.markdown("### Data Flow")

        st.info(
            "CSV Dataset → pandas Analysis → Streamlit Dashboard "
            "→ Metrics, Insights, Alerts and Exported Reports"
        )

    elif selected_page == "View Data":
        st.title("View Drug Discovery Data")

        st.write(
            f"Displaying {len(dataset)} records and "
            f"{len(dataset.columns)} fields."
        )

        st.dataframe(
            dataset,
            use_container_width=True,
            hide_index=True,
        )

    elif selected_page == "Search":
        st.title("Search Compound Information")

        search_field_labels = {
            "Compound ID": "compound_id",
            "Compound Name": "compound_name",
            "Target Protein": "target_protein",
            "Researcher Name": "assigned_researcher",
        }

        selected_label = st.selectbox(
            "Search field",
            list(search_field_labels.keys()),
        )

        search_term = st.text_input(
            "Enter search value"
        )

        search_results = search_dataset(
            dataset,
            search_field_labels[selected_label],
            search_term,
        )

        st.write(
            f"Matching records: {len(search_results)}"
        )

        if search_results.empty:
            display_empty_result_message()
        else:
            st.dataframe(
                search_results,
                use_container_width=True,
                hide_index=True,
            )

    elif selected_page == "Filters":
        st.title("Filter Drug Discovery Data")

        filter_column_one, filter_column_two = st.columns(2)

        with filter_column_one:
            selected_stages = st.multiselect(
                "Research Stage",
                sorted(
                    dataset["research_stage"].unique()
                ),
            )

            selected_statuses = st.multiselect(
                "Development Status",
                sorted(
                    dataset["development_status"].unique()
                ),
            )

            selected_priorities = st.multiselect(
                "Priority",
                sorted(
                    dataset["priority"].unique()
                ),
            )

            selected_years = st.multiselect(
                "Study Year",
                sorted(
                    dataset["study_year"].unique()
                ),
            )

        with filter_column_two:
            selected_countries = st.multiselect(
                "Country",
                sorted(
                    dataset["country"].unique()
                ),
            )

            selected_targets = st.multiselect(
                "Target Protein",
                sorted(
                    dataset["target_protein"].unique()
                ),
            )

            selected_researchers = st.multiselect(
                "Assigned Researcher",
                sorted(
                    dataset["assigned_researcher"].unique()
                ),
            )

        filtered_dataset = apply_filters(
            dataset,
            selected_stages,
            selected_statuses,
            selected_priorities,
            selected_countries,
            selected_targets,
            selected_researchers,
            selected_years,
        )

        st.write(
            f"Filtered records: {len(filtered_dataset)}"
        )

        if filtered_dataset.empty:
            display_empty_result_message()
        else:
            filtered_metrics = calculate_business_metrics(
                filtered_dataset
            )

            display_metric_cards(
                filtered_metrics
            )

            st.dataframe(
                filtered_dataset,
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                label="Download Filtered Data",
                data=filtered_dataset.to_csv(
                    index=False
                ),
                file_name="filtered_research_data.csv",
                mime="text/csv",
            )

    elif selected_page == "Metrics":
        st.title("Drug Discovery Metrics Dashboard")

        metrics = calculate_business_metrics(
            dataset
        )

        display_metric_cards(
            metrics
        )

        st.markdown("### Development Status Distribution")

        status_distribution = (
            dataset["development_status"]
            .value_counts()
        )

        st.bar_chart(
            status_distribution
        )

        st.markdown("### Research Stage Distribution")

        stage_distribution = (
            dataset["research_stage"]
            .value_counts()
        )

        st.bar_chart(
            stage_distribution
        )

        st.markdown("### Priority Distribution")

        priority_distribution = (
            dataset["priority"]
            .value_counts()
        )

        st.bar_chart(
            priority_distribution
        )

        st.markdown("### Average Efficacy by Target Protein")

        target_efficacy = (
            dataset.groupby(
                "target_protein"
            )["efficacy_score"]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            target_efficacy
        )

        st.markdown("### Research Activity by Year")

        yearly_activity = (
            dataset["study_year"]
            .value_counts()
            .sort_index()
        )

        st.line_chart(
            yearly_activity
        )

    elif selected_page == "Insights":
        st.title("Business and Scientific Insights")

        insights = generate_business_insights(
            dataset
        )

        for number, insight in enumerate(
            insights,
            start=1,
        ):
            st.success(
                f"Insight {number}: {insight}"
            )

        st.markdown("### Top Compounds by Efficacy")

        top_compounds = (
            dataset[
                [
                    "compound_id",
                    "compound_name",
                    "efficacy_score",
                    "toxicity_score",
                    "development_status",
                ]
            ]
            .sort_values(
                by=[
                    "efficacy_score",
                    "toxicity_score",
                ],
                ascending=[
                    False,
                    True,
                ],
            )
            .head(10)
        )

        st.dataframe(
            top_compounds,
            use_container_width=True,
            hide_index=True,
        )

    elif selected_page == "Alerts & Recommendations":
        st.title("Alert and Recommendation Engine")

        alerts = identify_alerts(
            dataset
        )

        alert_columns = st.columns(5)

        alert_columns[0].metric(
            "High Toxicity",
            len(alerts["high_toxicity"]),
        )
        alert_columns[1].metric(
            "Low Efficacy",
            len(alerts["low_efficacy"]),
        )
        alert_columns[2].metric(
            "Delayed",
            len(alerts["delayed"]),
        )
        alert_columns[3].metric(
            "High-Priority Risk",
            len(alerts["high_priority_risk"]),
        )
        alert_columns[4].metric(
            "Stalled",
            len(alerts["stalled"]),
        )

        selected_alert = st.selectbox(
            "Select alert category",
            [
                "High Toxicity",
                "Low Efficacy",
                "Delayed",
                "High-Priority Risk",
                "Stalled",
            ],
        )

        alert_mapping = {
            "High Toxicity": "high_toxicity",
            "Low Efficacy": "low_efficacy",
            "Delayed": "delayed",
            "High-Priority Risk": "high_priority_risk",
            "Stalled": "stalled",
        }

        selected_alert_data = alerts[
            alert_mapping[selected_alert]
        ]

        st.dataframe(
            selected_alert_data,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Recommendations")

        recommendations = generate_recommendations(
            alerts
        )

        for number, recommendation in enumerate(
            recommendations,
            start=1,
        ):
            st.warning(
                f"Recommendation {number}: {recommendation}"
            )

    elif selected_page == "Export Report":
        st.title("Export Dashboard Report")

        metrics = calculate_business_metrics(
            dataset
        )

        insights = generate_business_insights(
            dataset
        )

        alerts = identify_alerts(
            dataset
        )

        recommendations = generate_recommendations(
            alerts
        )

        dashboard_report = create_dashboard_report(
            dataset,
            metrics,
            insights,
            alerts,
            recommendations,
        )

        st.text_area(
            "Report Preview",
            dashboard_report,
            height=500,
        )

        st.download_button(
            label="Download Dashboard Report",
            data=dashboard_report,
            file_name="research_intelligence_report.txt",
            mime="text/plain",
        )

        st.download_button(
            label="Download Complete Dataset",
            data=dataset.to_csv(
                index=False
            ),
            file_name="research_dashboard_data_export.csv",
            mime="text/csv",
        )


# ---------------------------------------------------------------------------
# Main Program
# ---------------------------------------------------------------------------

def main() -> None:
    """Load the dataset and run the dashboard application."""
    try:
        research_data = load_dataset(
            DATA_FILE
        )

        run_dashboard(
            research_data
        )

    except FileNotFoundError as error:
        st.error(
            f"File Error: {error}"
        )

    except pd.errors.EmptyDataError:
        st.error(
            "The dashboard dataset is empty."
        )

    except pd.errors.ParserError as error:
        st.error(
            "The CSV dataset could not be parsed. "
            f"Details: {error}"
        )

    except ValueError as error:
        st.error(
            f"Dataset Validation Error: {error}"
        )

    except KeyError as error:
        st.error(
            f"Required field missing: {error}"
        )

    except Exception as error:
        st.error(
            "An unexpected error occurred while running "
            f"the dashboard: {error}"
        )


if __name__ == "__main__":
    main()