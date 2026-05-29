package com.robcish.smartfactswidget.data.local

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(
    entities = [FactEntity::class],
    version = 2,
    exportSchema = false,
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun factDao(): FactDao
}
