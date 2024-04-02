from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, computed_field


class APIMethod(BaseModel):
    """Base class for all method calls to the Nutshell API."""
    api_method: str

    @computed_field
    @property
    def params(self) -> dict:
        return {}


class FindUsers(APIMethod):
    """findUsers method for Nutshell API."""
    query: Optional[dict] = None
    order_by: str = "last_name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findUsers"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }
        if self.query:
            params["query"] = self.query

        return params


class GetUser(APIMethod):
    """For retrieving a single user from the Nutshell API."""
    user_id: int = None  # with no user_id, the API will return the current user
    rev: str = None  # included to match API documentation
    api_method: str = "getUser"

    @computed_field
    @property
    def params(self) -> dict:
        params = {}
        if self.user_id:
            params["userId"] = self.user_id
        if self.rev:
            params["rev"] = self.rev
        return params


class FindTeams(APIMethod):
    """For retrieving a list of teams from the Nutshell API."""
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findTeams"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }

        return params


class FindActivityTypes(APIMethod):
    """For retrieving a list of activity types from the Nutshell API."""
    order_by: str = "name"
    order_direction: str = "ASC"
    limit: int = 50
    page: int = 1
    api_method: str = "findActivityTypes"

    @computed_field
    @property
    def params(self) -> dict:
        params = {
            "orderBy": self.order_by,
            "orderDirection": self.order_direction,
            "limit": self.limit,
            "page": self.page
        }

        return params


# TODO: add more types to match the API documentation
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


class GetAnalyticsReport(APIMethod):
    """For building a valid query to the Nutshell API for the getAnalyticsReport method."""
    report_type: ReportType
    period: str
    filters: list[ReportFilter] = None
    options: list[dict] = None  # little documentation 
    api_method: str = "getAnalyticsReport"

    @computed_field
    @property
    def params(self) -> dict:
        params = {"reportType": self.report_type.value,
                  "period": self.period}
        if self.filters:
            params["filter"] = [entity_filter.filter for entity_filter in self.filters]
        if self.options:
            params["options"] = self.options
        return params
