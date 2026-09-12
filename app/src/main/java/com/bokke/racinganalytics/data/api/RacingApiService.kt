package com.bokke.racinganalytics.data.api

import com.bokke.racinganalytics.data.model.Race
import com.bokke.racinganalytics.data.model.Horse
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface RacingApiService {
    @GET("/api/races")
    suspend fun getTodayRaces(
        @Query("date") date: String
    ): ApiResponse<List<Race>>

    @GET("/api/races/{raceId}")
    suspend fun getRaceDetails(
        @Path("raceId") raceId: String
    ): ApiResponse<Race>

    @GET("/api/races/{raceId}/horses")
    suspend fun getHorsesInRace(
        @Path("raceId") raceId: String
    ): ApiResponse<List<Horse>>

    @GET("/api/tracks")
    suspend fun getTracks(): ApiResponse<List<String>>
}

data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val message: String?
)