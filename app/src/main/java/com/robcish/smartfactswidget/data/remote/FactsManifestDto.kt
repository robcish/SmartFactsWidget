package com.robcish.smartfactswidget.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class FactsManifestDto(
    @SerialName("manifest_version") val manifestVersion: String = "",
    val version: Int = 1,
    @SerialName("generated_at") val generatedAt: String = "",
    val facts: List<FactDto> = emptyList(),
)

@Serializable
data class FactDto(
    val id: String,
    val locale: String,
    val category: String,
    val title: String,
    val teaser: String,
    @SerialName("body_md") val bodyMd: String,
    val month: Int,
    val day: Int,
    @SerialName("sequence_index") val sequenceIndex: Int,
    val published: Boolean,
    val version: Int,
)
