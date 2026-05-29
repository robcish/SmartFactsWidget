package com.robcish.smartfactswidget.data.repository

import android.content.Context
import com.robcish.smartfactswidget.data.local.FactDao
import com.robcish.smartfactswidget.data.local.FactEntity
import com.robcish.smartfactswidget.data.mapper.toEntities
import com.robcish.smartfactswidget.data.remote.FactsRemoteDataSource
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import java.util.Locale
import javax.inject.Inject
import javax.inject.Singleton

@OptIn(ExperimentalCoroutinesApi::class)
@Singleton
class FactRepositoryImpl @Inject constructor(
    private val factDao: FactDao,
    private val remoteDataSource: FactsRemoteDataSource,
    @ApplicationContext private val context: Context,
) : FactRepository {

    private val syncMutex = Mutex()
    private val refreshTrigger = MutableStateFlow(0)

    override fun resolveDeviceLocale(): String {
        val locales = context.resources.configuration.locales
        if (!locales.isEmpty) {
            val language = locales[0].language.lowercase(Locale.US)
            if (language == "pl") return LOCALE_PL
        }
        return LOCALE_EN
    }

    override fun observeCurrentFact(locale: String): Flow<FactEntity?> {
        return refreshTrigger.flatMapLatest {
            flow { emit(getCurrentFact(locale)) }
        }
    }

    override suspend fun getCurrentFact(locale: String): FactEntity? {
        val nowMs = System.currentTimeMillis()
        return factDao.getCurrentFact(locale, nowMs)
            ?: factDao.getCurrentFact(LOCALE_EN, nowMs)
    }

    override suspend fun getFactTimeline(locale: String): List<FactEntity> {
        val nowMs = System.currentTimeMillis()
        val timeline = factDao.getReleasedTimeline(locale, nowMs)
        if (timeline.isNotEmpty()) return timeline
        return factDao.getReleasedTimeline(LOCALE_EN, nowMs)
    }

    override suspend fun getFactById(id: String): FactEntity? {
        return factDao.getFactById(id, System.currentTimeMillis())
    }

    override suspend fun ensureCacheWarm() {
        if (factDao.countAll() == 0) {
            syncFacts()
        }
    }

    override suspend fun syncFacts(): Result<Int> = syncMutex.withLock {
        runCatching {
            val manifest = remoteDataSource.fetchManifest()
            val nowMs = System.currentTimeMillis()
            val entities = manifest.facts
                .filter { it.published }
                .toEntities(nowMs)

            if (entities.isNotEmpty()) {
                factDao.upsertAll(entities)
            }

            refreshTrigger.value = refreshTrigger.value + 1
            entities.size
        }
    }

    companion object {
        const val LOCALE_PL = "pl-PL"
        const val LOCALE_EN = "en-US"
    }
}
