package com.robcish.smartfactswidget.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class FactsManifestDto(
    val version: Int,
    @SerialName("generated_at") val generatedAt: String,
    val facts: List<FactDto>,
)

@Serializable
data class FactDto(
    val id: String,
    val locale: String,
    val category: String,
    val title: String,
    val teaser: String,
    @SerialName("body_md") val bodyMd: String,
    @SerialName("release_epoch_ms") val releaseEpochMs: Long,
    val published: Boolean,
    val version: Int,
)
