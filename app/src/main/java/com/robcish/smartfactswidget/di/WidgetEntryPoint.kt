package com.robcish.smartfactswidget.di

import com.robcish.smartfactswidget.data.repository.FactRepository
import dagger.hilt.EntryPoint
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent

@EntryPoint
@InstallIn(SingletonComponent::class)
interface WidgetEntryPoint {
    fun factRepository(): FactRepository
}
