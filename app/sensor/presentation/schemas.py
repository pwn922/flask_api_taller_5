from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class SensorDataRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )

    device_id: str = Field(
        ...,
        validation_alias=AliasChoices("deviceId", "device_id"),
        min_length=1,
    )
    temperature: float = Field(
        ...,
        validation_alias=AliasChoices("temperatura", "temperature"),
    )
    humidity: float = Field(
        ...,
        validation_alias=AliasChoices("humedad", "humidity"),
    )
    water_level: float = Field(
        ...,
        validation_alias=AliasChoices("nivelAgua", "water_level"),
    )