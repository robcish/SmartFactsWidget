package com.robcish.smartfactswidget.worker

import android.content.Context
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.ExistingWorkPolicy
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import com.robcish.smartfactswidget.data.repository.FactRepository
import dagger.hilt.android.qualifiers.ApplicationContext
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SyncScheduler @Inject constructor(
    @ApplicationContext private val context: Context,
    private val factRepository: FactRepository,
) {
    private val workManager = WorkManager.getInstance(context)

    fun schedulePeriodicSync() {
        val request = PeriodicWorkRequestBuilder<SyncFactsWorker>(24, TimeUnit.HOURS)
            .build()

        workManager.enqueueUniquePeriodicWork(
            PERIODIC_SYNC_WORK,
            ExistingPeriodicWorkPolicy.UPDATE,
            request,
        )
    }

    fun enqueueImmediateSync() {
        val request = OneTimeWorkRequestBuilder<SyncFactsWorker>().build()
        workManager.enqueueUniqueWork(
            IMMEDIATE_SYNC_WORK,
            ExistingWorkPolicy.REPLACE,
            request,
        )
    }

    suspend fun scheduleNextSlotRefresh() {
        val locale = factRepository.resolveDeviceLocale()
        val delayMs = factRepository.millisUntilNextSlotBoundary(locale)
        val request = OneTimeWorkRequestBuilder<WidgetSlotRefreshWorker>()
            .setInitialDelay(delayMs, TimeUnit.MILLISECONDS)
            .build()
        workManager.enqueueUniqueWork(
            SLOT_REFRESH_WORK,
            ExistingWorkPolicy.REPLACE,
            request,
        )
    }

    companion object {
        private const val PERIODIC_SYNC_WORK = "sync_facts_periodic"
        private const val IMMEDIATE_SYNC_WORK = "sync_facts_immediate"
        const val SLOT_REFRESH_WORK = "widget_slot_refresh"
    }
}
