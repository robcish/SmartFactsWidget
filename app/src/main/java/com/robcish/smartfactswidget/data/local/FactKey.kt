package com.robcish.smartfactswidget.data.local

import androidx.room.ColumnInfo

/** Primary key columns for [FactEntity] — used when pruning stale rows after manifest sync. */
data class FactKey(
    @ColumnInfo(name = "id") val id: String,
    @ColumnInfo(name = "locale") val locale: String,
)
