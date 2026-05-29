package com.robcish.smartfactswidget.worker

import android.content.Context
import androidx.glance.appwidget.updateAll
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.robcish.smartfactswidget.widget.SmartFactsWidget
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject

@HiltWorker
class WidgetSlotRefreshWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted workerParams: WorkerParameters,
    private val syncScheduler: SyncScheduler,
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result {
        SmartFactsWidget().updateAll(applicationContext)
        syncScheduler.scheduleNextSlotRefresh()
        return Result.success()
    }
}
