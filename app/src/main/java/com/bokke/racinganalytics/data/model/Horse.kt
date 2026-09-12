package com.bokke.racinganalytics.data.model

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class Horse(
    val id: String,
    val number: Int,
    val name: String,
    val jockey: String,
    val trainer: String,
    val odds: String,
    val form: String,
    val weight: String,
    val age: Int,
    val breed: String
) : Parcelable