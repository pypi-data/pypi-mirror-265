from typing import Dict

from pydantic import BaseModel, Field


class User(BaseModel):
    stub: bool
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Users")
    rev: str
    name: str
    first_name: str = Field(None, alias="firstName")
    last_name: str = Field(None, alias="lastName")
    is_enabled: bool = Field(..., alias="isEnabled")
    is_administrator: bool = Field(..., alias="isAdministrator")
    emails: list[str]
    modified_time: str = Field(..., alias="modifiedTime")
    created_time: str = Field(..., alias="createdTime")


class FoundUsersResult(BaseModel):
    result: list[User]


class Team(BaseModel):
    stub: bool
    id: int
    name: str
    rev: str
    entity_type: str = Field(..., alias="entityType", pattern=r"Teams")
    modified_time: str = Field(..., alias="modifiedTime")
    created_time: str = Field(..., alias="createdTime")


class FoundTeamsResult(BaseModel):
    result: list[Team]


class Activity(BaseModel):
    stub: bool
    id: int
    rev: str
    entity_type: str = Field(..., alias="entityType", pattern=r"Activity_Types")
    name: str


class FoundActivityResult(BaseModel):
    result: list[Activity]


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
    series_data: SeriesData = Field(..., alias="seriesData")
    summary_data: Dict[str, SummaryData] = Field(..., alias="summaryData")
    period_description: str = Field(..., alias="periodDescription")
    delta_period_description: str = Field(..., alias="deltaPeriodDescription")


class AnalyticsResult(BaseModel):
    result: AnalyticsReport
