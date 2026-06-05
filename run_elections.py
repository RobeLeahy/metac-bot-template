import asyncio
import logging

from forecasting_tools import GeneralLlm
from main import SummerTemplateBot2026

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Metaculus election tournaments for Sparky to forecast on
ELECTION_TOURNAMENTS = [
    "midterms-2026",
    "POTUS-predictions",
]

sparky = SummerTemplateBot2026(
    research_reports_per_question=1,
    predictions_per_research_report=5,
    use_research_summary_to_forecast=False,
    publish_reports_to_metaculus=True,
    folder_to_save_reports_to=None,
    skip_previously_forecasted_questions=True,
    extra_metadata_in_explanation=True,
    llms={
        "default": GeneralLlm(
            model="anthropic/claude-opus-4-8",
            timeout=60,
            allowed_tries=2,
        ),
        "summarizer": "anthropic/claude-haiku-4-5",
        "researcher": "anthropic/claude-sonnet-4-6",
        "parser": "anthropic/claude-haiku-4-5",
    },
)

all_reports = []
for tournament in ELECTION_TOURNAMENTS:
    reports = asyncio.run(
        sparky.forecast_on_tournament(tournament, return_exceptions=True)
    )
    all_reports.extend(reports)

sparky.log_report_summary(all_reports)
