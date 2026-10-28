// static/js/main.js - Interactive Client Controller
document.addEventListener('DOMContentLoaded', () => {
  initDashboardCharts();
  initPatientExplorer();
  initRiskCalculator();
  initStoryStepper();
  initTableauEmbedder();
});

async function initDashboardCharts() {
  const ageCanvas = document.getElementById('chartAgePrevalence');
  const tierCanvas = document.getElementById('chartRiskTiers');
  const bpCanvas = document.getElementById('chartBpCategories');

  if (!ageCanvas && !tierCanvas && !bpCanvas) return;

  try {
    const res = await fetch('/api/stats');
    const data = await res.json();

    if (ageCanvas) {
      const labels = data.age_groups.map(g => g.age_group);
      new Chart(ageCanvas, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            { label: 'Heart Disease (%)', data: data.age_groups.map(g => g.heart_disease_pct), backgroundColor: '#ef4444' },
            { label: 'Diabetes (%)', data: data.age_groups.map(g => g.diabetes_pct), backgroundColor: '#3b82f6' },
            { label: 'Stroke (%)', data: data.age_groups.map(g => g.stroke_pct), backgroundColor: '#8b5cf6' }
          ]
        },
        options: {
          responsive: true,
          plugins: { legend: { position: 'top' } },
          scales: { y: { beginAtZero: true, max: 100, title: { display: true, text: 'Prevalence Rate (%)' } } }
        }
      });
    }

    if (tierCanvas) {
      const tiers = Object.keys(data.risk_tier_counts);
      const counts = Object.values(data.risk_tier_counts);
      new Chart(tierCanvas, {
        type: 'doughnut',
        data: {
          labels: tiers,
          datasets: [{
            data: counts,
            backgroundColor: ['#22c55e', '#0ea5e9', '#f97316', '#ef4444']
          }]
        },
        options: {
          responsive: true,
          plugins: { legend: { position: 'bottom' } }
        }
      });
    }

    if (bpCanvas) {
      const bpLabels = Object.keys(data.bp_cat_counts);
      const bpCounts = Object.values(data.bp_cat_counts);
      new Chart(bpCanvas, {
        type: 'bar',
        data: {
          labels: bpLabels,
          datasets: [{
            label: 'Patients',
            data: bpCounts,
            backgroundColor: '#0d9488'
          }]
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true } }
        }
      });
    }
  } catch (err) {
    console.error('Failed to load stats API for charts:', err);
  }
}

let currentPage = 1;
async function fetchPatients(page = 1) {
  const tableBody = document.getElementById('patientTableBody');
  const pageLabel = document.getElementById('pageIndicator');
  const countLabel = document.getElementById('totalPatientsCount');
  if (!tableBody) return;

  const tier = document.getElementById('filterTier')?.value || '';
  const gender = document.getElementById('filterGender')?.value || '';
  const ageGroup = document.getElementById('filterAge')?.value || '';

  tableBody.innerHTML = '<tr><td colspan="9" class="text-center py-4 text-muted"><i class="fas fa-spinner fa-spin me-2"></i>Loading patient records...</td></tr>';

  try {
    const url = `/api/patients?page=${page}&limit=12&tier=${encodeURIComponent(tier)}&gender=${encodeURIComponent(gender)}&age_group=${encodeURIComponent(ageGroup)}`;
    const res = await fetch(url);
    const data = await res.json();

    if (countLabel) countLabel.innerText = `${data.total.toLocaleString()} patients matched`;
    if (pageLabel) pageLabel.innerText = `Page ${data.page} of ${Math.max(1, Math.ceil(data.total / 12))}`;

    if (data.patients.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="9" class="text-center py-4 text-muted">No patient records match the selected filters.</td></tr>';
      return;
    }

    let rowsHtml = '';
    data.patients.forEach(p => {
      let tierClass = 'badge-tier-low';
      if (p.risk_tier === 'Moderate') tierClass = 'badge-tier-mod';
      else if (p.risk_tier === 'High') tierClass = 'badge-tier-high';
      else if (p.risk_tier === 'Critical') tierClass = 'badge-tier-crit';

      let hdBadge = p.heart_disease ? '<span class="badge bg-danger me-1">HD</span>' : '';
      let dmBadge = p.diabetes ? '<span class="badge bg-primary me-1">DM</span>' : '';
      let stBadge = p.stroke ? '<span class="badge bg-secondary me-1">Stroke</span>' : '';
      let noBadge = (!p.heart_disease && !p.diabetes && !p.stroke) ? '<span class="text-muted small">None</span>' : '';

      rowsHtml += `
        <tr>
          <td><span class="fw-bold text-dark">${p.patient_id}</span></td>
          <td>${p.age} <span class="text-muted small">(${p.age_group})</span></td>
          <td>${p.gender}</td>
          <td>${p.bmi} <span class="badge bg-light text-dark border">${p.bmi_category}</span></td>
          <td>${p.blood_pressure} mmHg</td>
          <td>${p.glucose} mg/dL</td>
          <td>${hdBadge}${dmBadge}${stBadge}${noBadge}</td>
          <td><span class="fw-bold">${p.calibrated_risk_score}</span></td>
          <td><span class="badge ${tierClass}">${p.risk_tier}</span></td>
        </tr>
      `;
    });
    tableBody.innerHTML = rowsHtml;
    currentPage = data.page;
  } catch (err) {
    tableBody.innerHTML = '<tr><td colspan="9" class="text-center text-danger py-4">Error loading patient data.</td></tr>';
    console.error(err);
  }
}

