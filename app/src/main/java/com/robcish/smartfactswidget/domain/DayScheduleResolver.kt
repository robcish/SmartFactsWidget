package com.robcish.smartfactswidget.domain

import com.robcish.smartfactswidget.data.local.FactEntity
import java.time.LocalDate
import java.time.ZoneId
import java.util.concurrent.TimeUnit

object DayScheduleResolver {

    fun zoneId(): ZoneId = ZoneId.systemDefault()

    /** Minutes from local midnight for slot [index] when the day has [count] facts. */
    fun slotStartMinutes(count: Int, index: Int): Int {
        require(index in 0 until count) { "index $index out of range for count $count" }
        return when (count) {
            1 -> 0
            2 -> if (index == 0) 0 else 12 * 60
            3 -> when (index) {
                0 -> 0
                1 -> 8 * 60
                else -> 16 * 60
            }
            4 -> when (index) {
                0 -> 0
                1 -> 6 * 60
                2 -> 12 * 60
                else -> 18 * 60
            }
            else -> (24 * 60 * index) / count
        }
    }

    fun effectiveStartMs(
        dayFacts: List<FactEntity>,
        fact: FactEntity,
        calendarDate: CalendarDate,
        year: Int,
        zone: ZoneId = zoneId(),
    ): Long {
        val sorted = dayFacts.sortedBy { it.sequenceIndex }
        val index = sorted.indexOfFirst { it.id == fact.id }
        if (index < 0) return Long.MAX_VALUE
        val minutes = slotStartMinutes(sorted.size, index)
        var zdt = calendarDate.toLocalDate(year)
            .atStartOfDay(zone)
            .plusMinutes(minutes.toLong())
        if (index == 0 && sorted.isNotEmpty()) {
            zdt = zdt.plusSeconds(1)
        }
        return zdt.toInstant().toEpochMilli()
    }

    fun isReleased(
        dayFacts: List<FactEntity>,
        fact: FactEntity,
        calendarDate: CalendarDate,
        year: Int,
        nowMs: Long,
        zone: ZoneId = zoneId(),
    ): Boolean {
        return effectiveStartMs(dayFacts, fact, calendarDate, year, zone) <= nowMs
    }

    fun pickCurrent(
        dayFacts: List<FactEntity>,
        calendarDate: CalendarDate,
        year: Int,
        nowMs: Long = System.currentTimeMillis(),
        zone: ZoneId = zoneId(),
    ): FactEntity? {
        if (dayFacts.isEmpty()) return null
        return dayFacts
            .filter { isReleased(dayFacts, it, calendarDate, year, nowMs, zone) }
            .maxByOrNull { effectiveStartMs(dayFacts, it, calendarDate, year, zone) }
    }

    fun millisUntilNextBoundary(
        dayFacts: List<FactEntity>,
        calendarDate: CalendarDate,
        year: Int,
        nowMs: Long = System.currentTimeMillis(),
        zone: ZoneId = zoneId(),
    ): Long {
        if (dayFacts.isEmpty()) {
            return TimeUnit.HOURS.toMillis(6)
        }
        val sorted = dayFacts.sortedBy { it.sequenceIndex }
        val starts = sorted.map { effectiveStartMs(sorted, it, calendarDate, year, zone) }
        val nextStart = starts.firstOrNull { it > nowMs }
        if (nextStart != null) {
            return (nextStart - nowMs).coerceAtLeast(TimeUnit.SECONDS.toMillis(30))
        }
        val tomorrow = calendarDate.toLocalDate(year).plusDays(1)
        val nextDayStart = tomorrow.atStartOfDay(zone).plusSeconds(1).toInstant().toEpochMilli()
        return (nextDayStart - nowMs).coerceAtLeast(TimeUnit.SECONDS.toMillis(30))
    }

    fun browsableDates(
        daysBack: Int = 7,
        zone: ZoneId = zoneId(),
    ): List<Pair<CalendarDate, Int>> {
        val today = LocalDate.now(zone)
        return (daysBack downTo 0).map { offset ->
            val date = today.minusDays(offset.toLong())
            CalendarDate.fromLocalDate(date) to date.year
        }
    }
}
