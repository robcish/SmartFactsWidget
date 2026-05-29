package com.robcish.smartfactswidget.data.local

import androidx.room.Entity

@Entity(
    tableName = "facts",
    primaryKeys = ["id", "locale"],
)
data class FactEntity(
    /** Content id shared by locale variants, e.g. 05-29-0-animals */
    val id: String,
    val locale: String,
    val title: String,
    val teaser: String,
    val bodyMd: String,
    val category: String,
    val month: Int,
    val day: Int,
    val sequenceIndex: Int,
    val published: Boolean,
    val version: Int,
    val updatedAt: Long,
    val isFavorite: Boolean = false,
)
