package com.robcish.smartfactswidget.widget

import android.content.Context
import android.content.Intent
import com.robcish.smartfactswidget.DetailActivity

object WidgetNavigation {
    fun detailIntent(context: Context, factId: String): Intent {
        return Intent(context, DetailActivity::class.java).apply {
            setPackage(context.packageName)
            putExtra(DetailActivity.EXTRA_FACT_ID, factId)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
        }
    }
}
