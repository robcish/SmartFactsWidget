package com.robcish.smartfactswidget.ui.category

import androidx.annotation.DrawableRes
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AutoStories
import androidx.compose.material.icons.outlined.Biotech
import androidx.compose.material.icons.outlined.Calculate
import androidx.compose.material.icons.outlined.Eco
import androidx.compose.material.icons.outlined.FactCheck
import androidx.compose.material.icons.outlined.Gavel
import androidx.compose.material.icons.outlined.Groups
import androidx.compose.material.icons.outlined.HistoryEdu
import androidx.compose.material.icons.outlined.Memory
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material.icons.outlined.Museum
import androidx.compose.material.icons.outlined.Pets
import androidx.compose.material.icons.outlined.Psychology
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.Restaurant
import androidx.compose.material.icons.outlined.RocketLaunch
import androidx.compose.material.icons.outlined.Savings
import androidx.compose.material.icons.outlined.Science
import androidx.compose.material.icons.outlined.SelfImprovement
import androidx.compose.material.icons.outlined.SportsSoccer
import androidx.compose.material.icons.outlined.Star
import androidx.compose.material.icons.outlined.Translate
import androidx.compose.ui.graphics.vector.ImageVector
import com.robcish.smartfactswidget.R

object CategoryIcons {
    private val composeIcons: Map<String, ImageVector> = mapOf(
        "science" to Icons.Outlined.Science,
        "math" to Icons.Outlined.Calculate,
        "biology" to Icons.Outlined.Biotech,
        "animals" to Icons.Outlined.Pets,
        "technology" to Icons.Outlined.Memory,
        "history" to Icons.Outlined.HistoryEdu,
        "geography" to Icons.Outlined.Public,
        "astronomy" to Icons.Outlined.RocketLaunch,
        "language" to Icons.Outlined.Translate,
        "psychology" to Icons.Outlined.Psychology,
        "philosophy" to Icons.Outlined.MenuBook,
        "society" to Icons.Outlined.Groups,
        "law" to Icons.Outlined.Gavel,
        "finance" to Icons.Outlined.Savings,
        "culture" to Icons.Outlined.Museum,
        "mythology" to Icons.Outlined.AutoStories,
        "myth-busting" to Icons.Outlined.FactCheck,
        "general" to Icons.Outlined.Star,
        "reflection" to Icons.Outlined.SelfImprovement,
        "sport" to Icons.Outlined.SportsSoccer,
        "food" to Icons.Outlined.Restaurant,
        "environment" to Icons.Outlined.Eco,
    )

    private val drawableIcons: Map<String, Int> = mapOf(
        "science" to R.drawable.ic_cat_science,
        "math" to R.drawable.ic_cat_math,
        "biology" to R.drawable.ic_cat_biology,
        "animals" to R.drawable.ic_cat_animals,
        "technology" to R.drawable.ic_cat_technology,
        "history" to R.drawable.ic_cat_history,
        "geography" to R.drawable.ic_cat_geography,
        "astronomy" to R.drawable.ic_cat_astronomy,
        "language" to R.drawable.ic_cat_language,
        "psychology" to R.drawable.ic_cat_psychology,
        "philosophy" to R.drawable.ic_cat_philosophy,
        "society" to R.drawable.ic_cat_society,
        "law" to R.drawable.ic_cat_law,
        "finance" to R.drawable.ic_cat_finance,
        "culture" to R.drawable.ic_cat_culture,
        "mythology" to R.drawable.ic_cat_mythology,
        "myth-busting" to R.drawable.ic_cat_myth_busting,
        "general" to R.drawable.ic_cat_general,
        "reflection" to R.drawable.ic_cat_reflection,
        "sport" to R.drawable.ic_cat_sport,
        "food" to R.drawable.ic_cat_food,
        "environment" to R.drawable.ic_cat_environment,
    )

    fun composeIcon(category: String): ImageVector {
        return composeIcons[category] ?: Icons.Outlined.Star
    }

    @DrawableRes
    fun drawableRes(category: String): Int {
        return drawableIcons[category] ?: R.drawable.ic_cat_general
    }
}
