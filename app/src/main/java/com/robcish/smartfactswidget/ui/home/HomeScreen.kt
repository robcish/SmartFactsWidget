package com.robcish.smartfactswidget.ui.home

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.robcish.smartfactswidget.R
import com.robcish.smartfactswidget.ui.category.CategoryIcons
import com.robcish.smartfactswidget.ui.theme.AccentYellow
import com.robcish.smartfactswidget.ui.theme.TextPrimary

@Composable
fun HomeScreen(
    onOpenDetail: (String) -> Unit,
    viewModel: HomeViewModel = hiltViewModel(),
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.Start,
    ) {
        Text(
            text = stringResource(R.string.app_name),
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            color = TextPrimary,
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = stringResource(R.string.home_tagline),
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f),
        )
        Spacer(modifier = Modifier.height(32.dp))

        when {
            uiState.isLoading -> {
                CircularProgressIndicator(color = AccentYellow)
            }

            uiState.fact != null -> {
                val fact = uiState.fact!!
                Box(modifier = Modifier.fillMaxWidth()) {
                    Icon(
                        imageVector = CategoryIcons.composeIcon(fact.category),
                        contentDescription = null,
                        modifier = Modifier
                            .align(Alignment.CenterEnd)
                            .size(96.dp)
                            .alpha(0.1f),
                        tint = TextPrimary,
                    )
                    Column {
                        Text(
                            text = fact.title,
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.SemiBold,
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            text = fact.teaser,
                            style = MaterialTheme.typography.bodyLarge,
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                        Button(
                            onClick = { onOpenDetail(fact.id) },
                            modifier = Modifier.fillMaxWidth(),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = AccentYellow,
                                contentColor = TextPrimary,
                            ),
                        ) {
                            Text(stringResource(R.string.read_more))
                        }
                    }
                }
            }

            else -> {
                Text(
                    text = stringResource(R.string.no_fact_title),
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = stringResource(R.string.no_fact_message),
                    style = MaterialTheme.typography.bodyMedium,
                )
            }
        }
    }
}
