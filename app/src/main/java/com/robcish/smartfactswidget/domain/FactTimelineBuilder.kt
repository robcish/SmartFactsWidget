package com.robcish.smartfactswidget.domain

import com.robcish.smartfactswidget.data.local.FactEntity
import java.time.ZoneId

object FactTimelineBuilder {

    fun buildBrowsableTimeline(
        allFacts: List<FactEntity>,
        locale: String,
        nowMs: Long = System.currentTimeMillis(),
        daysBack: Int = 7,
        zone: ZoneId = DayScheduleResolver.zoneId(),
    ): List<FactEntity> {
        val localeFacts = allFacts.filter { it.locale == locale }
        val entries = mutableListOf<Pair<Long, FactEntity>>()

        for ((calendarDate, year) in DayScheduleResolver.browsableDates(daysBack, zone)) {
            val dayFacts = localeFacts.filter { it.month == calendarDate.month && it.day == calendarDate.day }
            if (dayFacts.isEmpty()) continue
            for (fact in dayFacts.sortedBy { it.sequenceIndex }) {
                if (DayScheduleResolver.isReleased(dayFacts, fact, calendarDate, year, nowMs, zone)) {
                    val startMs = DayScheduleResolver.effectiveStartMs(dayFacts, fact, calendarDate, year, zone)
                    entries.add(startMs to fact)
                }
            }
        }

        // Newest first: opening today's widget lands on page 0; swipe left → older slots/days.
        return entries.sortedByDescending { it.first }.map { it.second }
    }
}
