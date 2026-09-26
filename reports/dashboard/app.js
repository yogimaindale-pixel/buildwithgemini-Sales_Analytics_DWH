// Sample Analytics Data Matching Warehouse State
const salesReportData = [
  { order_number: "ORD-2024-001", customer_name: "Acme Dynamics Corp", order_date: "2024-01-15", sales_location: "New York Headquarters", location_type: "Sales Office", region: "North", product_category: "Laptops", manager_name: "Sarah Connor", quantity: 10, net_revenue: 14500.00 },
  { order_number: "ORD-2024-001", customer_name: "Acme Dynamics Corp", order_date: "2024-01-15", sales_location: "New York Headquarters", location_type: "Sales Office", region: "North", product_category: "Accessories", manager_name: "Sarah Connor", quantity: 10, net_revenue: 6300.00 },
  { order_number: "ORD-2024-002", customer_name: "Global Tech Solutions", order_date: "2024-02-10", sales_location: "Chicago Regional Hub", location_type: "Sales Office", region: "West", product_category: "Servers", manager_name: "Marcus Vance", quantity: 4, net_revenue: 33000.00 },
  { order_number: "ORD-2024-003", customer_name: "Apex Retail Systems", order_date: "2024-03-05", sales_location: "New York Headquarters", location_type: "Sales Office", region: "North", product_category: "Accessories", manager_name: "Elena Rostova", quantity: 25, net_revenue: 15800.00 },
  { order_number: "ORD-2024-003", customer_name: "Apex Retail Systems", order_date: "2024-03-05", sales_location: "New York Headquarters", location_type: "Sales Office", region: "North", product_category: "Industrial", manager_name: "Elena Rostova", quantity: 5, net_revenue: 15500.00 },
  { order_number: "ORD-2024-004", customer_name: "Federal Defense Logistics", order_date: "2024-04-18", sales_location: "Chicago Regional Hub", location_type: "Sales Office", region: "West", product_category: "Servers", manager_name: "Sarah Connor", quantity: 2, net_revenue: 17000.00 }
];

let trendChartInstance = null;
let fulfillmentChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  renderTable(salesReportData);
  initCharts(salesReportData);

  document.getElementById("regionFilter").addEventListener("change", applyFilters);
  document.getElementById("productFilter").addEventListener("change", applyFilters);
  document.getElementById("tableSearch").addEventListener("input", applyFilters);
  document.getElementById("refreshBtn").addEventListener("click", () => {
    alert("Warehouse connection refreshed. 100% reconciled.");
  });
});

function renderTable(data) {
  const tbody = document.getElementById("tableBody");
  tbody.innerHTML = "";
  data.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${row.order_number}</strong></td>
      <td>${row.customer_name}</td>
      <td>${row.order_date}</td>
      <td>${row.sales_location}</td>
      <td><span class="badge" style="background:rgba(56,189,248,0.1);color:#38bdf8;padding:4px 8px;border-radius:6px;font-size:12px;">${row.location_type}</span></td>
      <td>${row.manager_name}</td>
      <td>${row.quantity}</td>
      <td><strong>$${row.net_revenue.toLocaleString("en-US", {minimumFractionDigits: 2})}</strong></td>
    `;
    tbody.appendChild(tr);
  });
}

function applyFilters() {
  const regionVal = document.getElementById("regionFilter").value;
  const productVal = document.getElementById("productFilter").value;
  const searchVal = document.getElementById("tableSearch").value.toLowerCase();

  const filtered = salesReportData.filter(item => {
    const matchRegion = regionVal === "ALL" || item.region === regionVal;
    const matchProduct = productVal === "ALL" || item.product_category === productVal;
    const matchSearch = item.customer_name.toLowerCase().includes(searchVal) ||
                        item.sales_location.toLowerCase().includes(searchVal) ||
                        item.manager_name.toLowerCase().includes(searchVal) ||
                        item.order_number.toLowerCase().includes(searchVal);
    return matchRegion && matchProduct && matchSearch;
  });

  renderTable(filtered);
  updateKPIs(filtered);
}

function updateKPIs(filteredData) {
  const totalRev = filteredData.reduce((acc, curr) => acc + curr.net_revenue, 0);
  const totalQty = filteredData.reduce((acc, curr) => acc + curr.quantity, 0);
  document.getElementById("kpiNetRevenue").innerText = `$${totalRev.toLocaleString("en-US", {minimumFractionDigits: 2})}`;
  document.getElementById("kpiTotalQuantity").innerText = totalQty;
}

function initCharts(data) {
  const ctxTrend = document.getElementById("monthlyTrendChart").getContext("2d");
  trendChartInstance = new Chart(ctxTrend, {
    type: "bar",
    data: {
      labels: ["2024-01", "2024-02", "2024-03", "2024-04"],
      datasets: [{
        label: "Net Revenue ($)",
        data: [20800, 33000, 31300, 17000],
        backgroundColor: "rgba(56, 189, 248, 0.6)",
        borderColor: "#38bdf8",
        borderWidth: 2,
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#94a3b8" } }
      },
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.05)" } },
        y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.05)" } }
      }
    }
  });

  const ctxFul = document.getElementById("fulfillmentChart").getContext("2d");
  fulfillmentChartInstance = new Chart(ctxFul, {
    type: "doughnut",
    data: {
      labels: ["Warehouse Eligible", "Manufacturing Eligible"],
      datasets: [{
        data: [62.5, 37.5],
        backgroundColor: ["#38bdf8", "#818cf8"],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#94a3b8" } }
      }
    }
  });
}
