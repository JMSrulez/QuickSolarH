import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type Site = {
  site_id: string;
  measured_at: string;
  solar_power_w: number | null;
  consumption_power_w: number | null;
  battery_state_of_charge: number | null;
  grid_power_w: number | null;
};

type Dashboard = { sites: Site[]; updated_at: string };

const apiUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function power(value: number | null): string {
  if (value === null) return "—";
  return `${(value / 1000).toFixed(2)} kW`;
}

function App() {
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);

  useEffect(() => {
    const load = async () => {
      const response = await fetch(`${apiUrl}/api/dashboard`);
      if (!response.ok) throw new Error("Impossible de charger le tableau de bord");
      setDashboard(await response.json() as Dashboard);
    };
    void load();
    const timer = window.setInterval(() => void load(), 60_000);
    return () => window.clearInterval(timer);
  }, []);

  const sites = dashboard?.sites ?? [];
  const totalSolar = sites.reduce((sum, site) => sum + (site.solar_power_w ?? 0), 0);
  const totalConsumption = sites.reduce(
    (sum, site) => sum + (site.consumption_power_w ?? 0),
    0,
  );

  return (
    <main>
      <header>
        <div>
          <p className="eyebrow">FUSIONSOLAR · TABLEAU DE BORD</p>
          <h1>Vue énergétique</h1>
          <p className="muted">Les deux fermes réunies sur une seule page.</p>
        </div>
        <span className="status"><i /> Mise à jour automatique</span>
      </header>
      <section className="summary">
        <article><span>Production solaire</span><strong>{power(totalSolar)}</strong></article>
        <article><span>Consommation</span><strong>{power(totalConsumption)}</strong></article>
        <article><span>Sites connectés</span><strong>{sites.length} / 2</strong></article>
      </section>
      <section className="sites">
        {sites.length === 0 ? (
          <div className="empty">En attente de la première collecte Huawei…</div>
        ) : sites.map((site) => (
          <article className="site" key={site.site_id}>
            <div className="site-heading"><h2>{site.site_id}</h2><span className="live">LIVE</span></div>
            <div className="metrics">
              <div><span>Solaire</span><strong>{power(site.solar_power_w)}</strong></div>
              <div><span>Consommation</span><strong>{power(site.consumption_power_w)}</strong></div>
              <div><span>Batterie</span><strong>{site.battery_state_of_charge === null ? "—" : `${site.battery_state_of_charge.toFixed(0)} %`}</strong></div>
              <div><span>Réseau</span><strong>{power(site.grid_power_w)}</strong></div>
            </div>
          </article>
        ))}
      </section>
    </main>
  );
}

import { useEffect, useState } from "react";
createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
