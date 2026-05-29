package com.robcish.smartfactswidget.domain

import java.time.LocalDate
import java.time.ZoneId

data class CalendarDate(
    val month: Int,
    val day: Int,
) {
    fun toLocalDate(year: Int): LocalDate = LocalDate.of(year, month, day)

    fun minusDays(days: Long, zone: ZoneId = ZoneId.systemDefault()): CalendarDate {
        val today = LocalDate.now(zone)
        return fromLocalDate(today.minusDays(days))
    }

    companion object {
        fun today(zone: ZoneId = ZoneId.systemDefault()): CalendarDate {
            return fromLocalDate(LocalDate.now(zone))
        }

        fun fromLocalDate(date: LocalDate): CalendarDate {
            return CalendarDate(month = date.monthValue, day = date.dayOfMonth)
        }
    }
}
