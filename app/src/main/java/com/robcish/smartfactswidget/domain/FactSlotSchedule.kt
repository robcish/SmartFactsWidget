package com.robcish.smartfactswidget.domain

import java.time.Instant
import java.time.ZoneId
import java.time.ZonedDateTime

object FactSlotSchedule {
    val slotHours: List<Int> = listOf(0, 6, 12, 18)

    fun zoneId(): ZoneId = ZoneId.systemDefault()

    /** Start of the active 6-hour slot (inclusive) for [instant]. */
    fun slotStartMs(instantMs: Long = System.currentTimeMillis(), zone: ZoneId = zoneId()): Long {
        val zdt = ZonedDateTime.ofInstant(Instant.ofEpochMilli(instantMs), zone)
        val hour = zdt.hour
        val slotHour = slotHours.last { it <= hour }
        return zdt.withHour(slotHour).withMinute(0).withSecond(0).withNano(0).toInstant().toEpochMilli()
    }

    fun millisUntilNextSlot(nowMs: Long = System.currentTimeMillis(), zone: ZoneId = zoneId()): Long {
        val zdt = ZonedDateTime.ofInstant(Instant.ofEpochMilli(nowMs), zone)
        val hour = zdt.hour
        val nextSlotHour = slotHours.firstOrNull { it > hour }
        val next = if (nextSlotHour != null) {
            zdt.withHour(nextSlotHour).withMinute(0).withSecond(0).withNano(0)
        } else {
            zdt.plusDays(1).withHour(slotHours.first()).withMinute(0).withSecond(0).withNano(0)
        }
        return next.toInstant().toEpochMilli() - nowMs
    }
}
