package com.bokke.racinganalytics.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import com.bokke.racinganalytics.data.model.SubscriptionPlan

@Composable
fun SubscriptionScreen(navController: NavHostController) {
    val plans = listOf(
        SubscriptionPlan(
            id = "monthly",
            name = "Monthly",
            price = 9.99,
            duration = "1 Month",
            features = listOf("Live race updates", "Horse profiles", "Track conditions", "Historical data")
        ),
        SubscriptionPlan(
            id = "quarterly",
            name = "Quarterly",
            price = 24.99,
            duration = "3 Months",
            features = listOf("Live race updates", "Horse profiles", "Track conditions", "Historical data", "Advanced statistics")
        ),
        SubscriptionPlan(
            id = "annual",
            name = "Annual",
            price = 79.99,
            duration = "12 Months",
            features = listOf("Live race updates", "Horse profiles", "Track conditions", "Historical data", "Advanced statistics", "Priority support")
        )
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Choose Your Plan",
            style = MaterialTheme.typography.headlineLarge,
            modifier = Modifier.padding(bottom = 24.dp)
        )

        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(plans) { plan ->
                SubscriptionPlanCard(
                    plan = plan,
                    onSubscribe = {
                        navController.navigate("payment/${plan.id}")
                    }
                )
            }
        }
    }
}

@Composable
fun SubscriptionPlanCard(
    plan: SubscriptionPlan,
    onSubscribe: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(plan.name, style = MaterialTheme.typography.headlineSmall)
            Text(plan.duration, style = MaterialTheme.typography.labelSmall)
            
            Text(
                text = "\$${plan.price}",
                style = MaterialTheme.typography.displaySmall,
                modifier = Modifier.padding(vertical = 8.dp)
            )

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp)
            ) {
                plan.features.forEach { feature ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Icon(
                            Icons.Default.Check,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(20.dp)
                        )
                        Text(feature, style = MaterialTheme.typography.bodySmall)
                    }
                }
            }

            Button(
                onClick = onSubscribe,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 12.dp)
            ) {
                Text("Subscribe Now")
            }
        }
    }
}