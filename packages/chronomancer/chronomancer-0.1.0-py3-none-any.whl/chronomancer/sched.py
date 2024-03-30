from enum import Enum
from pydantic import BaseModel
import schedule
from typing import Tuple
from .systemd import Service, ServiceType, Timer


class ScheduleMechanism(Enum):
    cron = 'cron'
    systemd = 'systemd'
    native = 'native'


class Config(BaseModel):
    mode: ScheduleMechanism


class ScheduleEntry(BaseModel):
    command: str
    schedule: str

    def get_systemd(self) -> Tuple[Service, Timer]:
        service_section = Service.ServiceSection(Type=ServiceType.simple, ExecStart=self.command)
        service = Service(service=service_section)

        timer_section = Timer.TimerSection(OnCalendar=self.schedule, Persistent=True)
        timer = Timer(timer=timer_section)

        return service, timer
