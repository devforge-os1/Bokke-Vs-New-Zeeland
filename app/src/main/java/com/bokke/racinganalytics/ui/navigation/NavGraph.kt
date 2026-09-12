package com.bokke.racinganalytics.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.bokke.racinganalytics.ui.screens.HomeScreen
import com.bokke.racinganalytics.ui.screens.RaceDetailsScreen
import com.bokke.racinganalytics.ui.screens.SubscriptionScreen
import com.bokke.racinganalytics.ui.screens.ProfileScreen

seal class NavDestination(val route: String) {
    object Home : NavDestination("home")
    object RaceDetails : NavDestination("race_details/{raceId}")
    object Subscription : NavDestination("subscription")
    object Profile : NavDestination("profile")
}

@Composable
fun NavGraph(
    navController: NavHostController = rememberNavController(),
    startDestination: String = NavDestination.Home.route
) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable(NavDestination.Home.route) {
            HomeScreen(navController)
        }
        composable(NavDestination.RaceDetails.route) { backStackEntry ->
            val raceId = backStackEntry.arguments?.getString("raceId") ?: ""
            RaceDetailsScreen(raceId, navController)
        }
        composable(NavDestination.Subscription.route) {
            SubscriptionScreen(navController)
        }
        composable(NavDestination.Profile.route) {
            ProfileScreen(navController)
        }
    }
}