package com.bokke.racinganalytics.data.model

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class Race(
    val id: String,
    val number: Int,
    val track: String,
    val time: String,
    val status: String,
    val distance: String,
    val surface: String,
    val weather: String,
    val temperature: Float
) : Parcelable