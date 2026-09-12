package com.bokke.racinganalytics.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import com.bokke.racinganalytics.data.model.Horse

@Composable
fun RaceDetailsScreen(raceId: String, navController: NavHostController) {
    var horses by remember { mutableStateOf<List<Horse>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var hasSubscription by remember { mutableStateOf(false) }

    LaunchedEffect(raceId) {
        isLoading = false
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            IconButton(onClick = { navController.popBackStack() }) {
                Icon(Icons.Default.ArrowBack, contentDescription = "Back")
            }
            Text(
                text = "Race #$raceId",
                style = MaterialTheme.typography.headlineMedium
            )
        }

        if (isLoading) {
            CircularProgressIndicator(
                modifier = Modifier
                    .align(androidx.compose.ui.Alignment.CenterHorizontally)
                    .padding(32.dp)
            )
        } else {
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 16.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Track Conditions", style = MaterialTheme.typography.titleMedium)
                    Text("Surface: Turf", style = MaterialTheme.typography.bodySmall)
                    Text("Weather: Clear", style = MaterialTheme.typography.bodySmall)
                    Text("Temperature: 22°C", style = MaterialTheme.typography.bodySmall)
                }
            }

            Text(
                text = "Horses in Race",
                style = MaterialTheme.typography.titleMedium,
                modifier = Modifier.padding(bottom = 12.dp)
            )

            if (!hasSubscription) {
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 16.dp)
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally
                    ) {
                        Text("Subscribe for Live Updates", style = MaterialTheme.typography.titleSmall)
                        Button(
                            onClick = { navController.navigate("subscription") },
                            modifier = Modifier.padding(top = 8.dp)
                        ) {
                            Text("View Plans")
                        }
                    }
                }
            } else {
                LazyColumn(
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(horses) { horse ->
                        HorseListItem(horse)
                    }
                }
            }
        }
    }
}

@Composable
fun HorseListItem(horse: Horse) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("${horse.number}. ${horse.name}", style = MaterialTheme.typography.titleSmall)
            Text("Jockey: ${horse.jockey}", style = MaterialTheme.typography.bodySmall)
            Text("Odds: ${horse.odds}", style = MaterialTheme.typography.bodySmall)
        }
    }
}