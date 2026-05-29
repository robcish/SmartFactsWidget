package com.robcish.smartfactswidget.ui.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.robcish.smartfactswidget.data.local.FactEntity
import com.robcish.smartfactswidget.data.repository.FactRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val factRepository: FactRepository,
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            val locale = factRepository.resolveDeviceLocale()
            _uiState.update { it.copy(isLoading = true, locale = locale) }

            launch {
                factRepository.observeCurrentFact(locale).collect { fact ->
                    val hasLocal = factRepository.hasLocalFacts()
                    _uiState.update {
                        it.copy(
                            fact = fact,
                            isLoading = false,
                            hasError = fact == null && !hasLocal,
                        )
                    }
                }
            }

            factRepository.ensureCacheWarm()
        }
    }
}

data class HomeUiState(
    val fact: FactEntity? = null,
    val locale: String = "",
    val isLoading: Boolean = true,
    val hasError: Boolean = false,
)
