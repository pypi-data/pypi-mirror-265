from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, computed_field


class FindUsers(BaseModel):
    """findUsers method for Nutshell API."""
    query: Optional[dict] = None
    order_by: str = "last_name"
    order_direction: str = "ASC"
    limit: None | int = 100
    page: int = 1
    api_method: str = "findUsers"

    @computed_field
    @property
    def params(self) -> dict:
        params = {}
        if self.query:
            params["query"] = self.query
        if self.order_by:
            params["orderBy"] = self.order_by
        if self.order_direction:
            params["orderDirection"] = self.order_direction
        if self.limit:
            params["limit"] = self.limit
        if self.page:
            params["page"] = self.page

        return params


class GetUser(BaseModel):
    """For retrieving a single user from the Nutshell API."""
    user_id: int
    api_method: str = "getUser"

    @computed_field
    @property
    def params(self) -> dict:
        return {"userId": self.user_id}


class ReportType(StrEnum):
    EFFORT = "Effort"
    PIPELINE = "Pipeline"


class FilterEntity(StrEnum):
    USERS = "Users"
    TEAMS = "Teams"
    ACTIVITY_TYPES = "Activity_Types"


class ReportFilter(BaseModel):
    """For building a valid filter for the Nutshell API."""
    entity_id: int
    entity_name: FilterEntity

    @computed_field
    @property
    def filter(self) -> dict:
        return {"entityId": self.entity_id, "entityName": self.entity_name.value}


class GetAnalyticsReport(BaseModel):
    """For building a valid query to the Nutshell API for the getAnalyticsReport method."""
    report_type: ReportType = ReportType.EFFORT
    period: str = "-d30"
    filters: list[ReportFilter] = None
    api_method: str = "getAnalyticsReport"

    @computed_field
    @property
    def params(self) -> dict:
        params = {"reportType": self.report_type.value,
                  "period": self.period}
        if self.filters:
            params["filter"] = [entity_filter.filter for entity_filter in self.filters]
        return params
