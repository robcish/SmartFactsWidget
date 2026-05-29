package com.robcish.smartfactswidget.data.repository

import com.robcish.smartfactswidget.data.local.FactEntity
import kotlinx.coroutines.flow.Flow

interface FactRepository {
    fun observeCurrentFact(locale: String): Flow<FactEntity?>
    suspend fun getCurrentFact(locale: String): FactEntity?
    suspend fun getFactTimeline(locale: String): List<FactEntity>
    suspend fun getFactById(id: String): FactEntity?
    suspend fun ensureCacheWarm()
    suspend fun syncFacts(): Result<Int>
    fun resolveDeviceLocale(): String
}
