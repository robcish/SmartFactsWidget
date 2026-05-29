package com.robcish.smartfactswidget.di

import android.content.Context
import androidx.room.Room
import com.robcish.smartfactswidget.data.local.AppDatabase
import com.robcish.smartfactswidget.data.local.FactDao
import com.robcish.smartfactswidget.data.repository.FactRepository
import com.robcish.smartfactswidget.data.repository.FactRepositoryImpl
import dagger.Binds
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    @Singleton
    abstract fun bindFactRepository(impl: FactRepositoryImpl): FactRepository
}

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "smart_facts.db",
        ).build()
    }

    @Provides
    fun provideFactDao(database: AppDatabase): FactDao = database.factDao()
}
