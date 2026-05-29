package com.robcish.smartfactswidget.data.mapper

import com.robcish.smartfactswidget.data.local.FactEntity
import com.robcish.smartfactswidget.data.remote.FactDto

fun FactDto.toEntity(nowMs: Long = System.currentTimeMillis()): FactEntity {
    return FactEntity(
        id = id,
        locale = locale,
        title = title,
        teaser = teaser,
        bodyMd = bodyMd,
        category = category,
        month = month,
        day = day,
        sequenceIndex = sequenceIndex,
        published = published,
        version = version,
        updatedAt = nowMs,
    )
}

fun List<FactDto>.toEntities(nowMs: Long = System.currentTimeMillis()): List<FactEntity> {
    return map { it.toEntity(nowMs) }
}
