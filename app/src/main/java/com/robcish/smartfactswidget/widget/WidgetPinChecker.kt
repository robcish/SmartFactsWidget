package com.robcish.smartfactswidget.widget

import android.appwidget.AppWidgetManager
import android.content.ComponentName
import android.content.Context
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class WidgetPinChecker @Inject constructor(
    @ApplicationContext private val context: Context,
) {
    fun isWidgetPinned(): Boolean {
        val manager = AppWidgetManager.getInstance(context)
        val provider = ComponentName(context, SmartFactsWidgetReceiver::class.java)
        return manager.getAppWidgetIds(provider).isNotEmpty()
    }
}
