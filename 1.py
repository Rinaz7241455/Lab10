# Лабораторная работа № 10. Вариант 8: «Расписание» (schedule_module.py)
# Программный модуль CRUD занятий с проверкой конфликтов времени и аудиторий

class ScheduleError(Exception):
    """Исключение при конфликте расписания или некорректных данных."""


class ScheduleManager:
    """Модуль управления расписанием учебных занятий (CRUD)."""

    def __init__(self) -> None:
        self._lessons: dict[int, dict] = {}
        self._next_id: int = 1

    def _has_conflict(self, day: str, time_slot: str, room: str, ignore_id: int | None = None) -> bool:
        for lid, item in self._lessons.items():
            if lid != ignore_id and item["day"] == day and item["time"] == time_slot and item["room"] == room:
                return True
        return False

    def create(self, subject: str, day: str, time_slot: str, room: str) -> int:
        if not subject.strip() or not room.strip():
            raise ValueError("Предмет и аудитория не могут быть пустыми.")
        if self._has_conflict(day, time_slot, room):
            raise ScheduleError(f"Конфликт: аудитория {room} занята ({day}, {time_slot}).")
        lid = self._next_id
        self._next_id += 1
        self._lessons[lid] = {"id": lid, "subject": subject, "day": day, "time": time_slot, "room": room}
        return lid

    def read(self, lid: int) -> dict:
        if lid not in self._lessons:
            raise KeyError(f"Занятие ID={lid} не найдено.")
        return self._lessons[lid]

    def update(self, lid: int, subject: str, day: str, time_slot: str, room: str) -> None:
        if lid not in self._lessons:
            raise KeyError(f"Занятие ID={lid} не найдено.")
        if self._has_conflict(day, time_slot, room, ignore_id=lid):
            raise ScheduleError("Конфликт времени/аудитории при обновлении.")
        self._lessons[lid].update({"subject": subject, "day": day, "time": time_slot, "room": room})

    def delete(self, lid: int) -> bool:
        return self._lessons.pop(lid, None) is not None

    def list_all(self) -> list[dict]:
        return list(self._lessons.values())
