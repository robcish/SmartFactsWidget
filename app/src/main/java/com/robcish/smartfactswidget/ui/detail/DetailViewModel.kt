package com.robcish.smartfactswidget.ui.detail

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
class DetailViewModel @Inject constructor(
    private val factRepository: FactRepository,
) : ViewModel() {

    private val _uiState = MutableStateFlow(DetailUiState())
    val uiState: StateFlow<DetailUiState> = _uiState.asStateFlow()

    fun load(factId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            val locale = factRepository.resolveDeviceLocale()
            val timeline = factRepository.getBrowsableTimeline(locale)
            val hasLocal = factRepository.hasLocalFacts()
            val initialPage = timeline.indexOfFirst { it.id == factId }.let { index ->
                when {
                    index >= 0 -> index
                    timeline.isNotEmpty() -> timeline.lastIndex
                    else -> 0
                }
            }
            _uiState.update {
                it.copy(
                    timeline = timeline,
                    initialPage = initialPage,
                    isLoading = false,
                    hasError = timeline.isEmpty() && !hasLocal,
                )
            }
        }
    }
}

data class DetailUiState(
    val timeline: List<FactEntity> = emptyList(),
    val initialPage: Int = 0,
    val isLoading: Boolean = true,
    val hasError: Boolean = false,
)
