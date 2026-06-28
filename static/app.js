/**
 * Gráficos Chart.js e interações da interface.
 * Reutiliza os dados do backend Flask (via atributos data-* no HTML).
 */

/* ===== Configuração global Chart.js ===== */

Chart.defaults.color = '#9a9ab0';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.06)';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;

/* ===== Paleta de cores para gráficos ===== */
const CHART_COLORS = [
  { bg: 'rgba(168, 85, 247, 0.2)', border: '#a855f7' },
  { bg: 'rgba(59, 130, 246, 0.2)',  border: '#3b82f6' },
  { bg: 'rgba(6, 182, 212, 0.2)',   border: '#06b6d4' },
  { bg: 'rgba(16, 185, 129, 0.2)',  border: '#10b981' },
  { bg: 'rgba(245, 158, 11, 0.2)',  border: '#f59e0b' },
  { bg: 'rgba(236, 72, 153, 0.2)',  border: '#ec4899' },
];

/* ===== Mini gráficos nos cards do dashboard ===== */

function createMiniChart(canvasId, labels, allValues, lisIndices) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext('2d');

  // Cores por ponto: roxo para LIS, cinza para os demais
  const pointColors = allValues.map((_, i) =>
    lisIndices.includes(i) ? '#a855f7' : 'rgba(154, 154, 176, 0.4)'
  );
  const pointBorders = allValues.map((_, i) =>
    lisIndices.includes(i) ? '#a855f7' : 'rgba(154, 154, 176, 0.3)'
  );
  const pointRadii = allValues.map((_, i) =>
    lisIndices.includes(i) ? 4 : 2.5
  );

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        data: allValues,
        borderColor: 'rgba(168, 85, 247, 0.4)',
        backgroundColor: 'rgba(168, 85, 247, 0.05)',
        borderWidth: 1.5,
        pointBackgroundColor: pointColors,
        pointBorderColor: pointBorders,
        pointRadius: pointRadii,
        pointHoverRadius: 6,
        fill: true,
        tension: 0.3,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1a1a26',
          borderColor: 'rgba(168, 85, 247, 0.3)',
          borderWidth: 1,
          titleColor: '#f0f0f5',
          bodyColor: '#9a9ab0',
          padding: 10,
          cornerRadius: 8,
          displayColors: false,
          callbacks: {
            label: function(ctx) {
              const isLIS = lisIndices.includes(ctx.dataIndex);
              return `${ctx.parsed.y}${isLIS ? ' ★ LIS' : ''}`;
            }
          }
        }
      },
      scales: {
        x: {
          display: false,
        },
        y: {
          display: false,
        }
      },
      interaction: {
        intersect: false,
        mode: 'index',
      },
    }
  });
}

/* ===== Gráfico detalhado na página de exercício ===== */

function createDetailChart(canvasId, labels, allValues, lisIndices, lisValues, metric) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext('2d');

  // Dataset com todos os valores
  const allPointColors = allValues.map((_, i) =>
    lisIndices.includes(i) ? '#a855f7' : 'rgba(154, 154, 176, 0.5)'
  );
  const allPointRadii = allValues.map((_, i) =>
    lisIndices.includes(i) ? 6 : 3
  );

  // Dataset apenas com a LIS (null nos pontos que não são LIS)
  const lisLine = allValues.map((v, i) =>
    lisIndices.includes(i) ? v : null
  );

  // Gradient para a área da LIS
  const gradient = ctx.createLinearGradient(0, 0, 0, 320);
  gradient.addColorStop(0, 'rgba(168, 85, 247, 0.15)');
  gradient.addColorStop(1, 'rgba(168, 85, 247, 0.0)');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Todos os registros',
          data: allValues,
          borderColor: 'rgba(154, 154, 176, 0.3)',
          backgroundColor: 'rgba(154, 154, 176, 0.03)',
          borderWidth: 1.5,
          pointBackgroundColor: allPointColors,
          pointBorderColor: allPointColors,
          pointRadius: allPointRadii,
          pointHoverRadius: 7,
          fill: true,
          tension: 0.2,
          order: 2,
        },
        {
          label: 'Subsequência Crescente (LIS)',
          data: lisLine,
          borderColor: '#a855f7',
          backgroundColor: gradient,
          borderWidth: 2.5,
          pointBackgroundColor: '#a855f7',
          pointBorderColor: '#a855f7',
          pointRadius: 6,
          pointHoverRadius: 8,
          fill: true,
          tension: 0.2,
          spanGaps: true,
          order: 1,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          align: 'end',
          labels: {
            usePointStyle: true,
            pointStyle: 'circle',
            padding: 16,
            font: { size: 11, weight: 500 },
          }
        },
        tooltip: {
          backgroundColor: '#1a1a26',
          borderColor: 'rgba(168, 85, 247, 0.3)',
          borderWidth: 1,
          titleColor: '#f0f0f5',
          bodyColor: '#9a9ab0',
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: function(ctx) {
              const isLIS = lisIndices.includes(ctx.dataIndex);
              const prefix = ctx.dataset.label;
              return `${prefix}: ${ctx.parsed.y} ${metric}${isLIS ? ' ★' : ''}`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: {
            font: { size: 11, weight: 500 },
            maxRotation: 45,
          }
        },
        y: {
          grid: {
            color: 'rgba(255, 255, 255, 0.04)',
          },
          ticks: {
            font: { size: 11 },
          },
          title: {
            display: true,
            text: metric,
            font: { size: 12, weight: 600 },
            color: '#9a9ab0',
          }
        }
      },
      interaction: {
        intersect: false,
        mode: 'index',
      },
    }
  });
}

/* ===== Formulário: adicionar/remover medidas customizadas ===== */

function addMeasurementRow() {
  const container = document.getElementById('measurements-container');
  if (!container) return;

  const row = document.createElement('div');
  row.className = 'measurement-row';
  row.innerHTML = `
    <input type="text" name="measurement_name[]" placeholder="Nome (ex: braco_cm)" required>
    <input type="number" name="measurement_value[]" placeholder="Valor" step="any" required>
    <button type="button" class="btn btn-icon" onclick="removeMeasurementRow(this)" title="Remover">✕</button>
  `;
  container.appendChild(row);

  // Animação
  row.style.opacity = '0';
  row.style.transform = 'translateY(-8px)';
  requestAnimationFrame(() => {
    row.style.transition = 'all 0.25s ease';
    row.style.opacity = '1';
    row.style.transform = 'translateY(0)';
  });
}

function removeMeasurementRow(btn) {
  const row = btn.closest('.measurement-row');
  row.style.transition = 'all 0.2s ease';
  row.style.opacity = '0';
  row.style.transform = 'translateX(-16px)';
  setTimeout(() => row.remove(), 200);
}

/* ===== Flash messages auto-dismiss ===== */

document.addEventListener('DOMContentLoaded', () => {
  const flashes = document.querySelectorAll('.flash-message');
  flashes.forEach((flash, i) => {
    setTimeout(() => {
      flash.style.transition = 'all 0.3s ease';
      flash.style.opacity = '0';
      flash.style.transform = 'translateX(20px)';
      setTimeout(() => flash.remove(), 300);
    }, 3000 + i * 500);
  });
});
