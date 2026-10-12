
from typing import Any

import httpx

from src.configs.config import settings


class SQLPlannerError(Exception):
    """Raised when the SQL Planner cannot return valid data."""


class SQLPlannerClient:
    """
    Adapter for the existing SQL Planner API.

    Mock mode:
        Returns simulated internal business metrics.

    Real mode:
        Calls the existing SQL Planner HTTP API.

    The real API payload and response mapping must be
    aligned with the actual SQL Planner contract.
    """

    async def execute(
        self,
        question: str,
        session_id: str,
        dashboard_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        if settings.USE_MOCK_SQL:
            return self._mock_response(
                question,
                dashboard_context,
            )

        return await self._real_request(
            question,
            session_id,
            dashboard_context,
        )

    def _mock_response(
        self,
        question: str,
        dashboard_context: dict[str, Any] | None,
    ) -> dict[str, Any]:

        context = dashboard_context or {}

        product_name = (
            context.get("productName") or "Demo Product"
        )

        question_lower = question.lower()

        if any(
            word in question_lower
            for word in ["sales", "revenue", "declining"]
        ):
            metrics = {
                "sales_current": 125000,
                "sales_previous": 140000,
                "sales_change_pct": -10.71,
                "currency": "USD",
            }

        elif any(
            word in question_lower
            for word in ["profit", "margin", "profitability"]
        ):
            metrics = {
                "profit_current": 22500,
                "profit_previous": 24500,
                "margin_pct": 18.0,
                "currency": "USD",
            }

        else:
            metrics = {
                "sales_current": 125000,
                "profit_current": 22500,
                "margin_pct": 18.0,
                "currency": "USD",
            }

        return {
            "status": "success",
            "source": "mock_sql",
            "is_mock": True,
            "product_name": product_name,
            "metrics": metrics,
            "data_available": True,
        }

    async def _real_request(
        self,
        question: str,
        session_id: str,
        dashboard_context: dict[str, Any] | None,
    ) -> dict[str, Any]:

        if not settings.SQL_PLANNER_URL:
            raise SQLPlannerError(
                "SQL_PLANNER_URL is not configured."
            )

        # Placeholder request contract.
        # Update after receiving the real API specification.
        payload = {
            "question": question,
            "session_id": session_id,
            "dashboard_context": dashboard_context or {},
        }

        headers = {
            "Content-Type": "application/json",
        }

        if settings.SQL_PLANNER_API_KEY:
            headers["Authorization"] = (
                f"Bearer {settings.SQL_PLANNER_API_KEY}"
            )

        try:
            async with httpx.AsyncClient(
                timeout=settings.SQL_PLANNER_TIMEOUT
            ) as client:
                response = await client.post(
                    settings.SQL_PLANNER_URL,
                    json=payload,
                    headers=headers,
                )

                response.raise_for_status()
                data = response.json()

        except httpx.HTTPError as exc:
            raise SQLPlannerError(
                "SQL Planner API request failed."
            ) from exc

        except ValueError as exc:
            raise SQLPlannerError(
                "SQL Planner returned invalid JSON."
            ) from exc

        if not isinstance(data, dict):
            raise SQLPlannerError(
                "SQL Planner response must be a JSON object."
            )

        # Temporary expected contract.
        # Adapt this mapping to the real SQL Planner output.
        if (
            not isinstance(data.get("metrics"), dict)
            or not isinstance(data.get("data_available"), bool)
        ):
            raise SQLPlannerError(
                "SQL Planner response does not match "
                "the expected schema."
            )

        return {
            "status": "success",
            "source": "sql_planner_api",
            "is_mock": False,
            "product_name": data.get("product_name"),
            "metrics": data["metrics"],
            "data_available": data["data_available"],
        }


sql_planner_client = SQLPlannerClient()
