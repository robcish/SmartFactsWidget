package com.robcish.smartfactswidget.widget

import android.content.Context
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.glance.GlanceId
import androidx.glance.GlanceModifier
import androidx.glance.Image
import androidx.glance.ImageProvider
import androidx.glance.action.clickable
import androidx.glance.appwidget.GlanceAppWidget
import androidx.glance.appwidget.action.actionStartActivity
import androidx.glance.appwidget.provideContent
import androidx.glance.background
import androidx.glance.layout.Alignment
import androidx.glance.layout.Box
import androidx.glance.layout.fillMaxSize
import androidx.glance.layout.padding
import androidx.glance.layout.size
import androidx.glance.text.FontWeight
import androidx.glance.text.Text
import androidx.glance.text.TextStyle
import androidx.glance.unit.ColorProvider
import com.robcish.smartfactswidget.data.local.FactEntity
import com.robcish.smartfactswidget.data.repository.FactRepository
import com.robcish.smartfactswidget.di.WidgetEntryPoint
import com.robcish.smartfactswidget.ui.category.CategoryIcons
import dagger.hilt.android.EntryPointAccessors

class SmartFactsWidget : GlanceAppWidget() {

    override suspend fun provideGlance(context: Context, id: GlanceId) {
        val repository = EntryPointAccessors.fromApplication(
            context.applicationContext,
            WidgetEntryPoint::class.java,
        ).factRepository()

        val locale = repository.resolveDeviceLocale()
        repository.ensureCacheWarm()
        var fact = repository.getCurrentFact(locale)
        if (fact == null) {
            repository.syncFacts()
            fact = repository.getCurrentFact(locale)
        }

        provideContent {
            WidgetContent(context = context, fact = fact)
        }
    }
}

@Composable
private fun WidgetContent(context: Context, fact: FactEntity?) {
    val background = ColorProvider(AccentYellow)
    val textColor = ColorProvider(TextDark)
    val watermarkColor = ColorProvider(WatermarkTint)

    Box(
        modifier = GlanceModifier
            .fillMaxSize()
            .background(background)
            .padding(12.dp)
            .then(
                if (fact != null) {
                    GlanceModifier.clickable(
                        actionStartActivity(WidgetNavigation.detailIntent(context, fact.id)),
                    )
                } else {
                    GlanceModifier
                },
            ),
        contentAlignment = Alignment.Center,
    ) {
        if (fact != null) {
            Image(
                provider = ImageProvider(CategoryIcons.drawableRes(fact.category)),
                contentDescription = null,
                modifier = GlanceModifier
                    .size(88.dp)
                    .padding(4.dp),
                colorFilter = androidx.glance.ColorFilter.tint(watermarkColor),
            )
        }

        if (fact == null) {
            Text(
                text = context.getString(com.robcish.smartfactswidget.R.string.widget_empty),
                style = TextStyle(
                    color = textColor,
                    fontSize = 14.sp,
                ),
            )
        } else {
            Text(
                text = fact.teaser,
                style = TextStyle(
                    color = textColor,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Medium,
                ),
                modifier = GlanceModifier.padding(horizontal = 4.dp),
            )
        }
    }
}

private val AccentYellow = androidx.compose.ui.graphics.Color(0xFFFFD54F)
private val TextDark = androidx.compose.ui.graphics.Color(0xFF212121)
private val WatermarkTint = androidx.compose.ui.graphics.Color(0x33212121)
