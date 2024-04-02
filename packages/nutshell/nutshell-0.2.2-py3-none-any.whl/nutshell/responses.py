from typing import Dict

from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    """Base class for all API responses."""
    result: list[BaseModel] | BaseModel


class User(BaseModel):
    stub: bool = None
    id: int
    entity_type: str = Field(..., validation_alias="entityType", pattern=r"Users")
    rev: str
    name: str
    first_name: str = Field(None, validation_alias="firstName")
    last_name: str = Field(None, validation_alias="lastName")
    is_enabled: bool = Field(..., validation_alias="isEnabled")
    is_administrator: bool = Field(..., validation_alias="isAdministrator")
    emails: list[str]
    modified_time: str = Field(..., validation_alias="modifiedTime")
    created_time: str = Field(..., validation_alias="createdTime")


class Team(BaseModel):
    stub: bool
    id: int
    name: str
    rev: str
    entity_type: str = Field(..., validation_alias="entityType", pattern=r"Teams")
    modified_time: str = Field(..., validation_alias="modifiedTime")
    created_time: str = Field(..., validation_alias="createdTime")


class ActivityTypes(BaseModel):
    stub: bool
    id: int
    rev: str
    entity_type: str = Field(..., validation_alias="entityType", pattern=r"Activity_Types")
    name: str


class SeriesData(BaseModel):
    total_effort: list[list[int]]
    successful_effort: list[list[int]]


class SummaryData(BaseModel):
    sum: float
    avg: float
    min: float
    max: float
    sum_delta: float
    avg_delta: float
    min_delta: float
    max_delta: float


class AnalyticsReport(BaseModel):
    series_data: SeriesData = Field(..., validation_alias="seriesData")
    summary_data: Dict[str, SummaryData] = Field(..., validation_alias="summaryData")
    period_description: str = Field(..., validation_alias="periodDescription")
    delta_period_description: str = Field(..., validation_alias="deltaPeriodDescription")


class FindUsersResult(APIResponse):
    result: list[User]


class GetUserResult(APIResponse):
    result: User


class FindTeamsResult(APIResponse):
    result: list[Team]


class FindActivityTypesResult(APIResponse):
    result: list[ActivityTypes]


class GetAnalyticsReportResult(APIResponse):
    result: AnalyticsReport
