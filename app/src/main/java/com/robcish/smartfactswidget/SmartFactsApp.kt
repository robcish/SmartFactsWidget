package com.robcish.smartfactswidget

import android.app.Application
import androidx.glance.appwidget.updateAll
import androidx.hilt.work.HiltWorkerFactory
import androidx.work.Configuration
import com.robcish.smartfactswidget.data.repository.FactRepository
import com.robcish.smartfactswidget.widget.SmartFactsWidget
import com.robcish.smartfactswidget.worker.SyncScheduler
import dagger.hilt.android.HiltAndroidApp
import javax.inject.Inject
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

@HiltAndroidApp
class SmartFactsApp : Application(), Configuration.Provider {

    @Inject
    lateinit var workerFactory: HiltWorkerFactory

    @Inject
    lateinit var syncScheduler: SyncScheduler

    @Inject
    lateinit var factRepository: FactRepository

    private val appScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    override val workManagerConfiguration: Configuration
        get() = Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .build()

    override fun onCreate() {
        super.onCreate()
        syncScheduler.schedulePeriodicSync()
        syncScheduler.enqueueImmediateSync()
        appScope.launch {
            factRepository.ensureCacheWarm()
            SmartFactsWidget().updateAll(this@SmartFactsApp)
            syncScheduler.scheduleNextSlotRefresh()
        }
    }
}
