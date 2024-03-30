from configparser import ConfigParser
from enum import Enum
from io import TextIOWrapper
from pydantic import BaseModel, Field
from typing import Optional, cast


class ServiceType(Enum):
    simple = 'simple'
    exec = 'exec'
    forking = 'forking'
    oneshot = 'oneshot'
    dbus = 'dbus'
    notify = 'notify'
    notify_reload = 'notify-reload'
    idle = 'idle'


class Unit(BaseModel):
    description: str = Field(..., alias='Description')


class Install(BaseModel):
    something: str


class SystemD(BaseModel):
    unit: Optional[Unit] = Field(alias='Unit', default=None)
    install: Optional[Install] = Field(alias='Install', default=None)

    def dump(self, f: TextIOWrapper) -> None:
        config = ConfigParser()
        for section_name in self.model_fields:
            section_details = getattr(self, section_name)
            if not section_details:
                continue
            config.add_section(section_name)
            for field in cast(BaseModel, section_details).model_fields:
                value = getattr(section_details, field)
                config.set(section_name, field, str(value))
        config.write(f)


class Service(SystemD):
    class ServiceSection(BaseModel):
        service_type: ServiceType = Field(..., alias='Type')
        exec_start: str = Field(..., alias='ExecStart')
    service: ServiceSection


class Timer(SystemD):
    class TimerSection(BaseModel):
        on_calendar: str = Field(..., alias='OnCalendar')
        persistent: bool = Field(..., alias='Persistent')
    timer: TimerSection
