# Набор из 10 unit-тестов (pytest) для модуля schedule_module.py (Фотография 2)
import pytest
from schedule_module import ScheduleManager, ScheduleError


def test_01_create_valid():
    m = ScheduleManager()
    assert m.create("БД", "Пн", "09:00", "305") == 1


def test_02_read_existing():
    m = ScheduleManager()
    i = m.create("ООП", "Вт", "10:40", "210")
    assert m.read(i)["subject"] == "ООП"


def test_03_read_missing():
    m = ScheduleManager()
    with pytest.raises(KeyError):
        m.read(99)


def test_04_conflict_same_room_time():
    m = ScheduleManager()
    m.create("БД", "Пн", "09:00", "305")
    with pytest.raises(ScheduleError):
        m.create("Сети", "Пн", "09:00", "305")


def test_05_no_conflict_diff_room():
    m = ScheduleManager()
    m.create("БД", "Пн", "09:00", "305")
    assert m.create("Сети", "Пн", "09:00", "306") == 2


def test_06_no_conflict_diff_time():
    m = ScheduleManager()
    m.create("БД", "Пн", "09:00", "305")
    assert m.create("Сети", "Пн", "10:40", "305") == 2


def test_07_update_valid():
    m = ScheduleManager()
    i = m.create("БД", "Пн", "09:00", "305")
    m.update(i, "БД", "Пн", "12:20", "305")
    assert m.read(i)["time"] == "12:20"


def test_08_update_conflict():
    m = ScheduleManager()
    i1 = m.create("БД", "Пн", "09:00", "305")
    i2 = m.create("ООП", "Пн", "10:40", "305")
    with pytest.raises(ScheduleError):
        m.update(i2, "ООП", "Пн", "09:00", "305")


def test_09_delete_lesson():
    m = ScheduleManager()
    i = m.create("БД", "Пн", "09:00", "305")
    assert m.delete(i) and len(m.list_all()) == 0


def test_10_empty_fields_error():
    m = ScheduleManager()
    with pytest.raises(ValueError):
        m.create("", "Пн", "09:00", "305")
