package com.robcish.smartfactswidget

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.robcish.smartfactswidget.ui.detail.DetailScreen
import com.robcish.smartfactswidget.ui.theme.SmartFactsTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class DetailActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val factId = intent.getStringExtra(EXTRA_FACT_ID).orEmpty().trim()
        if (factId.isBlank()) {
            startActivity(Intent(this, MainActivity::class.java))
            finish()
            return
        }
        setContent {
            SmartFactsTheme {
                DetailScreen(
                    factId = factId,
                    onBack = { finish() },
                )
            }
        }
    }

    companion object {
        const val EXTRA_FACT_ID = "extra_fact_id"

        fun createIntent(context: android.content.Context, factId: String): Intent {
            return com.robcish.smartfactswidget.widget.WidgetNavigation.detailIntent(context, factId)
        }
    }
}
