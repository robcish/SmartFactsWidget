package com.robcish.smartfactswidget.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "facts")
data class FactEntity(
    @PrimaryKey val id: String,
    val locale: String,
    val title: String,
    val teaser: String,
    val bodyMd: String,
    val category: String,
    val releaseEpochMs: Long,
    val published: Boolean,
    val version: Int,
    val updatedAt: Long,
    val isFavorite: Boolean = false,
)
