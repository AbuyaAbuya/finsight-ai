import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import AppLayout from "./layouts/AppLayout";

import Dashboard from "./pages/Dashboard";
import TrialBalance from "./pages/TrialBalance";
import IncomeStatement from "./pages/IncomeStatement";
import BalanceSheet from "./pages/BalanceSheet";
import CashFlow from "./pages/CashFlow";
import StatementOfEquity from "./pages/StatementOfEquity";

import Budget from "./pages/Budget";
import Forecast from "./pages/Forecast";
import VarianceAnalysis from "./pages/VarianceAnalysis";
import ScenarioPlanning from "./pages/ScenarioPlanning";

import FinancialRatios from "./pages/FinancialRatios";
import Reports from "./pages/Reports";

import AICopilot from "./pages/AICopilot";
import Settings from "./pages/Settings";

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>

          {/* Executive */}

          <Route
            path="/"
            element={<Dashboard />}
          />

          {/* Financial Reporting */}

          <Route
            path="/trial-balance"
            element={<TrialBalance />}
          />

          <Route
            path="/income-statement"
            element={<IncomeStatement />}
          />

          <Route
            path="/balance-sheet"
            element={<BalanceSheet />}
          />

          <Route
            path="/cash-flow"
            element={<CashFlow />}
          />

          <Route
            path="/statement-equity"
            element={<StatementOfEquity />}
          />

          {/* Planning & Analysis */}

          <Route
            path="/budget"
            element={<Budget />}
          />

          <Route
            path="/forecast"
            element={<Forecast />}
          />

          <Route
            path="/variance"
            element={<VarianceAnalysis />}
          />

          <Route
            path="/scenario"
            element={<ScenarioPlanning />}
          />

          {/* Analytics */}

          <Route
            path="/ratios"
            element={<FinancialRatios />}
          />

          <Route
            path="/reports"
            element={<Reports />}
          />

          {/* AI */}

          <Route
            path="/ai-copilot"
            element={<AICopilot />}
          />

          {/* Administration */}

          <Route
            path="/settings"
            element={<Settings />}
          />

          <Route
            path="*"
            element={<Navigate to="/" replace />}
          />

        </Route>
      </Routes>
    </BrowserRouter>
  );
}