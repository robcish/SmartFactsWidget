package com.robcish.smartfactswidget.data.repository

import android.content.Context
import android.util.Log
import com.robcish.smartfactswidget.data.local.FactDao
import com.robcish.smartfactswidget.data.local.FactEntity
import com.robcish.smartfactswidget.data.local.ManifestPreferences
import com.robcish.smartfactswidget.data.mapper.toEntities
import com.robcish.smartfactswidget.data.remote.FactsRemoteDataSource
import com.robcish.smartfactswidget.domain.CalendarDate
import com.robcish.smartfactswidget.domain.DayScheduleResolver
import com.robcish.smartfactswidget.domain.FactTimelineBuilder
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import java.time.LocalDate
import java.time.ZoneId
import java.util.Locale
import javax.inject.Inject
import javax.inject.Singleton

@OptIn(ExperimentalCoroutinesApi::class)
@Singleton
class FactRepositoryImpl @Inject constructor(
    private val factDao: FactDao,
    private val remoteDataSource: FactsRemoteDataSource,
    private val manifestPreferences: ManifestPreferences,
    @ApplicationContext private val context: Context,
) : FactRepository {

    private val syncMutex = Mutex()
    private val refreshTrigger = MutableStateFlow(0)

    override fun resolveDeviceLocale(): String {
        val locales = context.resources.configuration.locales
        if (!locales.isEmpty) {
            val primary = locales[0]
            val language = primary.language.lowercase(Locale.US)
            if (language == "pl") return LOCALE_PL
            if (language == "en") return LOCALE_EN
            // Region-only tags (e.g. en-US device) still report language "en"
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
        val zone = DayScheduleResolver.zoneId()
        val today = CalendarDate.today(zone)
        val year = LocalDate.now(zone).year
        return resolveCurrentForDay(locale, today, year, nowMs)
            ?: resolveCurrentForDay(LOCALE_EN, today, year, nowMs)
    }

    private suspend fun resolveCurrentForDay(
        locale: String,
        calendarDate: CalendarDate,
        year: Int,
        nowMs: Long,
    ): FactEntity? {
        val dayFacts = factDao.getFactsForDay(locale, calendarDate.month, calendarDate.day)
        val current = DayScheduleResolver.pickCurrent(dayFacts, calendarDate, year, nowMs)
        if (current == null && dayFacts.isNotEmpty()) {
            Log.d(
                TAG,
                "No released slot yet for $locale on ${calendarDate.month}/${calendarDate.day} " +
                    "(facts=${dayFacts.size}, db=${factDao.countAll()})",
            )
        }
        return current
    }

    override suspend fun getBrowsableTimeline(locale: String): List<FactEntity> {
        val nowMs = System.currentTimeMillis()
        val timeline = FactTimelineBuilder.buildBrowsableTimeline(
            allFacts = factDao.getAllPublished(locale),
            locale = locale,
            nowMs = nowMs,
        )
        if (timeline.isNotEmpty()) return timeline
        return FactTimelineBuilder.buildBrowsableTimeline(
            allFacts = factDao.getAllPublished(LOCALE_EN),
            locale = LOCALE_EN,
            nowMs = nowMs,
        )
    }

    override suspend fun getFactById(id: String): FactEntity? {
        val locale = resolveDeviceLocale()
        val fact = factDao.getFactById(id, locale)
            ?: factDao.getFactById(id, LOCALE_EN)
            ?: return null
        val zone = DayScheduleResolver.zoneId()
        val nowMs = System.currentTimeMillis()
        val dayFacts = factDao.getFactsForDay(fact.locale, fact.month, fact.day)
        val year = LocalDate.now(zone).year
        val calendarDate = CalendarDate(fact.month, fact.day)
        return if (DayScheduleResolver.isReleased(dayFacts, fact, calendarDate, year, nowMs, zone)) {
            fact
        } else {
            null
        }
    }

    override suspend fun hasLocalFacts(): Boolean = factDao.countAll() > 0

    override suspend fun ensureCacheWarm() {
        if (factDao.countAll() == 0) {
            loadBundledSeed()
        }
        syncFacts()
    }

    private suspend fun loadBundledSeed() {
        runCatching {
            val manifest = remoteDataSource.loadBundledManifest()
            val entities = manifest.facts.filter { it.published }.toEntities()
            if (entities.isNotEmpty()) {
                factDao.upsertAll(entities)
                val version = manifest.manifestVersion.ifBlank { manifest.version.toString() }
                manifestPreferences.setStoredManifestVersion(version)
                refreshTrigger.value = refreshTrigger.value + 1
                logRowCount("bundled seed", entities.size)
            }
        }.onFailure { error ->
            Log.w(TAG, "Bundled seed load failed (will try network sync)", error)
        }
    }

    override suspend fun syncFacts(): Result<Int> = syncMutex.withLock {
        val cachedCount = factDao.countAll()
        runCatching {
            val manifest = remoteDataSource.fetchManifest()
            val version = manifest.manifestVersion.ifBlank { manifest.version.toString() }
            if (version == manifestPreferences.getStoredManifestVersion() && cachedCount > 0) {
                refreshTrigger.value = refreshTrigger.value + 1
                Log.d(TAG, "Manifest unchanged ($version), using $cachedCount cached facts")
                return@withLock Result.success(cachedCount)
            }

            val entities = manifest.facts
                .filter { it.published }
                .toEntities()

            if (entities.isNotEmpty()) {
                factDao.upsertAll(entities)
                manifestPreferences.setStoredManifestVersion(version)
                logRowCount("sync", entities.size)
            } else {
                Log.w(TAG, "Remote manifest contained no published facts")
            }

            refreshTrigger.value = refreshTrigger.value + 1
            entities.size
        }.fold(
            onSuccess = { Result.success(it) },
            onFailure = { error ->
                Log.w(TAG, "syncFacts failed", error)
                if (cachedCount > 0) {
                    refreshTrigger.value = refreshTrigger.value + 1
                    Result.success(cachedCount)
                } else {
                    Result.failure(error)
                }
            },
        )
    }

    override suspend fun millisUntilNextSlotBoundary(locale: String): Long {
        val zone = DayScheduleResolver.zoneId()
        val today = CalendarDate.today(zone)
        val year = LocalDate.now(zone).year
        val dayFacts = factDao.getFactsForDay(locale, today.month, today.day)
            .ifEmpty { factDao.getFactsForDay(LOCALE_EN, today.month, today.day) }
        return DayScheduleResolver.millisUntilNextBoundary(dayFacts, today, year, zone = zone)
    }

    private suspend fun logRowCount(source: String, manifestCount: Int) {
        val rows = factDao.countAll()
        Log.d(TAG, "$source: manifest=$manifestCount rows=$rows")
        if (rows < manifestCount) {
            Log.e(
                TAG,
                "Expected $manifestCount rows but found $rows — uninstall app to reset Room DB",
            )
        }
    }

    companion object {
        private const val TAG = "FactRepository"
        const val LOCALE_PL = "pl-PL"
        const val LOCALE_EN = "en-US"
    }
}
