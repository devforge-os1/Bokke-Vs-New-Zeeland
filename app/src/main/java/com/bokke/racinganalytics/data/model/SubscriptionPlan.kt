package com.bokke.racinganalytics.data.model

data class SubscriptionPlan(
    val id: String,
    val name: String,
    val price: Double,
    val duration: String,
    val features: List<String>
)