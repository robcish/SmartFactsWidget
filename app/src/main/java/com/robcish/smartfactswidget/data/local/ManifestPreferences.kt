package com.robcish.smartfactswidget.data.local

import android.content.Context
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ManifestPreferences @Inject constructor(
    @ApplicationContext context: Context,
) {
    private val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun getStoredManifestVersion(): String? = prefs.getString(KEY_MANIFEST_VERSION, null)

    fun setStoredManifestVersion(version: String) {
        prefs.edit().putString(KEY_MANIFEST_VERSION, version).apply()
    }

    companion object {
        private const val PREFS_NAME = "smart_facts_prefs"
        private const val KEY_MANIFEST_VERSION = "manifest_version"
    }
}
