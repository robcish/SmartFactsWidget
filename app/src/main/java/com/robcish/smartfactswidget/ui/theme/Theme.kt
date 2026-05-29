package com.robcish.smartfactswidget.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.foundation.isSystemInDarkTheme

private val LightColors = lightColorScheme(
    primary = AccentYellow,
    onPrimary = TextPrimary,
    secondary = AccentYellowDark,
    background = BackgroundLight,
    onBackground = TextPrimary,
    surface = BackgroundLight,
    onSurface = TextPrimary,
)

private val DarkColors = darkColorScheme(
    primary = AccentYellow,
    onPrimary = TextPrimary,
    secondary = AccentYellowDark,
    background = BackgroundDark,
    onBackground = androidx.compose.ui.graphics.Color.White,
    surface = BackgroundDark,
    onSurface = androidx.compose.ui.graphics.Color.White,
)

@Composable
fun SmartFactsTheme(content: @Composable () -> Unit) {
    val darkTheme = isSystemInDarkTheme()
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        content = content,
    )
}
