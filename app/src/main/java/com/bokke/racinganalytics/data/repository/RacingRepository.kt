package com.bokke.racinganalytics.data.repository

import com.bokke.racinganalytics.data.api.RacingApiService
import com.bokke.racinganalytics.data.model.Race
import com.bokke.racinganalytics.data.model.Horse
import java.time.LocalDate
import java.time.format.DateTimeFormatter

class RacingRepository(private val apiService: RacingApiService) {
    
    suspend fun getTodayRaces(): List<Race> {
        return try {
            val today = LocalDate.now().format(DateTimeFormatter.ISO_DATE)
            val response = apiService.getTodayRaces(today)
            response.data ?: emptyList()
        } catch (e: Exception) {
            emptyList()
        }
    }

    suspend fun getRaceDetails(raceId: String): Race? {
        return try {
            val response = apiService.getRaceDetails(raceId)
            response.data
        } catch (e: Exception) {
            null
        }
    }

    suspend fun getHorsesInRace(raceId: String): List<Horse> {
        return try {
            val response = apiService.getHorsesInRace(raceId)
            response.data ?: emptyList()
        } catch (e: Exception) {
            emptyList()
        }
    }
}