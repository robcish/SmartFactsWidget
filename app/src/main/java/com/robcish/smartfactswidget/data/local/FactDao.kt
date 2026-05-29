package com.robcish.smartfactswidget.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface FactDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(facts: List<FactEntity>)

    @Query(
        """
        SELECT * FROM facts
        WHERE locale = :locale
          AND published = 1
          AND releaseEpochMs <= :nowMs
        ORDER BY releaseEpochMs DESC
        LIMIT 1
        """,
    )
    suspend fun getCurrentFact(locale: String, nowMs: Long): FactEntity?

    @Query(
        """
        SELECT * FROM facts
        WHERE locale = :locale
          AND published = 1
          AND releaseEpochMs <= :nowMs
        ORDER BY releaseEpochMs ASC
        """,
    )
    suspend fun getReleasedTimeline(locale: String, nowMs: Long): List<FactEntity>

    @Query(
        """
        SELECT * FROM facts
        WHERE id = :id
          AND published = 1
          AND releaseEpochMs <= :nowMs
        LIMIT 1
        """,
    )
    suspend fun getFactById(id: String, nowMs: Long): FactEntity?

    @Query("SELECT COUNT(*) FROM facts")
    suspend fun countAll(): Int
}
