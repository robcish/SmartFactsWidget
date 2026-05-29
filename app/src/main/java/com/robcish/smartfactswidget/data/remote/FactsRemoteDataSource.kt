package com.robcish.smartfactswidget.data.remote

import android.content.Context
import com.robcish.smartfactswidget.BuildConfig
import dagger.hilt.android.qualifiers.ApplicationContext
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.get
import kotlinx.serialization.json.Json
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class FactsRemoteDataSource @Inject constructor(
    private val httpClient: HttpClient,
    @ApplicationContext private val context: Context,
    private val json: Json,
) {
    suspend fun fetchManifest(): FactsManifestDto {
        return try {
            httpClient.get(BuildConfig.FACTS_MANIFEST_URL).body()
        } catch (remoteError: Exception) {
            loadBundledManifest().also {
                if (it.facts.isEmpty()) throw remoteError
            }
        }
    }

    private fun loadBundledManifest(): FactsManifestDto {
        val raw = context.assets.open("seed_facts.json").bufferedReader().use { it.readText() }
        return json.decodeFromString(FactsManifestDto.serializer(), raw)
    }
}
