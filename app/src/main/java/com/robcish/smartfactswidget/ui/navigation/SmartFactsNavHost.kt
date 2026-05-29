package com.robcish.smartfactswidget.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.robcish.smartfactswidget.ui.detail.DetailScreen
import com.robcish.smartfactswidget.ui.home.HomeScreen

object Routes {
    const val HOME = "home"
    const val DETAIL = "detail/{factId}"

    fun detail(factId: String) = "detail/$factId"
}

@Composable
fun SmartFactsNavHost() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Routes.HOME,
    ) {
        composable(Routes.HOME) {
            HomeScreen(
                onOpenDetail = { factId ->
                    navController.navigate(Routes.detail(factId))
                },
            )
        }
        composable(
            route = Routes.DETAIL,
            arguments = listOf(navArgument("factId") { type = NavType.StringType }),
        ) { backStackEntry ->
            val factId = backStackEntry.arguments?.getString("factId").orEmpty()
            DetailScreen(
                factId = factId,
                onBack = { navController.popBackStack() },
            )
        }
    }
}