function initPatientExplorer() {
  const table = document.getElementById('patientTableBody');
  if (!table) return;

  document.getElementById('filterTier')?.addEventListener('change', () => fetchPatients(1));
  document.getElementById('filterGender')?.addEventListener('change', () => fetchPatients(1));
  document.getElementById('filterAge')?.addEventListener('change', () => fetchPatients(1));

  document.getElementById('btnPrevPage')?.addEventListener('click', () => {
    if (currentPage > 1) fetchPatients(currentPage - 1);
  });
  document.getElementById('btnNextPage')?.addEventListener('click', () => {
    fetchPatients(currentPage + 1);
  });

  fetchPatients(1);
}

function initRiskCalculator() {
  const form = document.getElementById('riskCalcForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const resultBox = document.getElementById('calcResultBox');
    if (resultBox) {
      resultBox.classList.remove('d-none');
      resultBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    const formData = new FormData(form);
    const payload = {};
    formData.forEach((val, key) => payload[key] = val);

    try {
      const res = await fetch('/api/predict-risk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (data.error) {
        alert(data.error);
        return;
      }

      document.getElementById('resScoreVal').innerText = data.calibrated_risk_score;
      const tierBadge = document.getElementById('resTierBadge');
      tierBadge.innerText = `${data.risk_tier} Risk`;
      tierBadge.className = `badge fs-5 px-3 py-2 bg-${data.risk_tier_color}`;

      document.getElementById('resRecommendation').innerText = data.recommendation;

      const b = data.breakdown;
      setBar('barAge', b.age_points, 25);
      setBar('barChronic', b.chronic_points, 30);
      setBar('barBP', b.blood_pressure_points, 8);
      setBar('barChol', b.cholesterol_points, 7);
      setBar('barGlu', b.glucose_points, 8);
      setBar('barBMI', b.bmi_points, 7);
      setBar('barLife', b.lifestyle_points, 10);
      setBar('barSymp', b.symptom_points, 5);
    } catch (err) {
      console.error(err);
      alert('Failed to calculate patient risk score.');
    }
  });
}

function setBar(id, val, max) {
  const bar = document.getElementById(id);
  const text = document.getElementById(id + 'Val');
  if (bar) {
    const pct = Math.min(100, Math.round((val / max) * 100));
    bar.style.width = pct + '%';
  }
  if (text) {
    text.innerText = `${val} / ${max} pts`;
  }
}

let currentScene = 1;
const totalScenes = 4;
function initStoryStepper() {
  const storyContainer = document.getElementById('storyContainer');
  if (!storyContainer) return;

  function showScene(sceneNum) {
    for (let i = 1; i <= totalScenes; i++) {
      const el = document.getElementById(`scene-${i}`);
      const stepDot = document.getElementById(`stepDot-${i}`);
      if (el) el.classList.toggle('d-none', i !== sceneNum);
      if (stepDot) {
        stepDot.classList.toggle('btn-primary', i === sceneNum);
        stepDot.classList.toggle('btn-outline-secondary', i !== sceneNum);
      }
    }
    currentScene = sceneNum;
    const txt = document.getElementById('storyProgressText');
    if (txt) txt.innerText = `Scene ${sceneNum} of ${totalScenes}`;

    const prevB = document.getElementById('btnPrevScene');
    const nextB = document.getElementById('btnNextScene');
    if (prevB) prevB.disabled = (sceneNum === 1);
    if (nextB) nextB.disabled = (sceneNum === totalScenes);
  }

  document.getElementById('btnPrevScene')?.addEventListener('click', () => {
    if (currentScene > 1) showScene(currentScene - 1);
  });
  document.getElementById('btnNextScene')?.addEventListener('click', () => {
    if (currentScene < totalScenes) showScene(currentScene + 1);
  });

  for (let i = 1; i <= totalScenes; i++) {
    document.getElementById(`stepDot-${i}`)?.addEventListener('click', () => showScene(i));
  }
  showScene(1);
}

function initTableauEmbedder() {
  const btnApply = document.getElementById('btnApplyCustomTableau');
  const inputUrl = document.getElementById('inputTableauUrl');
  const iframe = document.getElementById('tableauIframe');
  const container = document.getElementById('tableauIframeContainer');
  const placeholder = document.getElementById('tableauLocalSimulation');

  if (!btnApply || !inputUrl) return;

  btnApply.addEventListener('click', () => {
    const url = inputUrl.value.trim();
    if (url) {
      if (iframe && container) {
        iframe.src = url;
        container.classList.remove('d-none');
        if (placeholder) placeholder.classList.add('d-none');
      }
    } else {
      alert('Please enter a valid Tableau Public or Server embed URL.');
    }
  });

  document.getElementById('btnResetTableauSimulation')?.addEventListener('click', () => {
    if (container) container.classList.add('d-none');
    if (placeholder) placeholder.classList.remove('d-none');
    if (inputUrl) inputUrl.value = '';
  });
}
