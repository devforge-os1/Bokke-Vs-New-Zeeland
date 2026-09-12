package com.bokke.racinganalytics.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import com.bokke.racinganalytics.data.model.Race
import com.bokke.racinganalytics.ui.components.RaceCard

@Composable
fun HomeScreen(navController: NavHostController) {
    var races by remember { mutableStateOf<List<Race>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        isLoading = false
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Today's Races",
            style = MaterialTheme.typography.headlineLarge,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        if (isLoading) {
            CircularProgressIndicator(
                modifier = Modifier
                    .align(androidx.compose.ui.Alignment.CenterHorizontally)
                    .padding(32.dp)
            )
        } else if (races.isEmpty()) {
            Text(
                text = "No races available",
                style = MaterialTheme.typography.bodyMedium,
                modifier = Modifier.padding(16.dp)
            )
        } else {
            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(races) { race ->
                    RaceCard(
                        race = race,
                        onClick = {
                            navController.navigate("race_details/${race.id}")
                        }
                    )
                }
            }
        }
    }
}