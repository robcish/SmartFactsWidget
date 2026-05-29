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
          AND month = :month
          AND day = :day
          AND published = 1
        ORDER BY sequenceIndex ASC
        """,
    )
    suspend fun getFactsForDay(locale: String, month: Int, day: Int): List<FactEntity>

    @Query(
        """
        SELECT * FROM facts
        WHERE locale = :locale
          AND published = 1
        """,
    )
    suspend fun getAllPublished(locale: String): List<FactEntity>

    @Query(
        """
        SELECT * FROM facts
        WHERE id = :id
          AND locale = :locale
          AND published = 1
        LIMIT 1
        """,
    )
    suspend fun getFactById(id: String, locale: String): FactEntity?

    @Query("SELECT COUNT(*) FROM facts")
    suspend fun countAll(): Int

    @Query("SELECT id, locale FROM facts")
    suspend fun getAllKeys(): List<FactKey>

    @Query("DELETE FROM facts WHERE id = :id AND locale = :locale")
    suspend fun deleteByKey(id: String, locale: String)
}
