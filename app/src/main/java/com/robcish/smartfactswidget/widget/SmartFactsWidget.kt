package com.robcish.smartfactswidget.widget

import android.content.Context
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.glance.GlanceId
import androidx.glance.GlanceModifier
import androidx.glance.Image
import androidx.glance.ImageProvider
import androidx.glance.LocalSize
import androidx.glance.action.clickable
import androidx.glance.appwidget.GlanceAppWidget
import androidx.glance.appwidget.SizeMode
import androidx.glance.appwidget.action.actionStartActivity
import androidx.glance.appwidget.provideContent
import androidx.glance.background
import androidx.glance.layout.Alignment
import androidx.glance.layout.Box
import androidx.glance.layout.fillMaxSize
import androidx.glance.layout.fillMaxWidth
import androidx.glance.layout.padding
import androidx.glance.layout.size
import androidx.glance.text.FontWeight
import androidx.glance.text.Text
import androidx.glance.text.TextAlign
import androidx.glance.text.TextStyle
import androidx.glance.unit.ColorProvider
import com.robcish.smartfactswidget.data.local.FactEntity
import com.robcish.smartfactswidget.data.repository.FactRepository
import com.robcish.smartfactswidget.di.WidgetEntryPoint
import com.robcish.smartfactswidget.ui.category.CategoryIcons
import dagger.hilt.android.EntryPointAccessors

class SmartFactsWidget : GlanceAppWidget() {

    // Exact size so tall resized widgets get real height (Responsive capped at ~180 dp).
    override val sizeMode: SizeMode = SizeMode.Exact

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
    val size = LocalSize.current
    val isStrip = size.height < 80.dp
    val contentPadding = when {
        isStrip -> GlanceModifier.padding(start = 12.dp, end = 8.dp, top = 6.dp, bottom = 6.dp)
        size.width < 150.dp || size.height < 130.dp ->
            GlanceModifier.padding(start = 14.dp, end = 10.dp, top = 8.dp, bottom = 8.dp)
        else -> GlanceModifier.padding(start = 16.dp, end = 12.dp, top = 12.dp, bottom = 12.dp)
    }
    val iconSize = if (isStrip) 16.dp else if (size.width < 150.dp || size.height < 130.dp) 28.dp else 40.dp
    val fontSize = if (isStrip) 11.sp else if (size.width < 150.dp || size.height < 130.dp) 12.sp else 14.sp

    val background = ColorProvider(AccentYellow)
    val textColor = ColorProvider(TextDark)
    val clickModifier = if (fact != null) {
        GlanceModifier.clickable(
            actionStartActivity(WidgetNavigation.detailIntent(context, fact.id)),
        )
    } else {
        GlanceModifier
    }

    Box(
        modifier = GlanceModifier
            .fillMaxSize()
            .background(background)
            .then(contentPadding)
            .then(clickModifier),
    ) {
        when {
            fact == null -> {
                Box(
                    modifier = GlanceModifier.fillMaxSize(),
                    contentAlignment = Alignment.Center,
                ) {
                    Text(
                        text = context.getString(com.robcish.smartfactswidget.R.string.widget_empty),
                        style = TextStyle(
                            color = textColor,
                            fontSize = fontSize,
                            textAlign = TextAlign.Center,
                        ),
                        modifier = GlanceModifier.fillMaxWidth(),
                    )
                }
            }

            else -> {
                Box(
                    modifier = GlanceModifier.fillMaxSize(),
                    contentAlignment = Alignment.BottomEnd,
                ) {
                    Image(
                        provider = ImageProvider(CategoryIcons.drawableRes(fact.category)),
                        contentDescription = null,
                        modifier = GlanceModifier.size(iconSize),
                    )
                }
                Box(
                    modifier = GlanceModifier.fillMaxSize(),
                    contentAlignment = Alignment.CenterStart,
                ) {
                    Text(
                        text = fact.teaser,
                        style = TextStyle(
                            color = textColor,
                            fontSize = fontSize,
                            fontWeight = FontWeight.Medium,
                            textAlign = TextAlign.Start,
                        ),
                        modifier = GlanceModifier.fillMaxWidth(),
                    )
                }
            }
        }
    }
}

private val AccentYellow = androidx.compose.ui.graphics.Color(0xFFFFD54F)
private val TextDark = androidx.compose.ui.graphics.Color(0xFF212121)
