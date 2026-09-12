package com.bokke.racinganalytics.data.model

data class User(
    val id: String,
    val email: String,
    val subscriptionId: String?,
    val subscriptionStatus: String,
    val renewalDate: String,
    val paymentMethod: String
)